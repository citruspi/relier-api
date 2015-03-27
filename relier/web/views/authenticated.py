from flask import g, redirect
from flask.views import MethodView

def authenticated(f):

    def decorator(*args, **kwargs):
        if g.user is None:
            return redirect('/login/')
        return f(*args, **kwargs)
    return decorator

class AuthenticatedView(MethodView):

    decorators = [authenticated]
