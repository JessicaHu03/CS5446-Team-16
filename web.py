from flask import Flask, render_template, request, jsonify, make_response
from chatgpt import interface, init

APP = Flask("airline chatbot")

@APP.route('/')
def main_page():
    resp = make_response(render_template('index.html'))
    return resp

@APP.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get('message')
    response_message = interface(user_message)
    return jsonify({'reply': response_message})

@APP.route('/reset', methods=['POST', 'GET'])
def reset_conversation():
    init()
    return jsonify({'status': "OK"})

if __name__ == '__main__':
    APP.run(port=5001, host="0.0.0.0")
