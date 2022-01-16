// Invoke Functions Call on Document Loaded
document.addEventListener('DOMContentLoaded', function () {
  hljs.highlightAll();
});

let alertWrapper = document.querySelector('.alert')
let alertClose = document.querySelector('.alert__close')
// console.log(alertWrapper)

if (alertWrapper) {
  alertClose.addEventListener('click', () => 
    alertWrapper.style.display = 'none'
  )
}

function closeAlert() {
    alertWrapper.remove()
}

if (alertWrapper) {
    setTimeout(closeAlert, 3000)
}
