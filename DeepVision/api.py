import random

from flask import Flask, request, render_template, send_file
from flask_cors import CORS
from git import Repo
import CodeAnalyzing.complexity as c
import CodeAnalyzing.readability as r
import Visualization.visualization as v
import json
import torch
from Chatbot.model_class import NeuralNet
from Chatbot.nltk_utils import tokenize, bag_of_words
from Similarity import Jaccard
import Similarity.summary as s
import os
import shutil

repo_dir = 'GitDownloads'

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

with open('Chatbot/intents.json', 'r') as json_data:
    intents = json.load(json_data)

FILE = "Chatbot/last_model.pth"
data = torch.load(FILE)

input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data['all_words']
tags = data['tags']
model_state = data["model_state"]

chat_history = []

model = NeuralNet(input_size, hidden_size, output_size).to(device)
model.load_state_dict(model_state)
model.eval()

bot_name = "Bot"

app = Flask(__name__)
CORS(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/complexity')
def complexity():
    complexity_list = c.getComplexity()
    total = 0
    complexity_score = 0
    for i in complexity_list:
        total += i
    if total < 20:
        complexity_score = 20
    elif total < 30:
        complexity_score = 30
    elif total < 40:
        complexity_score = 40
    elif total < 50:
        complexity_score = 50
    elif total < 60:
        complexity_score = 60
    elif total < 70:
        complexity_score = 70
    elif total < 80:
        complexity_score = 80
    elif total < 90:
        complexity_score = 90
    else:
        complexity_score = 95
    print(complexity_list)
    return render_template('complexity.html', data=complexity_list, complexity_score=complexity_score)


@app.route('/readability')
def readability():
    readability_score = r.getReadablility()
    print(readability_score)
    return render_template('readability.html', data=readability_score)


@app.route('/visualization')
def visualization():
    # print(json.dumps(path_to_dict('GitDownloads')))
    x = []
    x = v.visualize()
    print('called')
    data = json.loads("[" + str(path_to_dict('GitDownloads')).replace("'", '"') + "]")
    # print(data)

    for d in data:
        print(d)

    with open('static/js/data.json', 'w') as f:
        json.dump(data, f)
    return render_template('visualization.html', data=x)


@app.route('/chat_bot')
def chat_bot():
    return render_template('chat_bot.html')


@app.route('/similarity', methods=['GET', 'POST'])
def similarity():
    if request.method == 'POST':
        first_file = request.files['file1']
        second_file = request.files['file2']
        first_file.save('Similarity/upload/' + 'first_file.java')
        second_file.save('Similarity/upload/' + 'second_file.java')
        similarity_score = Jaccard.get_similarity()
        similarity_score = round((similarity_score * 100), 2)
        return render_template('similarity.html', data=similarity_score)
    else:
        return render_template('similarity.html')


@app.route('/summary', methods=['GET', 'POST'])
def summary():
    return render_template('similarity.html', sum=s.get_summary())


@app.route('/chat', methods=['GET', 'POST'])
def chat():
    if request.method == 'POST':
        msg = request.form['msg']
        chat_history.append('You : ' + msg)
        sentence = tokenize(msg)
        X = bag_of_words(sentence, all_words)
        X = X.reshape(1, X.shape[0])
        X = torch.from_numpy(X).to(device)

        output = model(X)
        _, predicted = torch.max(output, dim=1)

        tag = tags[predicted.item()]

        probs = torch.softmax(output, dim=1)
        prob = probs[0][predicted.item()]
        if prob.item() > 0.75:
            for intent in intents['intents']:
                if tag == intent["tag"]:
                    response_ = str(random.choice(intent['responses']))
                    if response_ == 'complexity':
                        complexity_list = c.getComplexity()
                        total = 0
                        complexity_score = 0
                        for i in complexity_list:
                            total += i
                        if total < 20:
                            complexity_score = 20
                        elif total < 30:
                            complexity_score = 30
                        elif total < 40:
                            complexity_score = 40
                        elif total < 50:
                            complexity_score = 50
                        elif total < 60:
                            complexity_score = 60
                        elif total < 70:
                            complexity_score = 70
                        elif total < 80:
                            complexity_score = 80
                        elif total < 90:
                            complexity_score = 90
                        else:
                            complexity_score = 95
                        response_ = "Complexity Score - " + str(complexity_score)
                        return_str = "Friday :- " + response_
                        print('complexity')
                    elif response_ == 'readability':
                        readability_score = r.getReadablility()
                        return_str = "Friday :- Readability Score - " + str(readability_score)
                        print('readability')
                    elif response_ == 'content_of_file':
                        return_str = "Friday :- " + r.content_of_file()
                        print('content_of_file')
                    elif response_ == 'summary':
                        return_str = "Friday :- " + s.get_summary()[0]
                        print('summary')
                    else:
                        return_str = "Friday :- " + response_
                    return render_template('chat_bot.html', data=return_str)
        else:
            # print(f"{bot_name}: I do not understand...")
            return_str = "Bot :- Sorry, I do not understand"
            return render_template('chat_bot.html', data=return_str)
    return_str = "Please use post method"
    return render_template('chat_bot.html', data=return_str)


@app.route('/git_download', methods=['GET', 'POST'])
def git_download():
    if os.path.isdir(repo_dir):
        deleteGit()
    git_url = request.form['git_url']

    try:
        Repo.clone_from(git_url, repo_dir)
        delete_gitignore()
    except:
        print("Error...")
        return render_template('index.html', data='Git did not download')
    return render_template('home.html')


def deleteGit():
    try:
        shutil.rmtree(repo_dir)
    except OSError as e:
        os.chmod(e.filename, 0o777)
        print("Error: %s - %s." % (e.filename, e.strerror))
        deleteGit()


def delete_gitignore():
    try:
        # os.remove(repo_dir + '/.gitignore')
        # os.remove(repo_dir + '/.git')
        shutil.rmtree(repo_dir + '/.git')
    except OSError as e:
        os.chmod(e.filename, 0o777)
        print("Error: %s - %s." % (e.filename, e.strerror))
        delete_gitignore()


def path_to_dict(path):
    d = {'name': os.path.basename(path)}
    if os.path.isdir(path):
        d['type'] = "directory"
        d['children'] = [path_to_dict(os.path.join(path, x)) for x in os.listdir \
            (path)]
    else:
        d['type'] = "file"
    return d


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, debug=True)
