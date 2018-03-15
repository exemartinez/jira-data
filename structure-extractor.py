# This script shows how to connect to a JIRA instance with a
# username and password over HTTP BASIC authentication.
from collections import Counter

from jira import JIRA
from io import StringIO
import time
from configparser import ConfigParser
import sys

# Codification system.
'''WATCH OUT THIS LINES ~ THESE COULD BROKE THE ENTIRE CODE; FIND SOME OTHER WAY TO ENCONDE THE STRINGS.'''
#reload(sys)
#sys.setdefaultencoding('utf-8')

# Constants
__INI_FILE__='.\\properties.ini'

# Common functions


class PropertiesHandler():
    '''It opens the properties.ini file and loads into memory for consumption.'''

    config = None
    user = None
    pwd = None
    server_url = None
    projects = None

    def __init__(self):
        self.load()

    def load(self):
        '''It loads or reloads the configuration variables.'''
        config = ConfigParser()
        config.read(__INI_FILE__)

        self.user = config.get('credentials', 'user')
        self.pwd = config.get('credentials', 'pwd')
        self.server_url = config.get('server', 'url')
        self.projects = config.get('monitor', 'projects').split(',')

    def getIterableProjects(self):
        for project in self.projects:
            yield project.strip()


class JiraDataExtractor():
    ''' Extracts structural data from Jira for further analysis '''
    options = None
    jira = None
    cfg = None

    def __init__(self):
        # By default, the client will connect to a JIRA instance started from the Atlassian Plugin SDK.
        # See https://developer.atlassian.com/display/DOCS/Installing+the+Atlassian+Plugin+SDK
        # for details.
        self.cfg = PropertiesHandler()

        self.options = {'server': self.cfg.server_url}
        self.jira = JIRA(self.options, basic_auth=(self.cfg.user, self.cfg.pwd))  # a username/password tuple

    def connect(self):
        '''It connects against the pre configured Jira server.'''
        self.options = {'server': self.cfg.server_url}
        self.jira = JIRA(self.options, basic_auth=(self.cfg.user, self.cfg.pwd))  # a username/password tuple

    def getSendToCSVFile(self,fileStr):
        '''Sends the String to a file'''
        f = open(".\\xls-export\\" + time.strftime("%Y%m%d") + "-" + time.strftime("%H%M%S") + "-jira-export.csv","wb")
        f.write(fileStr)
        f.close()

    def getAllCustomFields(self,name):
        '''Getting all the current custom fields ID's and dump it to a CSV file for revision.'''
        # Fetch all fields
        allfields = self.jira.fields()
        # Make a map from field name -> field id
        nameMap = {field['name']: field['id'] for field in allfields}

        stringBuffer = StringIO()
        stringBuffer.write("Field Name;Code\n")

        for field in allfields:
            stringBuffer.write(field['name'] + ";" + field['id'] + "\n")


        self.getSendToCSVFile(stringBuffer.getvalue())

        if (name != None):
            try:
                result = nameMap[name]
            except:
                return None

            return result
        else:
            return None

jiramng = JiraDataExtractor()
jiramng.getCustomFieldID()