from relier.web.views import AuthenticatedView
from relier.models import Event
from flask import render_template, g, abort, redirect, request

class DeleteEvent(AuthenticatedView):

    def get(self, event_id):

        if not g.user.is_admin:
            abort(403)

        if Event.select().where(Event.id == event_id).count() == 0:
            abort(404)

        event = Event.get(Event.id == event_id)

        event.delete_instance(recursive=True)

        return redirect('/events/')
