import functools

from flask import (
		Blueprint, 
		flash,
		g,
		redirect, 
		render_template,
		request,
		session,
		url_for
		)
	

bp = Blueprint('data_import', __name__, url_prefix = '/')

@bp.route('/', methods = ('GET', 'POST'))
def import_data():
	if request.method =='POST':
		dat = request.form['data']
		
		error = None
		
		if not dat: 
			error = 'Please input data.'
		if error is None:
			session['dat']=dat
			return redirect(url_for('data_import.view_results'))
		flash(error)
	return render_template('data_import.html') 
	
	
	
@bp.route('/view_results', methods = ('GET',))
def view_results():
	if session.get('dat'):
		from pandas import DataFrame, read_csv
		error = None
		from . import linear_modeling_engine
		from io import StringIO
		

		csv_like_input_str = session['dat'] 
		del session['dat']
		
		
		coef = linear_modeling_engine.call_r(csv_like_input_str)
		
		cc = []
		
		for i in coef:
			cc.append(i)
		
		return render_template('view_results.html', coef=cc)
		
	else:
		return redirect(url_for('data_import.import_data'))

	
'''
12,14,15,2
0,7,4,2
12,5,5,5
1,2,3,4


'''
	
