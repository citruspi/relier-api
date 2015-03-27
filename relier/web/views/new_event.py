from relier.web.views import AuthenticatedView
from relier.models import Event
from flask import render_template, g, abort, redirect, request
from datetime import datetime

class NewEvent(AuthenticatedView):

    def get(self):

        if not g.user.is_admin:
            abort(403)

        return render_template('new_event.j2')

    def post(self):

        title = request.form.get('title')
        date_time = request.form.get('datetime')
        description = request.form.get('description')
        video_source = request.form.get('video_source')
        video_id = request.form.get('video_id')

        if not title or not datetime or not description:
            abort(400)

        if not g.user.is_admin:
            abort(403)

        date_time = datetime.strptime(date_time, '%Y-%m-%d %H:%M')

        event = Event.create(title=title, start_time=date_time,
                                video_source = video_source,
                                video_id = video_id,
                                organization = g.user.organization,
                                description = description)

        return redirect ('/events/{id_}/'.format(id_ = event.id))
