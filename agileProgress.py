#!/usr/bin/python

import sys, json, os, httplib, urllib, ssl

from oauth2client.client import flow_from_clientsecrets
from apiclient.discovery import build
from restkit import Resource, BasicAuth, request
from Options import Options

def processWorkFromJira(opts):
  verbose = opts.verbose

  outputFile = open(opts.outputFile, 'w')

  user = opts.user
  password = opts.password
  auth = BasicAuth(user, password)

  jiraHost = opts.host

  jql_projects = 'project in (' + opts.projects + ')'
  jql_status = 'status in (Resolved,Closed)'
  jql_type = 'issuetype in (Story,Bug)'
  jql_since = 'resolutiondate >= "' + opts.since + '"'
  jql_and = " AND "

  jql = jql_projects + jql_and + jql_status + jql_and + jql_since + jql_and + jql_type

  encoded_jql = urllib.quote_plus(jql)

  fields = opts.fields

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

          writeStory(issuetype, jiraNumber, jiraStatus, sprintDate, assignee, outputFile)

      if storiesFound > 0 and storiesFound < storiesTotal:
        startAt += pageSize
      else:
        break
    else:
      break
  
  outputFile.close()

def writeStory(issuetype, jiraNumber, jiraStatus, resolutionDate, assignee, outputFile):
  outputFile.write(jiraNumber + "," + issuetype + "," + jiraStatus + "," + resolutionDate + "," + assignee + "\n")  

def log(msg):
  sys.stdout.write(msg + "\n")

def main(argv):
  opts = Options('agileProgress.ini', argv)

  processWorkFromJira(opts)

if __name__ == "__main__":
   main(sys.argv[1:])

