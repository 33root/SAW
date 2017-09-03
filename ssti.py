import flask
import base64
import jinja2
from flask import render_template, request

app = flask.Flask(__name__)


@app.route("/contacto", methods=['GET'])
def hello():

    decodedUsername = ''
    if 'username' in flask.request.cookies:
        decodedUsername = base64.b64decode(flask.request.cookies['username'])

    emailMessage = ''
    decodedTemplate = ''
    error = None
    if 'template' in flask.request.cookies:
        decodedTemplate = base64.b64decode(flask.request.cookies['template'])
        try:
            emailMessage = app.jinja_env.from_string(
                decodedTemplate).render(username=decodedUsername)
        except jinja2.TemplateSyntaxError as e:
            error = 'Error: ' + str(e)

    return flask.render_template('index.html',
                                 username=decodedUsername,
                                 template=decodedTemplate,
                                 emailMessage=emailMessage,
                                 error=error)


@app.route("/", methods=['GET'])
def limpiar():
    response = app.make_response(flask.redirect('/contacto'))
    response.set_cookie('template', '')
    response.set_cookie('username', '')
    return response


@app.route("/contacto/updateUsername", methods=['POST'])
def updateUsername():
    response = app.make_response(flask.redirect('/contacto'))
    response.set_cookie('username', base64.b64encode(
        flask.request.form['username']))
    return response


@app.errorhandler(404)
def page_not_found(error):
    return render_template('pages-404.html'), 404


@app.route('/perfil', methods=['GET', 'POST'])
def perfil():
    decodedUsername = ''
    if 'username' in flask.request.cookies:
        decodedUsername = base64.b64decode(flask.request.cookies['username'])

    decodedTemplate = ''
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
        decodedUsername = ''
        if 'username' in flask.request.cookies:
            decodedUsername = base64.b64decode(
                flask.request.cookies['username'])

        decodedTemplate = ''
        error = None

    return flask.render_template('pages-profile.html',
                                 username=decodedUsername,
                                 template=decodedTemplate,
                                 error=error)


@app.route("/perfil/settings_update", methods=['POST'])
def settings_update():
    username = str(request.values.get('username'))

    # SSTI VULNERABILITY
    # The vulnerability is introduced concatenating the
    # user-provided `name` variable to the template string.
    output = Jinja2.from_string('Hello ' + username + '!').render()

    # Instead, the variable should be passed to the template context.
    # Jinja2.from_string('Hello {{name}}!').render(name = name)

    # response = app.make_response(flask.redirect('/perfil'))
    # response.set_cookie('username', base64.b64encode(
    #    flask.request.form['username']))
    return output


if __name__ == "__main__":
    app.run(port=8085)
