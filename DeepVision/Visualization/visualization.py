import os
import re
import json

root_dir = 'GitDownloads'  # change this to correct git location
# java_file_list = []

# Regex patters
INHERITANCE_CLASS = "\\w*\\sextends\\s\\w*"
OBJECT_DICT = "(\\s+([a-zA-Z]+\\s+)+)=(\\s([new]+\\s)+)[a-zA-Z]+\\(\\);"
VARIABLE_DICT = "\\s(int|float|String|double|char|long|boolean)\\s[^\\s]*\\s"
CONTROL_STRUCTURE_JAVA_METHOD = "(public|protected|private|static|\\s) +[\\w\\<\\>\\[\\]]+\\s+(\\w+) *\\([^\\)]*\\) *(\\{?|[^;])";


def analyze(filename, java_file_content_list):
    dist = {}
    class_name = filename.split('/')[-1].replace(".java", "")
    dist["class_name"] = class_name
    inheritance_list = []
    object_list = []
    variable_list = []
    method_list = []
    for content in java_file_content_list:
        for line in content:
            class_test = re.compile(INHERITANCE_CLASS)
            object_test = re.compile(OBJECT_DICT)
            variable_test = re.compile(VARIABLE_DICT)
            method_test = re.compile(CONTROL_STRUCTURE_JAVA_METHOD)
            if class_test.search(str(line)) != None:
                inheritance_list.append(' '.join(class_test.search(str(line)).group().split()))
            if object_test.search(str(line)) != None:
                object_list.append(' '.join(object_test.search(str(line)).group().split()))
            if variable_test.search(str(line)) != None:
                variable_list.append(' '.join(variable_test.search(str(line)).group().split()))
            if method_test.search(str(line)) != None:
                method_list.append(' '.join(method_test.search(str(line)).group().split()))
    dist["inheritances"] = inheritance_list
    dist["objects"] = object_list
    dist["variables"] = variable_list
    dist["methods"] = method_list
    return dist


def visualize():

    print('called..............')
    java_file_list = []
    test = []
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith(".java"):
                java_file_list.append(os.path.join(root, file))

    for filename in java_file_list:
        java_file_content_list = []
        content = []
        with open(filename) as file:
            for line in file:
                content.append(line.rstrip())
        java_file_content_list.append(content)
        test.append(analyze(filename, java_file_content_list))

    # with open('static/js/test.json', 'w') as f:
    #     json.dump(test, f)
    return test
