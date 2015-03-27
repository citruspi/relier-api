from relier.web.views import AuthenticatedView
from relier.models import Question, Event, Answer
from flask import request, render_template, abort, g
from datetime import datetime

class Answers(AuthenticatedView):

    def post(self, event_id, question_id):

        if request.form.get('answer') is None:
            abort(400)

        if Event.select().where(Event.id == event_id).count() == 0:
            abort(404)

        if Question.select().where(Question.id == question_id).count() == 0:
            abort(404)

        if not g.user.can_answer:
            abort(403)

        question = Question.get(Question.id == question_id)

        Answer.create(question=question, created=datetime.now(),
                        content=request.form['answer'])

        return render_template('event.j2', event=question.event)
