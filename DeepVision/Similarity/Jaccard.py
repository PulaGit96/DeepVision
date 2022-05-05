import re


# Jaccard Algo
def jaccard_similarity(doc1, doc2):
    # List the unique words in a document
    words_doc1 = set(doc1.lower().split())
    words_doc2 = set(doc2.lower().split())

    # Find the intersection of words list of doc1 & doc2
    intersection = words_doc1.intersection(words_doc2)

    # Find the union of words list of doc1 & doc2
    union = words_doc1.union(words_doc2)

    # Calculate Jaccard similarity score
    # using length of intersection set divided by length of union set
    return float(len(intersection)) / len(union)


def get_similarity():
    doc1 = ''
    doc2 = ''
    with open('Similarity/upload/first_file.java') as file:
        for line in file:
            doc1 += line.rstrip() + ' '

    with open('Similarity/upload/second_file.java') as file:
        for line in file:
            doc2 += line.rstrip() + ' '

    first_file_method_count = get_method_counts('Similarity/upload/first_file.java')
    second_file_method_count = get_method_counts('Similarity/upload/second_file.java')

    method_similarity_score = first_file_method_count / second_file_method_count
    jaccard_similarity_score = jaccard_similarity(doc1, doc2)

    total_similarity_score = (method_similarity_score + jaccard_similarity_score) / 2

    return total_similarity_score


# doc_1 = "Data is the new oil of the digital economy"
# doc_2 = "Data is a new oil"
#
# x = Jaccard_Similarity(doc_1, doc_2)
# print(x)


def get_method_counts(path):
    CONTROL_STRUCTURE_JAVA_METHOD = "(public|protected|private|static|\\s) +[\\w\\<\\>\\[\\]]+\\s+(\\w+) *\\([^\\)]*\\) *(\\{?|[^;])";
    count = 1
    content = []
    with open(path) as file:
        for line in file:
            content.append(line.rstrip())

    for line in content:
        REGEX_CONTROL_STRUCTURE_JAVA_METHOD = re.compile(CONTROL_STRUCTURE_JAVA_METHOD)

    if REGEX_CONTROL_STRUCTURE_JAVA_METHOD.search(str(line)) == None:
        pass
    else:
        count += 1

    return count
