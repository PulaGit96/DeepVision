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
import joblib
import os

import nltk

nltk.download('stopwords')


subject_data = pd.read_csv('CodeAnalyzing/data/sample_data.csv')

subject_data.isnull().sum()

f_X = subject_data['content']

Y = subject_data['Readability']

stem_wrd = PorterStemmer()


def stemm(content):
    stem_feature = re.sub('[^a-zA-Z]', ' ', content)
    stem_feature = stem_feature.lower()
    stem_feature = stem_feature.split()
    stem_feature = [stem_wrd.stem(word) for word in stem_feature if not word in stopwords.words('english')]
    stem_feature = ' '.join(stem_feature)
    return stem_feature


def read(text):
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

    X_train, x_test, Y_train, y_test = train_test_split(features, label, test_size=0.2, random_state=2)

    model = MultinomialNB()
    model.fit(X_train, Y_train)

    stem_wrd1 = PorterStemmer()

    wrd = text
    stem_feature1 = re.sub('[^a-zA-Z]', ' ', wrd)
    stem_feature1 = stem_feature1.lower()
    stem_feature1 = stem_feature1.split()
    stem_feature1 = [stem_wrd1.stem(word) for word in stem_feature1 if not word in stopwords.words('english')]
    stem_feature1 = ' '.join(stem_feature1)
    # wrd_new = wrd.apply(stemm)

    test_tf = vect.transform([stem_feature1])
    test_tfidf = tfidf_trans.transform(test_tf)

    prediction = model.predict(test_tfidf)

    joblib.dump(model, 'model')
    # model.save('model')
    print('Prediction')
    print(prediction)
    if prediction == 0:
        return 10
    elif prediction == 1:
        return 20
    elif prediction == 2:
        return 30
    elif prediction == 3:
        return 40
    elif prediction == 4:
        return 50
    elif prediction == 5:
        return 60
    elif prediction == 7:
        return 70
    elif prediction == 8:
        return 80
    else:
        return 90


# read('Acollection of devices and circuits for transferring data from one computer to another')

def getReadablility():
    root_dir = '../GitDownloads'
    java_file_list = []

    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith(".java"):
                java_file_list.append(os.path.join(root, file))
                print(os.path.join(root, file))

    java_file_content_list = []
    all_in_one_string = ''

    for filename in java_file_list:
        content = []
        with open(filename) as file:
            for line in file:
                content.append(line.rstrip())
                all_in_one_string += ' ' + line.rstrip()
        java_file_content_list.append(content)

    return read(all_in_one_string)


def content_of_file():
    root_dir = 'GitDownloads'
    java_file_list = []
    total = 0
    return_list = []

    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith(".java"):
                total += 1
                java_file_list.append(os.path.join(root, file))
    return_list.append("Total file count : " + str(total))

    for filename in java_file_list:
        with open(filename) as file:
            temp = str(filename.split("/")[-1]) + " lines count :"
            tot = 0
            for line in file:
                tot += 1
            temp += str(tot)
            return_list.append(temp)

    return_str = ''
    for i in return_list:
        return_str = return_str + i + ', '
    return return_str


# getReadablility()
# print(content_of_file())
