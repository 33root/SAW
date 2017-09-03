import flask, base64, jinja2

app = flask.Flask(__name__)

@app.route("/contacto", methods = ['GET'])
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
            emailMessage = app.jinja_env.from_string(decodedTemplate).render(username = decodedUsername)
        except jinja2.TemplateSyntaxError as e:
            error = 'Error: ' + str(e)

    return flask.render_template('hello.html', username = decodedUsername, template = decodedTemplate, emailMessage = emailMessage, error = error)

@app.route("/", methods = ['GET'])
def limpiar():
    response = app.make_response(flask.redirect('/contacto'))
    response.set_cookie('template', '')
    response.set_cookie('username', '')
    return response

@app.route("/contacto/updateUsername", methods = ['POST'])
def updateUsername():
    response = app.make_response(flask.redirect('/contacto'))
    response.set_cookie('username', base64.b64encode(flask.request.form['username']))
    return response

@app.route("/contacto/updateEmailMessage", methods = ['POST'])
def updateEmailMessage():
    response = app.make_response(flask.redirect('/contacto'))
    response.set_cookie('template', base64.b64encode(flask.request.form['template']))
    return response

if __name__ == "__main__":
    app.run(port = 8085)