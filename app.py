from flask import Flask, request
from src.mongo import *
from json import dumps

app = Flask(__name__)

# POST endpoints

@app.route('/')
def hello_world():
    return 'Welcome to my chat sentiment analysis API!'

@app.route('/create/user/<name>', methods=['POST'])
def crearUsuario(name):
    return createUser(name)

@app.route('/create/chat/', methods=['POST'])
def crearChat(*chatName):
    return createChat(*chatName)

@app.route('/add/user/', methods=['POST'])
def anadirUsuario():
    return addUser()

@app.route('/create/message/', methods=['POST'])
def anadirMensaje():
    return addMessage()

# GET endpoints

'''{
"chatId":chatId,
"users":getUsers(chatId),
"chatAvgScore":[0.4,0.2,0.4],
"avgByUsr":{0:{compound},
        1:{compound},
            2:{compound}
        },
"messages":[{"text":"Hola","user"}]
}'''


if __name__ == '__main__':
    app.run("0.0.0.0", 5000, debug=True)  # run app in debug mode on port 5000
