import numpy as np
import pandas as pd
import re
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from flask import Flask, request, url_for, redirect, render_template
from flask_cors import CORS
from statsmodels.tsa.arima_model import ARIMAResults
from datetime import datetime, timedelta
import pandas as pd
import json
import os
import joblib
import nltk
nltk.download('stopwords')

app = Flask(__name__)
CORS(app)

model = joblib.load('model')
stem_wrd = PorterStemmer()
vect = CountVectorizer()
tfidf_trans = TfidfTransformer()


nltk.download('stopwords')

print(stopwords.words('english'))

subject_data = pd.read_csv('data/sample_data.csv')
subject_data

subject_data.isnull().sum()

f_X = subject_data['Lecture content ']
f_X

Y = subject_data['Subject']
Y

stem_wrd = PorterStemmer()


def stemm(content):
    stem_feature = re.sub('[^a-zA-Z]', ' ', content)
    stem_feature = stem_feature.lower()
    stem_feature = stem_feature.split()
    stem_feature = [stem_wrd.stem(word) for word in stem_feature if not word in stopwords.words('english')]
    stem_feature = ' '.join(stem_feature)
    return stem_feature


Y_new = f_X.apply(stemm)
# X_new = X.values
# Y_new = Y.values

vect = CountVectorizer()
features_tf = vect.fit_transform(Y_new)
# print(vect.vocabulary_)
# print(features_tf.shape)
# c = features.toarray()
# print (features_tf.toarray())
# features.shape

tfidf_trans = TfidfTransformer()
features = tfidf_trans.fit_transform(features_tf)

lbl = LabelEncoder()
label = lbl.fit_transform(Y_new)
label

X_train, x_test, Y_train, y_test = train_test_split(features, label, test_size=0.2, random_state=2)
print(X_train)
print('#################################################################')
print(x_test)

model = MultinomialNB()
model.fit(X_train, Y_train)

print(X_train[2])
print(y_test[1])

stem_wrd1 = PorterStemmer()


@app.route('/subject', methods=['GET', 'POST'])
def subject():
    input = request.json['input']

    stem_feature = stemm(input)
    wrd = "A collection of devices and circuits for transferring data from one computer to another"
    stem_feature1 = re.sub('[^a-zA-Z]', ' ', wrd)
    stem_feature1 = stem_feature1.lower()
    stem_feature1 = stem_feature1.split()
    stem_feature1 = [stem_wrd1.stem(word) for word in stem_feature1 if not word in stopwords.words('english')]
    stem_feature1 = ' '.join(stem_feature1)
    # wrd_new = wrd.apply(stemm)

    test_tf = vect.transform([stem_feature1])
    test_tfidf = tfidf_trans.transform(test_tf)

    prediction = model.predict(test_tfidf)

    if prediction < 3:
        return_str = '{ "result" : "Networking Related Lecture" }'
    else:
        return_str = '{ "result" : "Software Quality assurance Related Lecture" }'

    return json.loads(return_str)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
