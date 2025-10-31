# EduBot (Deepseek) - Deployment Ready
This project uses the OpenRouter API (deepseek/deepseek-chat-v3.1:free).

## Setup
1. Upload repository to GitHub.
2. On Render, create a new Web Service and connect the repo.
3. Add Environment Variable: OPENROUTER_API_KEY = <your_key>
4. Build command: pip install -r requirements.txt
5. Start command: gunicorn app:app
