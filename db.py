from pymongo import MongoClient
from werkzeug.security import generate_password_hash
from  user import User

client = MongoClient('mongodb://root:pass12345@localhost:27017/')

chat_db = client.get_database('ChatDB')
users_collection = chat_db.get_collection('users')

def save_user(username , email , password):
    password_hash = generate_password_hash(password)
    users_collection.insert_one({'_id' : username,'email' : email , 'password': password_hash})


def get_user(username):
    user_data = users_collection.find_one({"_id": username})
    print("---------user_data----------",user_data)
    return User(user_data["_id"],user_data['email'],user_data['password']) if user_data else None


# save_user("kamal_khan","raheel@gmail.com","pass")
# print(get_user('raheel'))