import os
from flask import Flask
from flask import render_template, request, jsonify

from modeling.get_model import get_response

app = Flask(__name__)

host_addr = "0.0.0.0"
port_num = "20373" # 그래도 폐쇄망에서는 막힘

@app.route('/')
def index():
    return render_template('index.html')

#아래 코드로 답변 띄우는 건 성공 
#그런데 새로 링크 안 파고 한 페이지에서 동적으로 하고 싶음.. ㅜㅜ 

@app.route('/chat', methods = ['POST'])
def chat():
    message = eval(request.data.decode())
    user_message = message['message'][0]['content']

    print(f"입력 메세지: {user_message}")
    response = get_response(user_message)

    llm_message = response['result']
    print(f"답변: {llm_message}")
    return jsonify({'result': llm_message})

if __name__ == '__main__':
    app.run(host = host_addr, port = port_num, debug = True)