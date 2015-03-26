from answer import Answer
from question import Question

class JsonHelper:

    @staticmethod
    def event_to_json(event=None, questions = False):

        response = {
                    'id': event.id,
                    'start_time_text': event.start_time.strftime('%Y-%m-%d %H:%M'),
                    'title': event.title,
                    'description': event.description,
                    'video_source' : event.video_source,
                    'video_id' : event.video_id, 
                    'end_time': event.end_time.strftime('%Y-%m-%d %H:%M') if event.end_time else ''
               }


        if questions: 
            response['questions'] = JsonHelper.questions_to_json(event)

        return response

    @staticmethod
    def questions_to_json(event): 
       query = Question.select().where(Question.event == event)
       question_array = [JsonHelper.question_to_json(question) for question in query]
        
       return question_array

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



            
            