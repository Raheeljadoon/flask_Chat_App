from flask import Flask, render_template ,request, redirect , url_for 
from flask_socketio import SocketIO , join_room
from flask_login import LoginManager, login_required, login_user,logout_user , current_user
import pymongo
from db import get_user , save_user
from pymongo.errors import DuplicateKeyError 

app = Flask(__name__)
app.secret_key = "raheel"

socketio = SocketIO(app)
login_manager = LoginManager()
login_manager.init_app(app) 
login_manager.login_view = 'login'

@app.route("/")
def home():
    # return "<p>Hello, World!</p>"
    title = "code title"
    return render_template("index.html", title = title)

@app.route("/login", methods = ['GET','POST'])
def login():

    message = ''
    if current_user.is_authenticated:
        return redirect(url_for("home"))
   
    if request.method == 'POST':
       
        username = request.form.get('username')
        password_input = request.form.get('password')
        user = get_user(username)
        print("------------user----------",user)
        if user and user.check_password(password_input):
            login_user(user)
            return redirect(url_for("home"))
        else :
            message = "failed to login"

    return render_template('login.html', message = message)

@app.route("/signup" , methods=['GET','POST'])
def signup():
    message = ''
    if current_user.is_authenticated:
        return redirect(url_for("home"))
   
    if request.method == 'POST':
       
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')
        # user = get_user(username)
        try:
            save_user(username, email , password)
            return redirect(url_for("login"))
        except DuplicateKeyError :
            message = 'user already exists !'
       

    return render_template('signup.html', message = message)



@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))

@app.route("/chat")
@login_required
def chat():
    username = request.args.get('username')
    room = request.args.get('room')
    
    if username and room :
        return render_template('chat.html' , username=username, room=room)
    else :
        return redirect(url_for("home"))

@socketio.on('send_message')
def handle_send_message_event(data):
    app.logger.info("{} has sent the message to the room {} : {}".format(data['username'],data['room'],data['message']))

    socketio.emit('receive_message',data , room = data['room'])


@socketio.on('join_room')
def handle_join_room_event(data):
    app.logger.info("{} has join the room {}".format(data['username'],data['room']))
    join_room(data['room'])
    socketio.emit('join_room_annoucement', data)

@login_manager.user_loader
def load_user(username):
    return get_user(username)


if __name__ == "__main__":
    socketio.run(app ,debug=True)