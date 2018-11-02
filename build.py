from flask import Flask, request, render_template, send_file, send_from_directory
from getpass import getuser
from flask_socketio import SocketIO, emit, disconnect
#from threading import Lock
import os

from myfunc import *

async_mode = None

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret"
socketio = SocketIO(app, async_mode=async_mode)
connection = 0
messagelist = []

osusername = getuser()
buildpdir = "/home/" + osusername + "/work/"
builddir = buildpdir + "flexbuild/"

'''
thread = None
thread_lock = Lock()
def background_thread():
    """Example of how to send server generated events to clients."""
    while True:
        socketio.sleep(10)
        socketio.emit('keep_connect',
                      {'data': 'Server generated event'},
                      namespace='/test')
'''

def sendmessage(message):
    if connection == 1:
        emit("my_response", {"data": message})
    else:
        messagelist.append(message)

@app.route("/")
def home():
    return render_template('form.html', async_mode=socketio.async_mode)

@app.route("/download/<filename>", methods = ['GET'])
def download_file(filename):
    directory = os.getcwd() + "/download"
    return send_from_directory(directory, filename, as_attachment=True)

@socketio.on('build', namespace='/test')
def build(message):
    machine = message['data'].strip()
    print machine
    if ('ls1043ardb' in machine):
        if not os.path.exists(builddir):
            emit("my_response", {"data": "Starting clone..."})
            os.chdir(buildpdir)
            os.system("git clone ssh://git@bitbucket.sw.nxp.com/dash/flexbuild.git")
            emit("my_response", {"data": "Finish clone..."})
        emit("my_response", {"data": "Starting build %s, will take a long time..." % machine})
        os.chdir(builddir)
        enEdge()
        command = "source ./setup.env && flex-builder -m ls1043ardb -a arm64"
        os.system(command)
        mksolution()
        print "=============connection = %d" % connection
        sendmessage("Finish build...")
    else:
        emit("my_response", {"data": "Doesn't support machine %s" % machine})

@socketio.on('deploy', namespace='/test')
def deploy(message):
    emit('my_response', {'data': 'Starting deploy...'})
    command = "escli  login --username alison\.wang@nxp.com --password 12345678"
    os.system(command)
    command = "escli task deploy-solution --device_id 1315 --id 502"
    os.system(command)
    emit('my_response', {'data': 'Deploy finished...'})

@socketio.on('my_event', namespace='/test')
def test_connect(message):
    print message['data']

@socketio.on('connect', namespace='/test')
def test_connect():
    '''
    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(target=background_thread)
    '''
    connection = 1
    emit('my_response', {'data': 'Connected to Server!'})
    while (len(messagelist) != 0):
        emit('my_response', {'data': messagelist.pop(0)})


@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    connection = 0
    print('Client disconnected', request.sid)

if __name__ == '__main__':
    #app.run(debug=True, host="0.0.0.0")
    socketio.run(app,debug=True,host='0.0.0.0',port=5000)
