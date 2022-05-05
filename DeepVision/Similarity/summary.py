import nltk
from nltk.corpus import stopwords
from nltk.cluster.util import cosine_distance
import numpy as np
import networkx as nx
from os import path


def read_article(filedata):
    # new edit---------------/
    # tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    # print(tokenizer.tokenize(filedata))
    # article = tokenizer.tokenize(filedata)
    # new edit---------------/

    # commented---------/
    print("before article split============", filedata);
    article = filedata.split(". ")
    # commented---------/
    print("After article split============", article);

    # print("arty",article);
    sentences = []
    # empty array
    # print("sen sen sen",sentences);

    for sentence in article:
        print("sentences before loop===== ", sentence)
        sentences.append(sentence.replace("[^a-zA-Z]", " ").split(" "))
    sentences.pop()
    print("sentences after loop===== ", sentences)
    # print(len(sentences))
    return sentences


def sentence_similarity(sent1, sent2, stopwords=None):
    if stopwords is None:
        stopwords = []

    sent1 = [w.lower() for w in sent1]
    sent2 = [w.lower() for w in sent2]
    # print("sen1 :::::",sent1)
    # print("sen2s :::::",sent2)
    all_words = list(set(sent1 + sent2))
    print("alllllllllllllllz", all_words)
    vector1 = [0] * len(all_words)
    # print("vec1",vector1)
    vector2 = [0] * len(all_words)

    # build the vector for the first sentence
    for w in sent1:
        print("sent1", sent1);
        if w in stopwords:
            continue
        vector1[all_words.index(w)] += 1

    # build the vector for the second sentence
    for w in sent2:
        print("sent2", sent2);
        if w in stopwords:
            continue
        vector2[all_words.index(w)] += 1

    return 1 - cosine_distance(vector1, vector2)


def build_similarity_matrix(sentences, stop_words):
    # Create an empty similarity matrix
    # print(len(sentences)); number of sentences 11
    similarity_matrix = np.zeros((len(sentences), len(sentences)))
    print("similarity_matrix================ \n", similarity_matrix);
    # range means 0 1 2 3 4 5 6 7 8 9 10 11
    for idx1 in range(len(sentences)):
        for idx2 in range(len(sentences)):
            if idx1 == idx2:  # ignore if both are same sentences
                continue
            similarity_matrix[idx1][idx2] = sentence_similarity(sentences[idx1], sentences[idx2], stop_words)
    print("similarity_matrix")
    print(similarity_matrix)
    return similarity_matrix


def generate_summary(file_name, top_n=1):
    nltk.download("stopwords")
    stop_words = stopwords.words('english')
    # print(stop_words);
    summarize_text = []

    # Step 1 - Read text anc split it
    sentences = read_article(file_name)
    # print("function articles",sentences)
    # Step 2 - Generate Similary Martix across sentences
    sentence_similarity_martix = build_similarity_matrix(sentences, stop_words)

    # Step 3 - Rank sentences in similarity martix
    sentence_similarity_graph = nx.from_numpy_array(sentence_similarity_martix)
    # print("dshfsdjhf sjdhdfbhsdf",sentence_similarity_graph,"uhjhjh")

    scores = nx.pagerank(sentence_similarity_graph)
    print("scores", scores)
    # print("score :  ",scores);
    # for i,s in enumerate(sentences):
    #     print(i);
    #     print(s);

    # Step 4 - Sort the rank and pick top sentences
    ranked_sentence = sorted(((scores[i], s) for i, s in enumerate(sentences)), reverse=True)
    # print("Indexes of top ranked_sentence order are ", ranked_sentence)

    for i in range(top_n):
        summarize_text.append(" ".join(ranked_sentence[i][1]))

    # Step 5 - Offcourse, output the summarize texr
    # print("Summarize Text: \n", ". ".join(summarize_text))
    # print( ". ".join(summarize_text))
    x = ". ".join(summarize_text)
    print(x)
    return summarize_text


def get_summary():
    filename = 'GitDownloads/README.md'
    string_value = ''
    if path.isfile(filename):
        with open(filename) as file:
            for line in file:
                string_value = string_value + ' ' + line.rstrip()
        print('final sum')
        return generate_summary(string_value)
    else:
        return 'README.md file not found in given GIT Repo'


