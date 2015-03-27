from flask.views import MethodView
from flask import render_template, request, flash, redirect, session
from relier.models import User

class Login(MethodView):

    def get(self):

        return render_template('login.j2')

    def post(self):

        if request.form.get('email_address') is None:
            flash('Missing email address.')
            return render_template('login.j2')

        if request.form.get('password') is None:
            flash('Missing password.')
            return render_template('login.j2')

        token = User.login(request.form['email_address'],
                            request.form['password'])

        if token is None:
            flash('Incorrect credentials.')
            return render_template('login.j2')

        session['token'] = token
        return redirect('/')
