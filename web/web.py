from flask import Flask, render_template, request, jsonify
import json
import time
import pickle


APP = Flask("airline chatbot")


@APP.route('/')
def main_page():
    return render_template('index.html')


@APP.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get('message')
    response_message = 'ok'
    return jsonify({'reply': response_message})


if __name__ == '__main__':
    APP.run(port=5001, host="0.0.0.0")