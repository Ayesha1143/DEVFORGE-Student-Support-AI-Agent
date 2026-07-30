const chatBox = document.getElementById("chat-box");
const messageInput = document.getElementById("message");
const sendButton = document.getElementById("send-btn");

// Store conversation history
let history = [];


/* ===========================
        AUTO SCROLL
=========================== */

function scrollToBottom() {

    chatBox.scrollTop = chatBox.scrollHeight;

}


/* ===========================
        USER MESSAGE
=========================== */

function appendUserMessage(message) {

    const row = document.createElement("div");

    row.className = "user-row";

    row.innerHTML = `
        <div class="user-message">
            ${message}
        </div>
    `;

    chatBox.appendChild(row);

    scrollToBottom();

}


/* ===========================
        BOT MESSAGE
=========================== */

function appendBotMessage(message) {

    const row = document.createElement("div");

    row.className = "bot-row";

    // Markdown → HTML
    const formattedMessage = marked.parse(message);

    row.innerHTML = `

        <img
            src="/static/images/logo.png"
            class="avatar"
            alt="Bot"
        >

        <div class="bot-response">

            ${formattedMessage}

        </div>

    `;

    chatBox.appendChild(row);

    scrollToBottom();

}


/* ===========================
        LOADING
=========================== */

function showLoading() {

    const row = document.createElement("div");

    row.className = "bot-row";

    row.id = "loading";

    row.innerHTML = `

        <img
            src="/static/images/logo.png"
            class="avatar"
        >

        <div class="loading">

            <span></span>
            <span></span>
            <span></span>

        </div>

    `;

    chatBox.appendChild(row);

    scrollToBottom();

}


function removeLoading() {

    const loading = document.getElementById("loading");

    if (loading) {

        loading.remove();

    }

}


/* ===========================
        SEND MESSAGE
=========================== */

async function sendMessage() {

    const message = messageInput.value.trim();

    if (!message) return;

    appendUserMessage(message);

    messageInput.value = "";

    sendButton.disabled = true;

    showLoading();

    try {

        const response = await fetch("/chat", {

            method: "POST",

            headers: {

                "Content-Type": "application/json"

            },

            body: JSON.stringify({

                message: message,

                history: history

            })

        });

        removeLoading();

        if (!response.ok) {

            throw new Error("Server Error");

        }

        const data = await response.json();

        appendBotMessage(data.response);

        // Save conversation

        history.push({

            role: "user",

            content: message

        });

        history.push({

            role: "assistant",

            content: data.response

        });

    }

    catch (error) {

        removeLoading();

        appendBotMessage(

            "❌ **Sorry!** Something went wrong while contacting the AI server."

        );

        console.error(error);

    }

    sendButton.disabled = false;

    messageInput.focus();

}


/* ===========================
        EVENTS
=========================== */

sendButton.addEventListener(

    "click",

    sendMessage

);


messageInput.addEventListener(

    "keydown",

    function(event){

        if(event.key==="Enter"){

            event.preventDefault();

            sendMessage();

        }

    }

);