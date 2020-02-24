from pymongo import MongoClient
from flask import request


# from bson.json_util import dumps


def connection(database, collection):
    # Connect to the database by creating a MongoDB instance
    client = MongoClient('mongodb://localhost/{}'.format(database))
    db = client[database]
    coll = db[collection]
    return db, coll


def createUser(name):
    # New user into the "users" collection

    endpoint = name.replace(" ", "_")
    user = {"username": str(endpoint)}
    db, coll = connection("sentiment", "users")

    allUsers = [e["username"] for e in list(db.coll.find())]
    if endpoint in allUsers:
        return "Error: This user is already in the database. Please try again."
    else:
        coll.insert_one(user)
        return "User {} has been successfully added to the Users collection.".format(name)

def createChat(*chatName):
    '''
    New chat into the "conversations" collection
    '''
    db, coll = connection("sentiment", "conversations")

    usernames = request.args.getlist("usernames")
    chatName = request.args.get("chatName")
    ids = [list(db.coll.find({"username": e}, "_id")) for e in usernames]
    ids = [i for e in ids for i in e]

    newChat = {
        "chatName": chatName,
        "usernames": {
            "name": usernames,
            "ID": ids
        }
    }

    # Añado en caso de que el usuario no exista en "users"
    allUsers = [e["username"] for e in list(db.coll.find())]
    for e in usernames:
        if e not in allUsers:
            createUser(e)


    allChats = [e["chatName"] for e in list(db.coll.find())]
    if chatName in allChats:
        return "This chat already exists in the database. Please try again"
    else:
        coll.insert_one(newChat)
        return "The chat with the usernames {0} has been successfully added to the Conversations collection.".format(usernames)

def addUser():
    '''
    Adds a new user to an existing chat where this user does not exist
    '''

    db, coll = connection("sentiment", "conversations")

    usernames = request.args.getlist("usernames")
    chatName = request.args.get("chatName")

    coll.update({"chatName": chatName},
                {"$addToSet":{
                    "usernames": usernames}
                })

    return "User {} has been succesfully added to the {} chat.".format(usernames, chatName)

def addMessage():
    '''
    New message into the "conversations" collection
    '''
    db, coll = connection("sentiment", 'messages')

    chatName = request.args.get("chatName")
    usernames = request.args.get("usernames")
    message = request.args.get("message")

    newMessage = {
        "chatName": chatName,
        "username": usernames,
        "message": message
    }

    # Compruebo que tanto el chat como el usuario existen, si no lo añado
    allUsers = [e["username"] for e in list(db.coll.find())]
    if usernames not in allUsers:
        createUser(usernames)

    allChats = [e["chatName"] for e in list(db.coll.find())]
    allMessages = [e["message"] for e in list(db.coll.find())]
    if chatName not in allChats:
        createChat(chatName)
        coll.insert_one(newMessage)
        return "This message of {} has been successfully added to the Messages collection.".format(usernames)
    else:
        if message in allMessages:
            return "This message already exists in the database."
        else:
            coll.insert_one(newMessage)
            return "This message of {} has been successfully added to the Messages collection.".format(usernames)


def getMessages(chatName):
    '''
    Get all the messages of a certain chat
    '''
    db, coll = connection('sentiment', 'messages')
    
    res = {}
    messages = list(db["messages"].find({"chatName": chatName},
                             {"message": 1,
                             "username": 1,
                              "_id": 0}))
    
    """for index, e in enumerate(messages):
        res[index] = {"username": e["username"],
                  "message": e["message"]}"""

    return messages





