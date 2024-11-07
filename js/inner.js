window.addEventListener('DOMContentLoaded', () => {
    const select = document.querySelector('#date');
    const form = document.querySelector('#form-date');

        select.addEventListener('change', event => {
            form.action="/cgi-bin/all.py"
            form.method="get"
            form.submit()
        })
})

