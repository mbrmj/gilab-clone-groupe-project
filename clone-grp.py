try:
    # For Python 3.0 and later
    from urllib.request import urlopen
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen
import json
import subprocess, shlex
import sys
import os

def getProjects( gitlabInstance,token,grpID ):
    url="https://"+gitlabInstance+"/api/v4/groups/"+grpID+"/projects?private_token="+token
    print("project : %s" % (url))
    allProjects     = urlopen(url)
    allProjectsDict = json.loads(allProjects.read())
    if bool(allProjectsDict):
        for thisProject in allProjectsDict: 
            try:
                print("repo: %s" % (thisProject['ssh_url_to_repo']))
                thisProjectURL  = thisProject['ssh_url_to_repo']
                command     = shlex.split('git clone %s' % thisProjectURL)
                resultCode  = subprocess.Popen(command)

            except Exception as e:
                print("Error on %s: %s" % (thisProjectURL, e.strerror))

def getGroups( gitlabInstance,token,grpID ):
    allGroups     = urlopen("https://"+gitlabInstance+"/api/v4/groups/"+grpID+"/subgroups?private_token="+token)
    allGroupsDict = json.loads(allGroups.read())
    if bool(allGroupsDict):
        parent=os.getcwd()
        for thisGroups in allGroupsDict: 
            try:
                groupId  = str(thisGroups['id'])
                groupName  = str(thisGroups['name'])
                print("GROUP OF PROJECT %s" % (groupId))
                os.makedirs(groupName)
                print("%s" % parent)
                os.chdir("%s/%s" % (parent,groupName))
                getProjects(gitlabInstance,token,groupId)
                getGroups(gitlabInstance,token,groupId)
                os.chdir(parent)
            except Exception as e:
                print("error on groupe  with dir %s" % os.getcwd())
                print("Error on : %s" % (e))
                exit(1);

getProjects(sys.argv[1],sys.argv[2],sys.argv[3]);
getGroups(sys.argv[1],sys.argv[2],sys.argv[3]);
