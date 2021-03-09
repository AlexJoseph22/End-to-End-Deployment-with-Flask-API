import flask
from flask import request
app = flask.Flask(__name__)
app.config['DEBUG'] = True

from flask_cors import CORS
CORS(app)

@app.route("/", methods=['GET'])
def default():
    return '''Get yourself checked to see whether you have bladder inflammation and nephritis or neither'''

@app.route("/predict", methods=['GET'])
def predict():
    import joblib
    model_inflam = joblib.load("model_inflam.pkl")
    model_neph = joblib.load("model_neph.pkl")
    inflammation = model_inflam.predict([[int(request.args['temp']),
                                          int(request.args['nausea']),
                                          int(request.args['lumbar']),
                                          int(request.args['urinepush']),
                                          int(request.args['micturition']),
                                          int(request.args['urethraburn'])]])[0]
    
    nephritis = model_neph.predict([[int(request.args['temp']),
                                          int(request.args['nausea']),
                                          int(request.args['lumbar']),
                                          int(request.args['urinepush']),
                                          int(request.args['micturition']),
                                          int(request.args['urethraburn'])]])[0]
    
    if (inflammation == 1) and (nephritis == 1):
        return '''You have both bladder inflammation and nephritis'''
    elif (inflammation == 1) and (nephritis == 0):
        return '''You have bladder inflammation'''
    elif (inflammation == 0) and (nephritis == 1):
        return '''You have nephritis'''
    else:
        return '''You neither have bladder inflammation nor nephritis'''
    

app.run()