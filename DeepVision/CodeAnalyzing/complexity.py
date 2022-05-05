import os
import re


def getComplexity():
    root_dir = 'GitDownloads'
    java_file_list = []

    # regex patterns
    CONTROL_STRUCTURE_IF_ELSEIF = "\\s?if\\s?\\(|\\selse if\\s?\\(";
    CONTROL_STRUCTURE_FOR_WHILE_DO_WHILE = "\\s?for\\s?\\(|\\s?while\\s?\\(";
    CONTROL_STRUCTURE_FOR_SWITCH = "\\sswitch\\s?\\(";
    CONTROL_STRUCTURE_FOR_CASE = "case\\s\\w\\s?:";
    CONTROL_STRUCTURE_LOGIC_GATE = "\\|\\||&&";
    CONTROL_STRUCTURE_JAVA_METHOD = "(public|protected|private|static|\\s) +[\\w\\<\\>\\[\\]]+\\s+(\\w+) *\\([^\\)]*\\) *(\\{?|[^;])";

    CONTROL_STRUCTURE_IF_ELSEIF_ARR = []
    CONTROL_STRUCTURE_FOR_WHILE_DO_WHILE_ARR = []
    CONTROL_STRUCTURE_FOR_SWITCH_ARR = []
    CONTROL_STRUCTURE_FOR_CASE_ARR = []
    CONTROL_STRUCTURE_LOGIC_GATE_ARR = []
    CONTROL_STRUCTURE_JAVA_METHOD_ARR = []

    CONTROL_STRUCTURE_IF_ELSEIF_COUNT = 0
    CONTROL_STRUCTURE_FOR_WHILE_DO_WHILE_COUNT = 0
    CONTROL_STRUCTURE_FOR_SWITCH_COUNT = 0
    CONTROL_STRUCTURE_FOR_CASE_COUNT = 0
    CONTROL_STRUCTURE_LOGIC_GATE_COUNT = 0
    CONTROL_STRUCTURE_JAVA_METHOD_COUNT = 0
    NO_OF_LINES = 0
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith(".java"):
                java_file_list.append(os.path.join(root, file))
                print(os.path.join(root, file))

    java_file_content_list = []

    for filename in java_file_list:
        content = []
        with open(filename) as file:
            for line in file:
                content.append(line.rstrip())
        java_file_content_list.append(content)

    # print(java_file_content_list[1])

    for content in java_file_content_list:
        for line in content:
            REGEX_CONTROL_STRUCTURE_IF_ELSEIF = re.compile(CONTROL_STRUCTURE_IF_ELSEIF)
            REGEX_CONTROL_STRUCTURE_FOR_WHILE_DO_WHILE = re.compile(CONTROL_STRUCTURE_FOR_WHILE_DO_WHILE)
            REGEX_CONTROL_STRUCTURE_FOR_SWITCH = re.compile(CONTROL_STRUCTURE_FOR_SWITCH)
            REGEX_CONTROL_STRUCTURE_FOR_CASE = re.compile(CONTROL_STRUCTURE_FOR_CASE)
            REGEX_CONTROL_STRUCTURE_LOGIC_GATE = re.compile(CONTROL_STRUCTURE_LOGIC_GATE)
            REGEX_CONTROL_STRUCTURE_JAVA_METHOD = re.compile(CONTROL_STRUCTURE_JAVA_METHOD)

            if REGEX_CONTROL_STRUCTURE_IF_ELSEIF.search(str(line)) == None:
                pass
            else:
                CONTROL_STRUCTURE_IF_ELSEIF_COUNT += 1

            if REGEX_CONTROL_STRUCTURE_FOR_WHILE_DO_WHILE.search(str(line)) == None:
                pass
            else:
                CONTROL_STRUCTURE_FOR_WHILE_DO_WHILE_COUNT += 1

            if REGEX_CONTROL_STRUCTURE_FOR_SWITCH.search(str(line)) == None:
                pass
            else:
                CONTROL_STRUCTURE_FOR_SWITCH_COUNT += 1

            if REGEX_CONTROL_STRUCTURE_FOR_CASE.search(str(line)) == None:
                pass
            else:
                CONTROL_STRUCTURE_FOR_CASE_COUNT += 1

            if REGEX_CONTROL_STRUCTURE_LOGIC_GATE.search(str(line)) == None:
                pass
            else:
                CONTROL_STRUCTURE_LOGIC_GATE_COUNT += 1

            if REGEX_CONTROL_STRUCTURE_JAVA_METHOD.search(str(line)) == None:
                pass
            else:
                CONTROL_STRUCTURE_JAVA_METHOD_COUNT += 1

            # CONTROL_STRUCTURE_IF_ELSEIF_COUNT += REGEX_CONTROL_STRUCTURE_IF_ELSEIF.search(str(line))
            # CONTROL_STRUCTURE_FOR_WHILE_DO_WHILE_COUNT += REGEX_CONTROL_STRUCTURE_FOR_WHILE_DO_WHILE.search(str(line))
            # CONTROL_STRUCTURE_FOR_SWITCH_COUNT += REGEX_CONTROL_STRUCTURE_FOR_SWITCH.search(str(line))
            # CONTROL_STRUCTURE_FOR_CASE_COUNT += REGEX_CONTROL_STRUCTURE_FOR_CASE.search(str(line))
            # CONTROL_STRUCTURE_LOGIC_GATE_COUNT += REGEX_CONTROL_STRUCTURE_LOGIC_GATE.search(str(line))
            # CONTROL_STRUCTURE_JAVA_METHOD_COUNT += REGEX_CONTROL_STRUCTURE_JAVA_METHOD.search(str(line))

    print('IF_ELSEIF ', CONTROL_STRUCTURE_IF_ELSEIF_COUNT)
    print('WHILE_DO_WHILE ', CONTROL_STRUCTURE_FOR_WHILE_DO_WHILE_COUNT)
    print('SWITCH ', CONTROL_STRUCTURE_FOR_SWITCH_COUNT)
    print('CASE ', CONTROL_STRUCTURE_FOR_CASE_COUNT)
    print('LOGIC_GATE ', CONTROL_STRUCTURE_LOGIC_GATE_COUNT)
    print('JAVA_METHOD ', CONTROL_STRUCTURE_JAVA_METHOD_COUNT)
    return [CONTROL_STRUCTURE_IF_ELSEIF_COUNT, CONTROL_STRUCTURE_FOR_WHILE_DO_WHILE_COUNT,
            CONTROL_STRUCTURE_FOR_SWITCH_COUNT, CONTROL_STRUCTURE_FOR_CASE_COUNT, CONTROL_STRUCTURE_LOGIC_GATE_COUNT,
            CONTROL_STRUCTURE_JAVA_METHOD_COUNT]


# print(getComplexity())
