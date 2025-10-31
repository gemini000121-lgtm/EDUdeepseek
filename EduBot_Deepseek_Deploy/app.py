from flask import Flask, render_template, request, jsonify
import requests, os, logging, time

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
if not OPENROUTER_API_KEY:
    app.logger.warning("OPENROUTER_API_KEY is not set. Set it in environment variables.")

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL_NAME = "deepseek/deepseek-chat-v3.1:free"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    payload = request.get_json() or {}
    user_message = payload.get('message','').strip()
    if not user_message:
        return jsonify({"error":"message required"}), 400

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    body = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": "You are EduBot — a helpful, friendly assistant for students."},
            {"role": "user", "content": user_message}
        ],
        # you can add other parameters like temperature, max_tokens here
        "temperature": 0.6,
        "max_tokens": 512
    }

    start = time.time()
    try:
        resp = requests.post(OPENROUTER_URL, headers=headers, json=body, timeout=30)
    except Exception as e:
        app.logger.exception("Request to OpenRouter failed")
        return jsonify({"error":"api request failed","details":str(e)}), 500
    latency = time.time() - start

    if resp.status_code != 200:
        app.logger.error("OpenRouter returned %s: %s", resp.status_code, resp.text)
        return jsonify({"error":"upstream error","status_code": resp.status_code, "details": resp.text}), 502

    data = resp.json()
    # safe navigation for reply
    try:
        reply = data["choices"][0]["message"]["content"]
    except Exception:
        app.logger.error("Unexpected response shape: %s", data)
        return jsonify({"error":"invalid response from api","raw": data}), 502

    return jsonify({"reply": reply, "meta": {"latency_s": round(latency,3)}})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=True)
