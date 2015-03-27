from flask.views import MethodView
from flask import render_template, flash, abort, redirect, request
from relier.models import Organization, User, database
import bcrypt

class RegisterView(MethodView):

    def get(self):
        print 'Get hit'
        return render_template('register.j2')

    @staticmethod
    def do_register(
        organization_name,
        first_name,
        last_name,
        email_address,
        password,
        ):

        try:

            if Organization.exists(organization_name):
                abort(409)

            if User.exists(email_address):
                abort(409)

            with database.atomic() as transaction:
                try:
                    organization = Organization.create(name=organization_name)
                except:
                    abort(500)

                db_password = bcrypt.hashpw(password,bcrypt.gensalt())
                
                print "Details"
                print db_password
                print organization.name
                print first_name
                print last_name



                User.create(password = db_password, is_admin = True, organization = organization, firstname = first_name, lastname = last_name, email = email_address)
        except Exception as e: 
            print e
            abort(500)

        return redirect('/login')

    def post(self):
        print 'POST hit'
        print 'form'
        print request.form

        organization_name = request.form.get('organization')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email_address = request.form.get('email')
        password = request.form.get('password').encode('utf-8')

        print organization_name
        print email_address

        if email_address is None:
            flash('Missing email address.')
            return render_template('register.j2')

        if organization_name is None:
            flash('Missing Organization.')
            return render_template('register.j2')

        return RegisterView.do_register(organization_name = organization_name, 
            first_name = first_name, 
            last_name = last_name,
            email_address = email_address, 
            password = password)



			