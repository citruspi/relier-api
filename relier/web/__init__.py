from flask import Flask, session, g, redirect
from relier.web.views import Login
from relier.models import User

app = Flask(__name__)
app.config['SECRET_KEY'] = '42'

@app.before_request
def fetch_user():

    user = User.authenticate(session.get('token'))
    g.user = user

def authenticated(f):

    def decorator(*args, **kwargs):
        if g.user is None:
            return redirect('/login/')
        return f(*args, **kwargs)
    return decorator

app.add_url_rule('/login/', view_func=Login.as_view('login'))
