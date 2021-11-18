
print("Accessing Github Info")

from github import Github   # github api access
import json                 # for converting a dictionary to a string
import pymongo              # for mongodb access
import requests
from requests.models import REDIRECT_STATI

#Function to write the json contents of a url into a dictionary and return it
def dic_writer(url):
    reponse = requests.get[url]
    return response.json()  

#we initialise a PyGithub Github object with our access token.
#     note that this token is ours, and now deleted. You must 
#     crete your own access token and use here instead. 
g = Github("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")


#Let's get the user object and build a data dictionary
usr = g.get_user()

repos_url = usr.repos_url
response = requests.get(repos_url)
repo_dict = response.json()

#for x in repo_dict:    Will need to find out how to go through the repos

repospec_dict = repo_dict[1]
print (repospec_dict.keys())
events_url = repospec_dict['events_url']
commits_url = repospec_dict['commits_url']
collab_url = repospec_dict['collaborators_url']
events_dic = dic_writer(events_url) 
commits_dic = dic_writer(commits_url) 
collab_dic = dic_writer(collab_url)

    #Do Something with the dictionarys




#
