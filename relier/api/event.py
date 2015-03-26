from flask import abort, request, make_response
from relier.models import Organization, Event
from relier.api import AuthenticatedResource
from datetime import datetime

class EventResource(AuthenticatedResource):
    #Create New Event
    def post(self):

        try:
            body = request.json
            organization_name = body['organization_name'].encode('utf-8')
            start_time_text = body['event']['start_time_text'].encode('utf-8')
            title = body['event']['title'].encode('utf-8')
            description = body['event']['title'].encode('utf-8')
            video_source = body['event']['video_source'].encode('utf-8')
            video_id = body['event']['video_id'].encode('utf-8')
            is_anonymous = body['event']['is_anonymous'].encode('utf-8')

        except Exception:
            abort(400)


        org = Organization.select().where(Organization.name == organization_name).get();
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

    