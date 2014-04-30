from sqlalchemy import Column, Integer, Text, DateTime
from flask import Flask, request, jsonify, send_file
from flask.ext.sqlalchemy import SQLAlchemy
from etl import intake
import cStringIO
import datetime
import json
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///capitaldb.db'
db = SQLAlchemy(app)

class Forms(db.Model):
	pid = Column(Integer, primary_key=True)
	version = Column(Text, primary_key=True, unique=False)
	#reporting_period = Column(DateTime, primary_key=True, unique=False) #TODO, add this PK
	file_title = Column(Text, unique=False)
	date_upload = Column(DateTime, unique=False)

	def to_json(self):
		return {"pid":self.pid, "version":self.version, "file_title":self.file_title, "date_upload":self.date_upload}

# db.drop_all()
# db.create_all()
# #manually prepolulate db with an intake form
# db.session.add(Forms(pid=999, version="intake", file_title="Big Bridge.xlsx", date_upload=datetime.datetime.now()))
# db.session.add(Forms(pid=888, version="intake", file_title="Bumpy Road.xlsx", date_upload=datetime.datetime.now()))
# db.session.commit()

def get_or_create_record(session, model, pk, all_data):
	"""check if the primary key(s) exist, if yes, overwrite with all_data, 
		otherwise create row with all_data """
	instance = session.query(model).filter_by(**pk).first()
	if instance:
		session.query(model).filter_by(**pk).update(all_data)
	else:
		session.add(model(**all_data))
	db.session.commit()

@app.route('/')
def root():
    return app.send_static_file('index.html')

@app.route('/api/upload/<version>', methods = ['POST'])
def upload(version=None):
	theFile = request.files['upFile']
	file_like = cStringIO.StringIO(theFile.read())
	xl_data = intake.getData(file_like)
	data = {}
	data['pid'] = xl_data['pid']
	data['date_upload'] = datetime.datetime.now()
	data['file_title'] = theFile.filename 
	data['version'] = request.form['version']
	save_path = 'forms/'+data['version']+'/'+str(data['pid'])
	with open(save_path, 'wb') as f:
		f.write(file_like.getvalue()) #TODO: rollback mechanism 1/2
	file_like.close() #Q: How to make sure this closes if error before this line?
	get_or_create_record(db.session, Forms, {'pid':data['pid'], 'version':data['version']}, data) #TODO: rollback mechanism 2/2
	return jsonify(xl_data)

@app.route('/api/downloadables', methods = ['GET'])
def downloadables():
	result = db.session.query(Forms).all()
	return jsonify({"forms":[row.to_json() for row in result]})

@app.route('/forms/<version>/<pid>', methods = ['GET'])
def download(version, pid):
	result = db.session.query(Forms).filter_by(version=version, pid=pid).first() #TODO: check only one result exists?
	return send_file(os.path.join('forms',version,pid), as_attachment=True, attachment_filename=result.file_title)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)


