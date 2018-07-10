'''
Creates a function which, given a Pandas DataFrame, calls an R script and 
returns the coefficients of a linear model. 
'''


def call_r(df):
	'''
	Arguments:
	df: A string replicating a CSV file. The observations for the dependent
		variable MUST be in the FIRST COLUMN

	Returns: an rpy2 Robject float vector which stores the coefficients of the
	linear regression
	'''
	from rpy2.robjects.packages import SignatureTranslatedAnonymousPackage
	from io import StringIO
	from rpy2.robjects import DataFrame
	from rpy2.robjects import FloatVector
	file_like_obj = StringIO(df)
	constructor_dict = parser(file_like_obj)
	rpy2_dataframe = DataFrame(constructor_dict)
	with open('regression_app\linear_modeler_function.R') as f:
		str = f.read()
	mod = SignatureTranslatedAnonymousPackage(str, 'mod')
	a = mod.linear_modeler(rpy2_dataframe)
	del mod 
	return a
	

def parser(flo):
    s = flo.readline()
    counter = 0
    dd = {}
    while s != '':
        dd[counter] = line_to_list(s)
        counter += 1
        s = flo.readline()
    dd =  dict_to_numeric(dd)
    return dict_to_robject(dd)


def line_to_list(s):
    s = s.strip()
    t = s.split(',')
    return t


def dict_to_numeric(dd):
    for (k,v) in dd.items():
        vt = ()
        for i in v:
            vt += (float(i),)
        dd[k] = vt
        #v = tuple(v)
    return dd    

def dict_to_robject(dd):
	from rpy2.robjects import FloatVector
	for (k,v) in dd.items():
		a = FloatVector(v)
		dd[k] = a
	return dd




############ Unused Code Below #############

	
def second_call_r(df):
	import rpy2.robjects
	from rpy2.robjects import pandas2ri
	from rpy2.robjects.packages import importr
	stats = importr('stats')
	base = importr('base')
	pandas2ri.activate()
	rpy2.robjects.globalenv['dataframe'] = df
	m = stats.lm('dataframe', data=base.as_symbol('dataframe'))
	return m
