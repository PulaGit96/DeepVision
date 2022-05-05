from os import path

filename = '../GitDownloads/README.md'
string_value = ''

if path.isfile(filename):
    with open(filename) as file:
        for line in file:
            string_value = string_value + ' ' + line.rstrip()

    print(string_value)
else:
    print('file not found')

