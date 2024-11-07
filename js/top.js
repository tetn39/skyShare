window.addEventListener("DOMContentLoaded", () =>{
    const send = document.querySelector('.top-show')
    const form = document.querySelector('#form-date');
    send.addEventListener('click', event => {
        form.action="/cgi-bin/all.py"
        form.method="post"
        form.submit()
    })
})