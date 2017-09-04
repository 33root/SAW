import flask
import base64
import jinja2
from flask import render_template, request

app = flask.Flask(__name__)


@app.route("/index", methods=['GET'])
def hello():

    decodedUsername = ''
    if 'username' in flask.request.cookies:
        decodedUsername = base64.b64decode(flask.request.cookies['username'])

    error = None
    
    return flask.render_template('index.html',
                                 username=decodedUsername,
                                 error=error)

@app.route("/", methods=['GET'])
def limpiar():
    response = app.make_response(flask.redirect('/index'))
    response.set_cookie('username', base64.b64encode('jdoe'))
    return response

@app.errorhandler(404)
def page_not_found(error):
    return render_template('pages-404.html'), 404

@app.errorhandler(500)
def page_internal_error(error):
    return render_template('pages-500.html'), 500

@app.route('/perfil', methods=['GET', 'POST'])
def perfil():
    decodedUsername = ''
    if 'username' in flask.request.cookies:
        decodedUsername = base64.b64decode(flask.request.cookies['username'])

    error = None
    if request.method == 'POST':
        pass
        # if request.form['username'] != 'admin' or \
        #         request.form['password'] != 'secret':
        #     error = 'Invalid credentials'
        # else:
        #     flash('You were successfully logged in')
        #     return redirect(url_for('index'))
    else:
		try:
			user = app.jinja_env.from_string(decodedUsername).render(username = decodedUsername)

		except jinja2.TemplateSyntaxError as e:
			error = 'Error: ' + str(e)

    return flask.render_template('pages-profile.html',
                                 username=user,
                                 error=error)


@app.route("/perfil/settings_update", methods=['POST'])
def settings_update():
    # username = str(request.values.get('username'))

    # SSTI VULNERABILITY
    # The vulnerability is introduced concatenating the
    # user-provided `name` variable to the template string.
    ##output = Jinja2.from_string('Hello ' + username + '!').render()

    # Instead, the variable should be passed to the template context.
    # Jinja2.from_string('Hello {{name}}!').render(name = name)
    response = app.make_response(flask.redirect('/perfil'))
    response.set_cookie('username', base64.b64encode(
        flask.request.form['username']))
    return response

if __name__ == "__main__":
    app.run(port=8085)
