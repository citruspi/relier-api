from flask import Flask, session, g, redirect
from relier.web.views import Login, EventView, Home, Events
from relier.models import User

app = Flask(__name__)
app.config['SECRET_KEY'] = '42'

@app.before_request
def fetch_user():

    user = None

    try:
        user = User.authenticate(session.get('token'))
    except:
        pass

    g.user = user

app.add_url_rule('/', view_func=Home.as_view('home'))
app.add_url_rule('/login/', view_func=Login.as_view('login'))
app.add_url_rule('/events/<int:event_id>/', view_func=EventView.as_view('event'))
app.add_url_rule('/events/', view_func=Events.as_view('events'))
