'''
    flask spotipy Flask-Session
'''
import os
from flask import Flask, session, request, redirect, render_template
import spotipy
from flask_session import Session

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(64)
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_FILE_DIR'] = './.flask_session/'
Session(app)

@app.route('/')
def index():
    return render_template('index.html')




if __name__ == "__main__":
    app.run(debug=True)