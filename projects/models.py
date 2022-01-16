from django.db import models
import uuid
from users.models import Profile


# Create your models here.
class Project(models.Model):
    owner = models.ForeignKey(Profile, null=True, blank=True, on_delete=models.CASCADE)  # SET_NULL change to CASCADE
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    featured_image = models.ImageField(null=True, blank=True, default='default.jpg')  # default='default.jpg': to specify an image by default that will be added if we don't add our own.
    demo_link = models.CharField(max_length=2000, null=True, blank=True)
    source_link = models.CharField(max_length=2000, null=True, blank=True)
    tags = models.ManyToManyField('Tag', blank=True)  # 'Tag': related to Tag class. we can also using ManyToManyField(Tag), but the Tag class should move above the Project class
    vote_total = models.IntegerField(default=0, null=True, blank=True)
    vote_ratio = models.IntegerField(default=0, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    def __str__(self):
        return self.title

    class Meta:
        # ordering = ['-created']  # selain menggunakan queryset API .order_by('-created') pada searchProjects() di utils.py, dapat juga menggunakan penambahan class Meta seperti ini pada models.py. tanda minus pada '-created' untuk menampilkan dari belakang (terbaru)
        # ordering = ['title']  # sort start from 1 or A
        ordering = ['-vote_ratio', '-vote_total', 'title']  # sort by high vote_ratio by value with high vote_total by value and first title by keyword
    
    @property  # to avoid the error when some reason user  deleted the project Image/Picture on clear checked button Featured image in Projects django admin
    def imageURL(self):
        try:
            url = self.featured_image.url
        except:
            url = ''  # if this doesn't exist, we're just going to set the url to an empty string.
        return url

    @property
    def reviewers(self):
        queryset = self.review_set.all().values_list('owner__id', flat=True)
        return queryset

    @property  # decorator property for vote. to make method for review
    def getVoteCount(self):
        reviews = self.review_set.all()
        # print(self.review)
        upVotes = reviews.filter(value='up').count()
        totalVotes = reviews.count()
        ratio = (upVotes / totalVotes) * 100
        self.vote_total = totalVotes
        self.vote_ratio = ratio
        self.save()


class Review(models.Model):
    VOTE_TYPE = (
        ('up', 'Up Vote'),
        ('down', 'Down Vote')
    )
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)  # models.CASCADE: will delete all the reviews if the project is deleted.
    body = models.TextField(null=True, blank=True)
    value = models.CharField(max_length=200, choices=VOTE_TYPE)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    def __str__(self):
        return f'{self.value} --> {self.project}'

    class Meta:
        unique_together = [['owner', 'project']]  # to ensure that we can't add another review with the same owner and projects


class Tag(models.Model):
    name = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    def __str__(self):
        return self.name
