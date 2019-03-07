import web
from web import form
import model
import random
from hashlib import sha1

urls = ('/', 'Login',
        '/logout/', 'Logout',
        '/register/', 'Register')

render = web.template.render('templates')
app = web.application(urls, globals())
# A simple user object that doesn't store passwords in plain text
class PasswordHash(object):
    def __init__(self, password_):
        self.salt = "".join(chr(random.randint(33,127)) for x in xrange(64))
        self.saltedpw = sha1(password_ + self.salt).hexdigest()
    def check_password(self, password_):
        """checks if the password is correct"""
        return self.saltedpw == sha1(password_ + self.salt).hexdigest()

# Note: a secure application would never store passwords in plaintext in the source code
users = {
    'radhe' : PasswordHash('free'), 
    'hello' : PasswordHash('hi'),  
    'java' : PasswordHash('josh') }
if web.config.get('_session') is None:
    session = web.session.Session(app, web.session.DiskStore('sessions'),
                              initializer={'user': 'anonymous'})
    web.config._session = session
else:
    session = web.config._session






class Login:
    login = form.Form(form.Textbox('username',form.Validator('Unknown username.',lambda x: x in users.keys()),description='Username:'),
                        form.Password('password',description='Password:'),validators = [form.Validator("Username and password didn't match.",lambda x: users[x.username].check_password(x.password)) ])
    def GET(self):
        login= self.login()
        return render.hello(session.user, login)

    def POST(self): 
        login = self.login() 
        if not login.validates(): 
            return render.hello(session.user, login)
        else:
            session.user = login['username'].value
            return render.hello(session.user, login)


class Logout:
    def GET(self):
        session.kill()
        raise web.seeother('/')


class Register:
    register = form.Form(
	form.Textbox('firstname'),
	form.Textbox('lastname'),
	form.Textbox('phone'),
    form.Textbox('email'),
	form.Textbox('username'),
	form.Password('password'),
	form.Button('Register'),
	)

    def GET(self):
        register = self.register()
        return render.signup(register)

    def POST(self):
        register = self.register()
        if not register.validates():            
			return "Unsuccessful"
        fn=register.d.firstname
        ln=register.d.lastname
        ph=register.d.phone
        eml=register.d.email
        un=register.d.username
        pwd1=PasswordHash(register.d.password)
        s = model.new_user(fn,ln,ph,eml,un)
        return s
        


if __name__ == "__main__":
    app.run()
