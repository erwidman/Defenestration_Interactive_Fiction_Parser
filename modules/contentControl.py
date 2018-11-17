import yaml
import os


rooms = None
title = None
plot = None







def __getYAML(fname):
    with open(fname,'r') as stream:
            try:
                return yaml.load(stream)
                #return stream.read()
            except yaml.YAMLError as exc:
                print(exc)

def __getFile(fname):
    with open(fname,'r') as stream:
            try:
                return stream.read()
            except yaml.YAMLError as exc:
                print(exc)

contentLoaded=False
def loadContent():
    global title
    global rooms
    global plot
    if not contentLoaded:
       additionalContentLoaded=True
       cwd = os.getcwd()
       title=__getFile(cwd+"/content/miscContent.yaml")
       rooms=__getYAML(cwd+"/content/rooms.yaml")
       plot=__getYAML(cwd+"/content/plot.yaml")
       #print(rooms)
       #print(rooms)
       #print("\n%s" % title)






