from flask.views import MethodView
from flask import render_template, abort
from relier.models import Event
from relier.web.views import AuthenticatedView

class EventView(AuthenticatedView):

    def get(self, event_id):

        if Event.select().where(Event.id == event_id).count() == 0:
            abort(404)

        try:
            event = Event.get(Event.id == event_id)
        except:
            abort(500)

        return render_template('event.j2', event=event)
