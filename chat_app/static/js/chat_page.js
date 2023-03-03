document.addEventListener('DOMContentLoaded', () => {

    msg_form = document.getElementById('message_form')
    msg_form.addEventListener('submit', function (event) {
        event.preventDefault();

        username = document.getElementById('username').innerHTML;
        message = document.getElementById('message').value;
        console.log(`${username}, ${message}`);

        fetch('/new_message', {
            method: 'POST',
            headers: { 'Content-Type': 'application/x-www-form-urlencoded', charset: 'utf8' },
            body: `username=${username}&message=${message}`
        }).then(response => response.json())
            .then(data => {
                document.getElementById('message').value = ''
            })
            .catch((error) => {
                console.log(error)
            });

    })
    let chat_window = document.getElementById('messages');
    function fetch_messages() {
        fetch('/messages').then(response => response.json())
            .then(results => {

                let messages = ""

                for (let index in results) {
                    let current_set = results[index]
                    for (let i in current_set) {
                        author = current_set[i]["author"]
                        id = current_set[i]["id"]
                        message = current_set[i]["message"]

                        messages += `${author}:\n${message}\n\n`;

                    }
                }
                chat_window.value = messages;
            })
            .catch((error) => {
                chat_window.value = "error retrieving messages from server";
            });
    }
    setInterval(fetch_messages, 5000)
});