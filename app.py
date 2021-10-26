from flask import Flask, render_template ,request, redirect , url_for 
from flask_socketio import SocketIO , join_room

app = Flask(__name__)
socketio = SocketIO(app)

@app.route("/")
def home():
    # return "<p>Hello, World!</p>"
    title = "code title"
    return render_template("index.html", title = title)

@app.route("/chat")
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

if __name__ == "__main__":
    socketio.run(app ,debug=True)