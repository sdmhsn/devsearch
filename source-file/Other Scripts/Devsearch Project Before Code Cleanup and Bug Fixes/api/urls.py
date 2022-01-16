from django.urls import path
from . import views

from rest_framework_simplejwt.views import (
    TokenObtainPairView,  # when we hit this endpoint and we submit our username and password, it's going to generate a JSON Web tokens for us.
    TokenRefreshView,  # to generate something called a refresh toolkit. it is going to give us a token to generate a new token. So this is how it works. A token is going to be stored in the browser somewhere, and it typically has a short lifespan of usually like five minutes or so, and that's it. So just to make sure that this token doesn't get stolen, somebody doesn't hack our website, that token expires.
)

urlpatterns = [
    path('users/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('users/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('', views.getRoutes),
    path('projects/', views.getProjects),
    path('projects/<str:pk>', views.getProject),
    path('projects/<str:pk>/vote/', views.projectVote),
]
