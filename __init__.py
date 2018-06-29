import os
from flask import Flask

def create_app(test_config=None):
	app = Flask(__name__, instance_relative_config = True)
	app.config.from_mapping(
		SECRET_KEY = 'dev',
		DATABASE=os.path.join(app.instance_path, 'regression_app.sqlite')
	)
	
	if test_config is None:
		app.config.from_pyfile('config.py', silent = True)
	else:
		app.config.from_mapping(test_config)
	
	try:
		os.makedirs(app.instance_path)
	except OSError:
		pass
	
	@app.route('/hello')
	def hello():
		return 'Hello, World!'
	
	
	from . import data_import
	app.register_blueprint(data_import.bp)
	
	return app

if __name__ == "__main__":
	app.run()