const API_URL = "https://chatbot-mlcoe.onrender.com";

function handleKey(event) {
    if (event.key === "Enter") {
        sendMessage();
    }
}

async function sendMessage() {
    const inputField = document.getElementById("user-input");
    const message = inputField.value.trim();

    if (!message) return;

    addMessage(message, "user");
    inputField.value = "";

    const botDiv = addMessage("Typing...", "bot", true);

    try {
        const response = await fetch(`${API_URL}/chat/stream`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ question: message })
        });

        const reader = response.body.getReader();
        const decoder = new TextDecoder();

        let botMessage = "";

        while (true) {
            const { done, value } = await reader.read();
            if (done) break;

            const chunk = decoder.decode(value, { stream: true });
            botMessage += chunk;
            botDiv.innerText = botMessage;
            scrollToBottom();
        }

    } catch (error) {
        botDiv.innerText = "Error connecting to server.";
    }
}

function addMessage(text, sender, isBotStreaming = false) {
    const chatBox = document.getElementById("chat-box");

    const msgDiv = document.createElement("div");
    msgDiv.classList.add("message", sender);

    const bubble = document.createElement("div");
    bubble.classList.add("bubble");

    if (sender === "bot" && isBotStreaming) {
        bubble.classList.add("typing");
    }

    bubble.innerText = text;
    msgDiv.appendChild(bubble);
    chatBox.appendChild(msgDiv);

    scrollToBottom();
    return bubble;
}

function scrollToBottom() {
    const chatBox = document.getElementById("chat-box");
    chatBox.scrollTop = chatBox.scrollHeight;
}
