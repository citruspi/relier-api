from flask.views import MethodView
from flask import render_template, redirect
from relier.models import Event
from relier.web.views import AuthenticatedView

class Home(AuthenticatedView):

    def get(self):

        events = Event.select().count()

        if events > 0:
            event = Event.select().order_by(Event.start_time.desc())[0]
            return redirect('/events/{id_}/'.format(id_ = event.id))
        else:
            return render_template('get_started.j2')
