/* Script for search form and page links */
// Get search form and page links
let searchForm = document.getElementById('searchForm');
let pageLinks = document.getElementsByClassName('page-link');
// console.log(searchForm);

// Ensure search form exists
if (searchForm) {
  for (let i = 0; pageLinks.length > i; i++) {
    pageLinks[i].addEventListener('click', function (e) {
      // console.log('button click');
      e.preventDefault();

      // Get the data attribute:
      let page = this.dataset.page;
      // console.log('page:', page);

      // Add hidden search input to form
      searchForm.innerHTML += `<input value="${page}" name="page" hidden>`;

      // Submit form
      searchForm.submit();
    });
  }
}

/* Script for remove tags in project-form.html template */
let tags = document.getElementsByClassName('project-tag');
// console.log(tags);

for (let i = 0; i < tags.length; i++) {
  tags[i].addEventListener('click', e => {
    let tagId = e.target.dataset.tag;
    let projectId = e.target.dataset.project;

    // console.log(`Tag ID: ${tagId}`);
    // console.log(`Project ID: ${projectId}`);

    fetch('http://127.0.0.1:8000/api/remove-tag/', {
      method: 'DELETE',
      headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(
          {
            "project": projectId,  // the key and value must be using double quote
            "tag": tagId
          }
        )
    })
      .then(response => response.json())
      .then(data => {
        e.target.remove()
      });
  });
}