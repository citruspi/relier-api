from relier.web.views import AuthenticatedView
from relier.models import Event
from flask import g, render_template

class Events(AuthenticatedView):

    def get(self):

        events = Event.select().where(Event.organization == g.user.organization)

        if events.count() == 0:
            return render_template('get_started.j2')

        events.order_by(Event.start_time.desc())
        return render_template('events.j2', events=events)
