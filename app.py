from flask import Flask, request, jsonify, render_template_string
from google import genai
import os

app = Flask(__name__)

# ✅ API Key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=GEMINI_API_KEY)

# ---------------- FRONTEND ---------------- #
HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
<title>AI Growth Chat</title>
<style>
body {
    margin: 0;
    font-family: Arial;
    background: #0f172a;
    color: white;
    display: flex;
    flex-direction: column;
    height: 100vh;
}

header {
    padding: 15px;
    text-align: center;
    font-size: 20px;
    background: #020617;
    border-bottom: 1px solid #1e293b;
}

#chat {
    flex: 1;
    padding: 20px;
    overflow-y: auto;
    display: flex;
    flex-direction: column;
}

.msg {
    max-width: 70%;
    padding: 12px;
    margin: 8px 0;
    border-radius: 10px;
    line-height: 1.4;
}

.user {
    background: #2563eb;
    align-self: flex-end;
}

.bot {
    background: #1e293b;
}

#quick-prompts {
    padding: 10px;
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
    border-top: 1px solid #1e293b;
}

.quick-btn {
    background: #334155;
    padding: 8px 12px;
    border-radius: 20px;
    cursor: pointer;
    font-size: 12px;
}

.quick-btn:hover {
    background: #475569;
}

#input-area {
    display: flex;
    padding: 10px;
    background: #020617;
}

input {
    flex: 1;
    padding: 12px;
    border: none;
    outline: none;
    background: #1e293b;
    color: white;
}

button {
    padding: 12px;
    margin-left: 10px;
    background: #22c55e;
    border: none;
    cursor: pointer;
}
</style>
</head>

<body>

<header>🚀 Personal Growth AI</header>

<div id="chat"></div>

<div id="quick-prompts">
    <div class="quick-btn" onclick="sendQuick('How to stay consistent?')">Consistency</div>
    <div class="quick-btn" onclick="sendQuick('How to avoid procrastination?')">Stop Procrastination</div>
    <div class="quick-btn" onclick="sendQuick('How to improve focus?')">Improve Focus</div>
    <div class="quick-btn" onclick="sendQuick('Daily routine for success')">Daily Routine</div>
</div>

<div id="input-area">
    <input id="prompt" placeholder="Ask anything..." onkeydown="handleKey(event)" />
    <button onclick="sendMessage()">Send</button>
</div>

<script>
async function sendMessage(message=null) {
    const input = document.getElementById("prompt");
    const text = message || input.value.trim();
    if (!text) return;

    addMessage(text, "user");
    input.value = "";

    const res = await fetch("/generate", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({prompt: text})
    });

    const data = await res.json();

    if (data.success) {
        addMessage(data.response, "bot");
    } else {
        addMessage("Error: " + data.error, "bot");
    }
}

function sendQuick(text) {
    sendMessage(text);
}

function addMessage(text, type) {
    const chat = document.getElementById("chat");
    const div = document.createElement("div");
    div.className = "msg " + type;
    div.innerText = text;
    chat.appendChild(div);
    chat.scrollTop = chat.scrollHeight;
}

function handleKey(e) {
    if (e.key === "Enter") sendMessage();
}
</script>

</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML_PAGE)

# ---------------- API ---------------- #
@app.route("/generate", methods=["POST"])
def generate():
    try:
        data = request.get_json()

        if not data or "prompt" not in data:
            return jsonify({"error": "Prompt is required"}), 400

        user_prompt = data["prompt"]

        final_prompt = f"""
You are a personal growth mentor.

User question:
{user_prompt}

Give:
- 3 actionable steps
- concise answer
- practical advice
"""

        response = client.models.generate_content(
            model="gemini-3-flash-preview",
            contents=final_prompt
        )

        return jsonify({
            "success": True,
            "response": response.text
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)