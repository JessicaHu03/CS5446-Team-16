from flask import Flask, render_template, request, jsonify, session, make_response
from chatgpt import interface
import uuid

APP = Flask("airline chatbot")
APP.secret_key = 'your_secret_key'  # 用于加密Session

@APP.route('/')
def main_page():
    # 检查是否有 conversation_id
    conversation_id = request.cookies.get('conversation_id')
    if not conversation_id:
        # 如果没有，生成一个新的 conversation_id 并初始化会话数据
        conversation_id = str(uuid.uuid4())
        session['conversation_data'] = {}  # 初始化对话数据

    # 返回页面并设置Cookie
    resp = make_response(render_template('index.html'))
    resp.set_cookie('conversation_id', conversation_id)
    return resp

@APP.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get('message')

    # 检查是否有conversation_id，如果没有，返回错误
    conversation_id = request.cookies.get('conversation_id')
    if not conversation_id:
        return jsonify({'reply': "No active conversation."}), 400

    # 获取对话数据
    conversation_data = session.get('conversation_data', {})

    # 使用 interface 函数处理用户消息
    response_message = interface(user_message)

    # 更新对话数据并存储在session中
    conversation_data['last_message'] = user_message
    session['conversation_data'] = conversation_data

    return jsonify({'reply': response_message})

@APP.route('/reset', methods=['POST'])
def reset_conversation():
    # 清除对话数据和 conversation_id
    session.pop('conversation_data', None)
    resp = make_response("Conversation reset!")
    resp.set_cookie('conversation_id', '', expires=0)  # 删除Cookie
    return resp

if __name__ == '__main__':
    APP.run(port=5001, host="0.0.0.0")
