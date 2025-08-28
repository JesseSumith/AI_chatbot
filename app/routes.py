from flask import Blueprint, request, jsonify
from app.chatbot import predict_class, get_response
from app.logger import log_interaction
from flask import Blueprint, request, jsonify, render_template


routes = Blueprint("routes", __name__)

@routes.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    message = data.get("message", "")
    intent = predict_class(message)
    response = get_response(intent)
    # Log the conversation
    log_interaction(message, intent, response)

    return jsonify({"intent": intent, "response": response})

@routes.route("/", methods=["GET"])
def home():
    return render_template("index.html")
