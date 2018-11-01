from flask import Flask
from flask import request
from flask import render_template
from flask import send_file
from flask import send_from_directory
from getpass import getuser
from flask_socketio import SocketIO, emit, disconnect
import os

from myfunc import *

async_mode = None

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret"
socketio = SocketIO(app, async_mode=async_mode)

osusername = getuser()
buildpdir = "/home/" + osusername + "/work/"
builddir = buildpdir + "flexbuild/"

@app.route("/")
def home():
    return render_template('form.html', async_mode=socketio.async_mode)

@app.route("/download/<filename>", methods = ['GET'])
def download_file(filename):
    directory = os.getcwd() + "/download"
    return send_from_directory(directory, filename, as_attachment=True)

@socketio.on('build', namespace='/test')
def build(message):
    machine = message['data']
    if not os.path.exists(builddir):
        emit("my_response", {"data": "Starting clone..."})
        os.chdir(buildpdir)
        os.system("git clone ssh://git@bitbucket.sw.nxp.com/dash/flexbuild.git")
        emit("my_response", {"data": "Finish clone..."})
    emit("my_response", {"data": "Starting build..."})
    os.chdir(builddir)
    enEdge()
    os.system("source ./setup.env && flex-builder all")
    mksolution()
    emit("my_response", {"data": "Finish build..."})

@socketio.on('deploy', namespace='/test')
def deploy(message):
    emit('my_response', {'data': 'Starting deploy...'})
    command = "escli task deploy-solution --device_id 1315 --id 502"
    os.system(command)
    emit('my_response', {'data': 'Deploy finished...'})

@socketio.on('connect', namespace='/test')
def test_connect():
    emit('my_response', {'data': 'Connected'})


@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected', request.sid)

if __name__ == '__main__':
    #app.run(debug=True, host="0.0.0.0")
    socketio.run(app,debug=True,host='0.0.0.0',port=5000)
