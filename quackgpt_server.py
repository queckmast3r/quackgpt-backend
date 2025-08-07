from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
LLM_MODEL = "llama3-70b-8192"

@app.route("/")
def home():
    return "QuackGPT is alive 🦆"

@app.route("/quack", methods=["POST"])
def quack():
    data = request.get_json()
    prompt = data.get("prompt", "")

    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": LLM_MODEL,
            "messages": [{"role": "user", "content": prompt}]
        }
    )

    try:
        reply = response.json()["choices"][0]["message"]["content"]
        return jsonify({"reply": reply})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
