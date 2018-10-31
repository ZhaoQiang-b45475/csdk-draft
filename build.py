from flask import Flask
from flask import request
from flask import render_template
from flask import send_file
from flask import send_from_directory
from getpass import getuser
import os

from myfunc import *

app = Flask(__name__)
osusername = getuser()
buildpdir = "/home/" + osusername + "/work/"
builddir = buildpdir + "flexbuild/"

@app.route("/", methods = ['GET'])
def home():
    return render_template('form.html')

@app.route("/download/<filename>", methods = ['GET'])
def download_file(filename):
    directory = os.getcwd() + "/download"
    return send_from_directory(directory, filename, as_attachment=True)

@app.route("/build", methods = ['POST'])
def build():
    machine = request.form['machine']
    if not os.path.exists(builddir):
        os.chdir(buildpdir)
        os.system("git clone ssh://git@bitbucket.sw.nxp.com/dash/flexbuild.git")
    os.chdir(builddir)
    enEdge()
    os.system("source ./setup.env && flex-builder all")
    return render_template('form.html')

@app.route("/deploy", methods = ['GET'])
def deploy():
    mksolution()
    command = "escli task deploy-solution --device_id 1315 --id 502"
    os.system(command)
    return render_template('form.html')

if __name__ == '__main__':
	app.run(debug=True, host="0.0.0.0")
