#!/usr/bin/python

import sys
import json
import os
import httplib
import urllib
import ssl

from oauth2client.client import flow_from_clientsecrets
from apiclient.discovery import build

from restkit import Resource, BasicAuth, request

def processWorkFromJira(since):
  verbose = False

  auth = BasicAuth('kevin.sagon', 'the.1.2.fflanda')

  jiraHost = "https://edointeractive.atlassian.net"

  jql_projects = 'project in ("Marketplace", "FI Solutions", Prewards, "edo Epics", "edo User Experience")'
  jql_status = 'status in (Resolved,Closed)'
  jql_since = 'resolutiondate >= "' + since + '"'
  jql_and = " AND "

  jql = jql_projects + jql_and + jql_status + jql_and + jql_since

  encoded_jql = urllib.quote_plus(jql)

  fields = "issuetype,summary,status,customfield_10005,resolutiondate,assignee,customfield_10006"

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

          if story["fields"]["customfield_10005"] is not None:
            jiraSprint = story["fields"]["customfield_10005"][0]
            sprintData = jiraSprint[jiraSprint.index('['):jiraSprint.index(']')]
            sprintMap = dict(u.split("=") for u in sprintData.split(","))
            sprintName = sprintMap["name"]

          if story["fields"]["assignee"] is not None:
            assignee = story["fields"]["assignee"]["displayName"]

          if story["fields"]["customfield_10006"] is not None:
            epic = story["fields"]["customfield_10006"]

          if story["fields"]["issuetype"] is not None:
            issuetype = story["fields"]["issuetype"]["name"]

          writeStory(epic, issuetype, jiraNumber, jiraStatus, sprintDate, assignee)

      if storiesFound > 0 and storiesFound < storiesTotal:
        startAt += pageSize
      else:
        break
    else:
      break

def writeStory(epic, issuetype, jiraNumber, jiraStatus, resolutionDate, assignee):
  outputFile.write(jiraNumber + "," + issuetype + "," + epic + "," + jiraStatus + "," + resolutionDate + "," + assignee + "\n")  

def log(msg):
  sys.stdout.write(msg + "\n")


workSince = sys.argv[1]
if not workSince:
  workSince = '2015-01-01'

outputFileName = sys.argv[2]
outputFile = open(outputFileName, 'w')

processWorkFromJira(sys.argv[1])
      
outputFile.close()
