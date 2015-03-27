from flask import abort, request, make_response
from relier.models import Event, Question, Answer
from relier.api import AuthenticatedResource
from datetime import datetime
from flask import g
class QuestionResource(AuthenticatedResource):

    def post(self, event_id):

        if not g.user.can_ask:
            abort(403)

        event = None
        try:
            body = request.json
            content = body['content'].encode('utf-8')
        except Exception:
            abort(400)

        if not content:
            abort(400)

        event = Event.get(Event.id == event_id)
        if not event:
            abort(404)

        try:
             question = Question.create(created=datetime.now(),
                                   content=content, event=event)
        except Exception:
            abort(500)

        response = make_response('', 201)
        response.headers['Location'] = '/events/{id_}/questions/{question_id_}'.format(id_ = event.id, question_id_ = question.id)
        return response



class QuestionInstance(AuthenticatedResource):
    # Retrieve single Question
    def get(self, event_id, question_id):


        if Question.select().where(Question.id == question_id).count() == 0:
            abort(404)

        question = Question.get(Question.id == question_id)
        
        return QuestionInstance.question_to_json(question)

    def delete(self, event_id, question_id):

        if not g.user.is_admin: 
            abort(403)

        question = None
        try:
            question = Question.get(Question.id == question_id)
        except Question.DoesNotExist:
            abort(404)

        answer_delete_query = Answer.delete().where(Answer.question == question)
        answer_delete_query.execute()

        question.delete_instance();
        response = make_response('', 204)
        return response 

    @staticmethod
    def question_to_json(question): 
        
        answer_json = ''
        try:
            answer = Answer.get(Answer.question == question)
            answer_json = answer.JSON()
        except Exception:
            pass
            
        
        return {
                    'id': question.id,
                    'content': question.content,
                    'created': question.created.strftime('%Y-%m-%d %H:%M'),
                    'updated': question.updated.strftime('%Y-%m-%d %H:%M') if question.updated else '',
                    'answer': answer_json
               }

class AnswerResource(AuthenticatedResource): 
    def post(self, event_id, question_id):

        if not g.user.can_answer:
            abort(403)


        try:
            body = request.json
            content = body['content'].encode('utf-8')
        except Exception as e:
            print e 
            abort(400)


        question = Question.get(Question.id == question_id)
        if not question:
            abort(400)

        answer = Answer.create( question = question, 
            created = datetime.now(), 
            content = content)

        response = make_response('', 201)
        response.headers['Location'] = '/events/{id_}/questions/{question_id_}/answers/{answer_id_}'.format(id_ = event_id, question_id_ = question.id, answer_id_ = answer.id)
        return response









