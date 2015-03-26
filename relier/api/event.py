from flask import abort, request, make_response
from relier.models import Event, JsonHelper
from relier.api import AuthenticatedResource
from datetime import datetime
from flask import g
class EventResource(AuthenticatedResource):
    
    #Create New Event
    def post(self):

        if not g.user.is_admin:
            abort(403)

        try:
            body = request.json
            start_time_text = body['start_time_text'].encode('utf-8')
            title = body['title'].encode('utf-8')
            description = body['description'].encode('utf-8')
            video_source = body['video_source'].encode('utf-8')
            video_id = body['video_id'].encode('utf-8')
            is_anonymous = body.get('is_anonymous', False)

        except Exception as e:
            print e 
            abort(400)


        org = g.user.organization
        if org is None :
            abort(400)
        if not start_time_text: 
            abort(400)
        if not title: 
            abort(400)
        if not video_id: 
            abort(400)

        if not video_source: 
            video_source = "youtube"


        #2015-03-31 8:30 we pbly should think about timezone at some point unless the client side takes care of that 
        start_date = datetime.strptime(start_time_text, '%Y-%m-%d %H:%M')  

        try:
            event  = Event.create(title=title, 
                start_time=start_date, 
                organization= org, 
                description= description, 
                video_id=video_id, 
                is_anonymous = bool(is_anonymous))

        except Exception:
            abort(500)

        response = make_response('', 201)
        response.headers['Location'] = '/events/{id_}/'.format(id_ = event.id)
        return response
    

    def get(self):
        query = Event.select().where(Event.organization == g.user.organization)
        events = [JsonHelper.event_to_json(event= event, questions=True) for event in query]
        return events



class EventInstance(AuthenticatedResource):

    def get(self, event_id):
        event = Event.get(Event.id == event_id)
        return JsonHelper.event_to_json(event=event, questions = True)

    #Update a single event
    def put(self, event_id):

        body = request.json
        if not body:
            abort(400)

        if not g.user.is_admin:
            abort(403)

        event = Event.get(Event.id == event_id )
        if not event: 
            abort(400)


        event.title = body.get('title', event.title)
        event.description = body.get('description', event.description)

        new_start_time_text = body['start_time_text']
        if new_start_time_text: 
            date = datetime.strptime(new_start_time_text,'%Y-%m-%d %H:%M') 
            event.start_date = date

        event.video_id = body.get('video_id', event.video_id)
        event.is_anonymous =  body.get('is_anonymous', event.is_anonymous)



        event.save()

        return {}, 204










    