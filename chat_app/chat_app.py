from flask import Flask, url_for, redirect, request, session, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_BINDS'] = {'chat': 'sqlite:///chat.db'}
app.secret_key = "this is a terrible secret key"
db = SQLAlchemy(app)

class Chat(db.Model):
    __bind_key__ = 'chat'
    id = db.Column(db.Integer, primary_key=True)
    sender = db.Column(db.String(200), nullable=False)
    message = db.Column(db.String(200), nullable=False)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    def __repr__(self):
        return '<User %r>' % self.username

with app.app_context():
   db.create_all()

users = []
    
@app.route("/")
def default():
    return redirect(url_for("login_controller"))

@app.route("/login/", methods=["GET", "POST"])
def login_controller():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username, password=password).first()
        if user is None:
            print("User doesn't exist")
            return redirect('/login')
        else:
            users.append(user)
            session["loggedin"] = True
            return redirect(url_for('profile', username=username))

    return render_template('loginPage.html')
    
@app.route("/register/", methods=["GET", "POST"])
def register_controller():

    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        password_again = request.form['password_again']

        if password != password_again:
            print("The passwords you entered do not match")
            return redirect(url_for('register_controller'))
        
        try:
            new_user = User(username=username, email=email, password=password)
            db.session.add(new_user)
            db.session.commit()
        except:
            print("User already exists")
            return redirect(url_for('register_controller'))

        return redirect(url_for('profile', username=username)) 
   
    return render_template('register.html')

@app.route("/profile/<username>") #is profile the same as chat_page?
def profile(username=None):
    return render_template('chat_page.html', username=username)

@app.route("/logout/")
def unlogger():
    if "username" in session:
        session.clear()
    return render_template('logoutPage.html')

@app.route("/new_message/", methods=["POST"])
def new_message():
    message = request.form.get("message")
    sender = request.form.get("username")

    try:
        new_message = Chat(sender=sender, message=message)
        db.session.add(new_message)
        db.session.commit()

    except:
        print('There was an error sending your message')

    return jsonify(sender=sender, message=message)
    

@app.route("/messages/")
def messages():

    username = session.get('username')
    chat = Chat.query.all()

    messages = []
    for c in chat:
        messages.append({"id": c.id, "author": c.sender, "message": c.message})

    return jsonify(messages=messages)


if __name__ == "__main__":
	app.run()