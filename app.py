from flask import Flask, render_template, request, jsonify
from chatbot_logic import get_chatbot_response
import os

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message")
    if not user_message:
        return jsonify({"response": "I didn't hear anything. How can I help?"})
    
    response = get_chatbot_response(user_message)
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True, port=5000)
