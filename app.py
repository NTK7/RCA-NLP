from unittest import result
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

    # def getReviewKeyWords(text):
    #     words = text.split()
    #     words = [word.lower() for word in words]
    #     words = [word.strip('\'"?,.') for word in words]

    #     stop_words = get_stop_words('en')
    #     meaningful_words = [w for w in words if not w in stop_words]

    #     categories = ["Negative", "Positive"]
    #     review = int(model.predict(pd.Series(text))[0])
    #     reviewKeyWordResult = []

    #     for word in meaningful_words:
    #         keywordReview = int(model.predict(pd.Series(word))[0])
    #         reviewKeyWordResult.append({"keyword": word, "review": categories[keywordReview]})
        
    #     return {"prediction": categories[review], "keywords": reviewKeyWordResult}

    def getReviewKeyWords(review):
        sentenses = review.split(".")
        # remove items from the sentenses list that are empty such as ""
        sentenses = [sentense for sentense in sentenses if sentense]
        sentenses = [sentense.lower() for sentense in sentenses]
        sentenses = [sentense.strip('\'"?,.') for sentense in sentenses]
        sentenses = [sentense.strip() for sentense in sentenses]

        stop_words = get_stop_words('en')
        meaningful_words = [w for w in sentenses if not w in stop_words]

        categories = ["Negative", "Positive"]
        review_result = int(model.predict(pd.Series(review))[0])
        reviewSentenseResult = []

        for sentense in meaningful_words:
            sentense_result = int(model.predict(pd.Series(sentense))[0])
            reviewSentenseResult.append({"sentense": sentense, "review": categories[sentense_result]})

        return {"prediction": categories[review_result], "sentenses": reviewSentenseResult}

    @staticmethod
    def post():
        parser = reqparse.RequestParser()
        parser.add_argument('review')
        
        requestBody = parser.parse_args() 
        result = Predict.getReviewKeyWords(requestBody.review)
        out = {'Prediction': result['prediction'], "Keys": result['sentenses']}

        return out, 200


API.add_resource(Predict, '/predict')

if __name__ == '__main__':
    APP.run(debug=True)