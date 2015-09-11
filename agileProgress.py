#!/usr/bin/python

import sys
import json
import os
import httplib
import urllib
import ssl

import ConfigParser

from oauth2client.client import flow_from_clientsecrets
from apiclient.discovery import build

from restkit import Resource, BasicAuth, request

def processWorkFromJira(since, config):
  verbose = config.getboolean('general', 'verbose')

  user = config.get('jira', 'user')
  password = config.get('jira', 'password')
  auth = BasicAuth(user, password)

  jiraHost = config.get('jira', 'host')

  jql_projects = 'project in (' + config.get('jira', 'projects') + ')'
  jql_status = 'status in (Resolved,Closed)'
  jql_since = 'resolutiondate >= "' + since + '"'
  jql_and = " AND "

  jql = jql_projects + jql_and + jql_status + jql_and + jql_since

  encoded_jql = urllib.quote_plus(jql)

  fields = config.get('jira', 'fields')
  log(fields);

  pageSize = 20
  startAt = 0

  while True:
    jiraPath = jiraHost + "/rest/api/2/search?maxResults=" + str(pageSize) + "&startAt=" + str(startAt) + "&fields=" + fields + "&jql=" + encoded_jql

    resource = Resource(jiraPath, filters=[auth])

    response = resource.get(headers = {'Content-Type' : 'application/json'})

    stories = json.loads(response.body_string())

    if "issues" in stories:
      storiesFound = len(stories["issues"])
      storiesTotal = stories["total"]

      for story in stories["issues"]:
        if story is not None:
          jiraNumber = story["key"]
          jiraStatus = story["fields"]["status"]["name"]

          sprintName = ""
          sprintDate = ""
          assignee = ""
          epic = ""
          issuetype = ""

          if story["fields"]["resolutiondate"] is not None:
            sprintDate = story["fields"]["resolutiondate"]

          if story["fields"]["assignee"] is not None:
            assignee = story["fields"]["assignee"]["displayName"]

          if story["fields"]["issuetype"] is not None:
            issuetype = story["fields"]["issuetype"]["name"]

          writeStory(issuetype, jiraNumber, jiraStatus, sprintDate, assignee)

      if storiesFound > 0 and storiesFound < storiesTotal:
        startAt += pageSize
      else:
        break
    else:
      break

def writeStory(issuetype, jiraNumber, jiraStatus, resolutionDate, assignee):
  outputFile.write(jiraNumber + "," + issuetype + "," + jiraStatus + "," + resolutionDate + "," + assignee + "\n")  

def log(msg):
  sys.stdout.write(msg + "\n")


workSince = sys.argv[1]
if not workSince:
  workSince = '2015-01-01'

config = ConfigParser.RawConfigParser()
config.read('agileProgress.ini')


outputFileName = sys.argv[2]
outputFile = open(outputFileName, 'w')

processWorkFromJira(sys.argv[1], config)
      
outputFile.close()
