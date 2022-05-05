from git import Repo

repo_dir = 'LocalDir'


git_url = 'https://github.com/HouariZegai/Calculator.git'

def download():
    Repo.clone_from(git_url, repo_dir)


download()


# import os
# import sys
# import shutil
#
# mydir= 'LocalDir'
# try:
#     shutil.rmtree(mydir)
# except OSError as e:
#     print ("Error: %s - %s." % (e.filename, e.strerror))