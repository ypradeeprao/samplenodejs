from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import openai
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Set OpenAI API key using new OpenAI SDK
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 🔮 General assistant
@app.route("/api/ask", methods=["POST"])
def ask():
    data = request.json
    user_prompt = data.get("prompt")

    if not user_prompt:
        return jsonify({"error": "Prompt is required"}), 400

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_prompt}
            ]
        )
        ai_reply = response.choices[0].message.content
        return jsonify({"response": ai_reply})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 👋 Simple welcome message
@app.route("/api/message")
def get_message():
    return jsonify({"message": "Hello from Python Flask (venv)!"})

# 🧮 Calculator + GPT explanation
@app.route("/api/calculate", methods=["POST"])
def calculate():
    data = request.json
    num1 = data.get("num1")
    num2 = data.get("num2")
    operator = data.get("operator")

    if num1 is None or num2 is None or operator is None:
        return jsonify({"error": "Missing num1, num2 or operator"}), 400

    try:
        num1 = float(num1)
        num2 = float(num2)

        if operator == "+":
            result = num1 + num2
        elif operator == "-":
            result = num1 - num2
        elif operator == "*":
            result = num1 * num2
        elif operator == "/":
            if num2 == 0:
                return jsonify({"error": "Division by zero"}), 400
            result = num1 / num2
        else:
            return jsonify({"error": "Unsupported operator"}), 400

        # Ask GPT to explain the result
        explanation_prompt = f"What is the result of {num1} {operator} {num2}, and how would you explain it to a beginner?"

        ai_response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a math tutor."},
                {"role": "user", "content": explanation_prompt}
            ]
        )

        explanation = ai_response.choices[0].message.content

        return jsonify({
            "result": result,
            "explanation": explanation
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 🌐 Serve openapi.yaml for GPT Actions
@app.route("/.well-known/openapi.yaml")
def serve_openapi():
    return send_from_directory(directory=".", path="openapi.yaml", mimetype="text/yaml")

# 🚀 Start Flask server
if __name__ == "__main__":
    app.run(debug=True, port=5000)
