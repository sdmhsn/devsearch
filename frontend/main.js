/* experiment sendiri:
let getProjects = () => {
    fetch('http://127.0.0.1:8000/api/projects/')
      .then(response => response.json())
      .then(data => {
          let wrap = document.getElementById('projects-wrapper');

          data.forEach(element => {
              wrap.innerHTML += `<h3>${element.title}</h3>`
              wrap.innerHTML += `<img src="http://127.0.0.1:8000${element.featured_image}">`
        });
      });
}

getProjects();
*/

/* for login and logut button */
let loginBtn = document.getElementById('login-btn');
let logoutBtn = document.getElementById('logout-btn');

let token = localStorage.getItem('token');
// console.log(token);

if (token) {
    loginBtn.remove();
} else {
    logoutBtn.remove();
}

logoutBtn.addEventListener('click', (e) => {
    e.preventDefault();  // So it's not going to try to send the user somewhere. without this, the page will still in projects-list.html page. the href atribut should in empty value
    localStorage.removeItem('token');
    window.location = 'http://127.0.0.1:5500/login.html'; // going to send user to the login page
});

let projectUrl = 'http://127.0.0.1:8000/api/projects/';

let getProjects = () => {
    fetch(projectUrl)  // by default, fetch API sending the get request
        .then(response => response.json())  // promise. So we're going to take our response and we're going to convert it to Jason data.
        .then(data => {
            // console.log(data);
            buildProjects(data);
        })  // return another promise. data on json response. so data is supposed to be in json response (array/list of projects in json format)
}

let buildProjects = projects => {
    let projectsWrapper = document.getElementById('projects-wrapper');
    projectsWrapper.innerHTML = '';

    for (let i = 0; i < projects.length; i++) {
        let project = projects[i];
        // console.log(project);
        let projectCard = `
            <div class="project--card">
                <img src="http://127.0.0.1:8000${project.featured_image}">
                
                <div>
                    <div class="card--header">
                        <h3>${project.title}</h3>
                        <strong class="vote--option" data-vote="up" data-project="${project.id}">&#43;</strong>
                        <strong class="vote--option" data-vote="down" data-project="${project.id}">&#8722;</strong>
                    </div>
                    <i>${project.vote_ratio}% Positive feedback</i>
                    <p>${project.description.substring(0, 150)}</p> <!-- substring(0, 150): js library. Extract a substring from text -->
                </div>
            </div>
        `;

        projectsWrapper.innerHTML += projectCard;
    }

    // Ad an event listener
    addVoteEvents()
}

let addVoteEvents = () => {
    let voteBtns = document.getElementsByClassName('vote--option');
    // console.log('VOTE BUTTONS:', voteBtns);

    for (let i = 0; voteBtns.length > i; i++) {
        // console.log(voteBtns[i]);
        voteBtns[i].addEventListener('click', (e) => {
            // let token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjQwOTQ1NzczLCJpYXQiOjE2NDA4NTkzNzMsImp0aSI6ImE0YjJmY2IxYTljMTQ1ZDI5M2I5NTlmMDU4ZTgyZjNkIiwidXNlcl9pZCI6MX0.GswyHDZ3v5cE7MUFMK_e6MTUCpvQB4GllLCbcIyaCK4'; // token store in localStorage
            let token = localStorage.getItem('token');  // token is in localStorage
            console.log('TOKEN:', token);
            
            // console.log(i)
            let vote = e.target.dataset.vote  // to get the votes
            let project = e.target.dataset.project  // to get the project id
            // console.log('Vote:', vote, ',', 'Project:', project);
            fetch(`http://127.0.0.1:8000/api/projects/${project}/vote/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json',
                    Authorization: `Bearer ${token}`
                },
                body: JSON.stringify(
                    {
                        "value": vote  // the key and value must be using double quote
                    }
                )
            })
            .then(response => response.json())
            .then(data => {
                console.log('Success', data);
                getProjects();
            });
        });
    }

    console.log(voteBtns);

    voteBtns.forEach(function (element) {
        console.log(element);
    });
    

    // experiment sendiri:
    // for (const voteBtn of voteBtns) {  // kekurangannya tidak terdapat i
        // console.log(voteBtn);
        // voteBtn.addEventListener('click', (e) => {
            // console.log('vote was click:', voteBtn);
        // });
    // }

}

getProjects();