from flask import Flask
from flask import request
from flask import render_template
import os
from getpass import getuser

app = Flask(__name__)
osusername = getuser()
buildpdir = "/home/" + osusername + "/work/"
builddir = buildpdir + "flexbuild/"

@app.route("/", methods = ['GET'])
def home():
	return render_template('form.html')

@app.route("/build", methods = ['POST'])
def build():
	machine = request.form['machine']
	if not os.path.exists(builddir):
		os.chdir(buildpdir)
		os.system("git clone ssh://git@bitbucket.sw.nxp.com/dash/flexbuild.git")
	os.chdir(builddir)
	os.system("source ./setup.env && flex-builder all")
	return "clone success"

if __name__ == '__main__':
	app.run(debug=True, host="0.0.0.0")
