let form = document.getElementById('login-form');

form.addEventListener('submit', (e) => {
    e.preventDefault();

    let formData = {  // username and password must active account in django app, to take the credentials
        'username': form.username.value,
        'password': form.password.value
    }

    /*
    console.log(formData);
    console.log(formData.username);
    console.log(formData.password);
     */

    fetch(`http://127.0.0.1:8000/api/users/token/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        },
        body: JSON.stringify(formData)
    })
        .then(response => response.json())
        .then(data => {
            // console.log('Success', data);
            if (data.access) {
                localStorage.setItem("token", data.access);
                window.location = 'http://127.0.0.1:5500/projects-list.html'; // going to send user to the next page
            } else {
                alert('Username OR Password did not work!');
            }
        });
    });