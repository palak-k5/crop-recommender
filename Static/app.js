
class Chatbox {
    constructor() {
        this.args = {
            openButton: document.querySelector('.chatbox__button'),
            chatBox: document.querySelector('.chatbox__support'),
            sendButton: document.querySelector('.send__button')
        }

        this.state = false;
        this.message = [];
    }

    display() {
        const { openButton, chatBox, sendButton } = this.args;

        openButton.addEventListener('click', () => this.toggleState(chatBox))
        sendButton.addEventListener('click', () => this.onSendButton(chatBox))

        const node = chatBox.querySelector('input');
        node.addEventListener('keyup', ({ key }) => {
            if (key == "Enter") {
                this.onSendButton(chatBox)
            }
        })
    }

    toggleState(chatBox) {
        this.state = !this.state;

        //show hide box
        if (this.state) {
            chatBox.classList.add('chatbox--active')
        } else {
            chatBox.classList.remove('chatbox--active')
        }
    }

    

}

const chatbox = new Chatbox();
chatbox.display();
const node = document.querySelector('input');
node.addEventListener('keyup', ({ key }) => {
            if (key == "Enter") {
                this.sendMessage()
            }
        })

function sendMessage() {
    const userInput = document.getElementById('user-input').value;
    document.getElementById('user-input').value = '';
    addMessage(userInput, 'user');

    fetch('/chatbot', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ user_input: userInput })
    })
        .then(response => response.json())
        .then(data => {
            const chatbotResponse = data.response;
            addMessage(chatbotResponse, 'chatbot');
        });
}

function addMessage(message, sender) {
    var html = '';
    const chatMsg = document.getElementById('chatbox__messages');
    // const messageDiv = document.createElement('div');
    // messageDiv.className = sender;
    // messageDiv.innerHTML = message;
    if (sender === "chatbot") {
        html += '<div class="messages__item messages__item--visitor">' + message + '</div>'
    }
    else {
        html += '<div class="messages__item messages__item--operator">' + message + '</div>'

    }
    // chatLog.appendChild(messageDiv);
    const chatmessage = document.querySelector('.chatbox__messages');
    chatmessage.innerHTML = html + chatmessage.innerHTML
}
