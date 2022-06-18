import joblib
import pandas as pd
import re
from stop_words import get_stop_words

from flask import Flask
from flask_cors import CORS
from flask_restful import Api, Resource, reqparse

APP = Flask(__name__)
APP.config['CORS_HEADERS'] = 'Content-Type'
CORS(APP)
API = Api(APP)


model = joblib.load('model')

class Predict(Resource):

    def clean_text(text):
        text = text.lower()
        text = re.sub(r"(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)|^rt|http.+?", "", text)
        return text

    def getReviewKeyWords(text):
        stop_words = get_stop_words('en')
        text = Predict.clean_text(text)
        text = text.split()
        text = [word for word in text if word not in stop_words]
        return text

    @staticmethod
    def post():
        parser = reqparse.RequestParser()
        parser.add_argument('review')
        
        requestBody = parser.parse_args()  # creates dictionary

        categories = ["Negative", "Positive"]
        result = int(model.predict(pd.Series(requestBody.review))[0])

        keyWords = Predict.getReviewKeyWords(requestBody.review)
        print("keyWords", str(keyWords))
        out = {'Prediction': categories[result], "KeyWords": keyWords}

        return out, 200


API.add_resource(Predict, '/predict')

if __name__ == '__main__':
    APP.run(debug=True)