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

# 🔮 General assistant REST endpoint (for OpenAI GPT)
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

# 🧮 Calculator + GPT explanation REST endpoint (for OpenAI GPT)
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

# 🧠 MCP initialize endpoint (for Claude Desktop)
@app.route("/mcp/initialize", methods=["POST"])
def mcp_initialize():
    data = request.json
    return jsonify({
        "jsonrpc": "2.0",
        "id": data.get("id"),
        "result": {
            "capabilities": {
                "name": "MCP Assistant",
                "version": "1.0",
                "methods": {
                    "ask": {
                        "description": "Ask a GPT assistant",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "prompt": {"type": "string"}
                            },
                            "required": ["prompt"]
                        }
                    },
                    "calculate": {
                        "description": "Perform basic math with GPT explanation",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "num1": {"type": "number"},
                                "num2": {"type": "number"},
                                "operator": {"type": "string"}
                            },
                            "required": ["num1", "num2", "operator"]
                        }
                    }
                }
            }
        }
    })

# ⚙️ MCP execute endpoint (for Claude Desktop)
@app.route("/mcp/execute", methods=["POST"])
def mcp_execute():
    data = request.json
    method = data.get("params", {}).get("method")
    args = data.get("params", {}).get("args", {})
    request_id = data.get("id")

    if method == "ask":
        return _mcp_ask(args, request_id)
    elif method == "calculate":
        return _mcp_calculate(args, request_id)
    else:
        return jsonify({
            "jsonrpc": "2.0",
            "id": request_id,
            "error": {"code": -32601, "message": f"Unknown method: {method}"}
        })

# MCP logic wrappers
def _mcp_ask(args, request_id):
    prompt = args.get("prompt")
    if not prompt:
        return jsonify({"jsonrpc": "2.0", "id": request_id, "error": "Missing prompt"})

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        ai_reply = response.choices[0].message.content
        return jsonify({"jsonrpc": "2.0", "id": request_id, "result": {"response": ai_reply}})
    except Exception as e:
        return jsonify({"jsonrpc": "2.0", "id": request_id, "error": str(e)})

def _mcp_calculate(args, request_id):
    try:
        num1 = float(args.get("num1"))
        num2 = float(args.get("num2"))
        operator = args.get("operator")

        if operator == "+":
            result = num1 + num2
        elif operator == "-":
            result = num1 - num2
        elif operator == "*":
            result = num1 * num2
        elif operator == "/":
            if num2 == 0:
                return jsonify({"jsonrpc": "2.0", "id": request_id, "error": "Division by zero"})
            result = num1 / num2
        else:
            return jsonify({"jsonrpc": "2.0", "id": request_id, "error": "Unsupported operator"})

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
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {
                "result": result,
                "explanation": explanation
            }
        })
    except Exception as e:
        return jsonify({"jsonrpc": "2.0", "id": request_id, "error": str(e)})

# 🚀 Start Flask server on 0.0.0.0 and dynamic PORT for Render
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
