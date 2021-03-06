from flask import Flask, request, render_template, send_file, send_from_directory
from getpass import getuser
from flask_socketio import SocketIO, emit, disconnect
from threading import Lock
import os
import fcntl

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
buildconf = "buildconf"
csdkdir = os.getcwd()

thread = None
thread_lock = Lock()

def background_thread():
    while True:
        socketio.sleep(5)
        if readstrfromfile(csdkdir+"/"+buildconf, "EDGEBUILD=3"):
            socketio.emit("my_response", {"data": "Build failed..."}, namespace='/test')
            modifyfile(csdkdir+"/"+buildconf, "EDGEBUILD=3", "EDGEBUILD=0")
        elif readstrfromfile(csdkdir+"/"+buildconf, "EDGEBUILD=4"):
            socketio.emit("my_response", {"data": "Build success..."},namespace='/test')
            modifyfile(csdkdir+"/"+buildconf, "EDGEBUILD=4", "EDGEBUILD=0")

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
        if readstrfromfile(buildconf, "EDGEBUILD=0"):
            emit("my_response", {"data": "Start to build %s, Maybe take a long time..." % machine})
            modifyfile(buildconf, "EDGEBUILD=0", "EDGEBUILD=1")
    else:
        emit("my_response", {"data": "Doesn't support machine %s" % machine})

@socketio.on('deploy', namespace='/test')
def deploy(message):
    emit('my_response', {'data': 'Starting deploy...'})
    command = "escli  login --username alison\.wang@nxp.com --password 12345678"
    os.system(command)
    command = "escli task deploy-solution --device_id 1315 --id 502"
    os.system(command)

@socketio.on('my_event', namespace='/test')
def test_connect(message):
    print message['data']

@socketio.on('connect', namespace='/test')
def test_connect():
    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(target=background_thread)
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
