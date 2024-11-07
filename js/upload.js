window.addEventListener('DOMContentLoaded', () => {
    // formの画像表示
    const input_file = document.querySelector('#input_file')

    input_file.addEventListener('change', event => {
        const div_element = document.querySelector('#file_viewer')
        const rem_element = document.querySelector('#selected_img')
        if (rem_element !== null) {
            div_element.removeChild(rem_element)
        }
        const upload_file_url = URL.createObjectURL(event.target.files[0]);

        const img_element = document.createElement('img');
        img_element.src = upload_file_url;
        img_element.width = 100;
        img_element.id = 'selected_img'
        img_element.onload = () => {
            URL.revokeObjectURL(this.src);
        }
        console.log(img_element.src)
        
        div_element.appendChild(img_element)
    
    })

    const reset_button = document.querySelector('#reset')
    reset_button.addEventListener('click', event => {
        const div_element = document.querySelector('#file_viewer')
        const rem_element = document.querySelector('#selected_img')

        if (rem_element !== null) {
            div_element.removeChild(rem_element)
        }
    })

    // 今日の日付
    const date = new Date();

        const yyyy = date.getFullYear();
        const mm = ("0"+(date.getMonth()+1)).slice(-2);
        const dd = ("0"+date.getDate()).slice(-2);

    document.querySelector("#today").value=yyyy+'-'+mm+'-'+dd;
})