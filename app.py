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


model_label = joblib.load('model_label')
model_type = joblib.load('model_type')

class Predict(Resource):

    def clean_text(text):
        text = text.lower()
        text = re.sub(r"(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)|^rt|http.+?", "", text)
        return text

    def getReviewKeyWords(review):
        sentenses = review.split(".")
        sentenses = [sentense for sentense in sentenses if sentense]
        sentenses = [sentense.lower() for sentense in sentenses]
        sentenses = [sentense.strip('\'"?,.') for sentense in sentenses]
        sentenses = [sentense.strip() for sentense in sentenses]

        stop_words = get_stop_words('en')
        meaningful_words = [w for w in sentenses if not w in stop_words]

        categories = ["Negative", "Positive"]
        review_result = int(model_label.predict(pd.Series(review))[0])
        reviewSentenseResult = []

        for sentense in meaningful_words:
            sentense_result = int(model_label.predict(pd.Series(sentense))[0])
            reviewType = int(model_type.predict(pd.Series(sentense))[0]) - 1

            reviewTypeList = ["Food", "Service", "Ambience", "Other"]
            reviewSentenseResult.append({"sentense": sentense, "review": categories[sentense_result], "reviewType": reviewTypeList[reviewType]})

        return {"prediction": categories[review_result], "sentenses": reviewSentenseResult}

    @staticmethod
    def post():
        parser = reqparse.RequestParser()
        parser.add_argument('review')
        
        requestBody = parser.parse_args() 
        result = Predict.getReviewKeyWords(requestBody.review)
        out = {'Prediction': result['prediction'], "Keys": result['sentenses']}

        return out, 200

class Search(Resource):

    def findReviewsWithGivenKeyword(search):
        dataframe = pd.read_csv('data_cleaned.csv')
        dataframeReviews = dataframe['review_text']
        dataframeReviews = dataframeReviews.tolist()

        dataframeReviews = [review.lower() for review in dataframeReviews]
        search = search.lower()
        print(search)
        
        reviews = []

        for review in dataframeReviews:
            reviewCopy = review
            stop_words = get_stop_words('en')
            review = [w for w in review.split() if not w in stop_words]
            review = [w.strip('\'"?,.') for w in review]
            review = [w.strip() for w in review]

            if search in review:
                # reviews.append(reviewCopy)
                sentenses = reviewCopy.split(".")
                sentensesWithKeyword = []

                for sentense in sentenses:
                    if search in sentense:
                        result = Predict.getReviewKeyWords(sentense)
                        sentensesWithKeyword.append({ "sentense": sentense, "prediction": result['prediction'], "keys": result['sentenses']})

                ketResults_ = []
                for review_ in sentensesWithKeyword:
                    ketResults_.append(review_['keys'])
                reviews.append(ketResults_[0][0])

        return reviews

        
    def get(self, search):
        reviews = Search.findReviewsWithGivenKeyword(search)
        return reviews, 200


API.add_resource(Predict, '/predict')
API.add_resource(Search, '/review/<string:search>')

if __name__ == '__main__':
    APP.run(debug=True)