from relier.web.views import AuthenticatedView
from relier.models import Question, Event
from flask import request, render_template, abort, g
from datetime import datetime

class Questions(AuthenticatedView):

    def post(self, event_id):

        if request.form.get('question') is None:
            abort(400)

        if Event.select().where(Event.id == event_id).count() == 0:
            abort(404)

        if not g.user.can_ask:
            abort(403)

        event = Event.get(Event.id == event_id)

        Question.create(event=event, created=datetime.now(),
                        content=request.form['question'])

        return render_template('event.j2', event=event)
