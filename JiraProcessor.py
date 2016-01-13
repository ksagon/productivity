import sys, dateutil.parser

from Options import Options
from jira import JIRA
from Issue import Issue

class JiraProcessor:
  opts = None
  verbose = False

  def __init__(self, opts):
    self.opts = opts
    self.verbose = self.opts.verbose

  def processWorkFromJiraClient(self):
    outputFile = open(self.opts.outputFile, 'w')

    jira = self.initJira()
    jql = self.initJQL()

    pageSize = 20
    startAt = 0

    while True:
      issues = jira.search_issues(jql, fields=self.opts.fields, maxResults=pageSize, startAt=startAt, expand='changelog')

      storiesFound = len(issues)
      storiesTotal = issues.total

      for i in issues:
        devTime = self.calcDevTime(i)

        issue = Issue(i, devTime)

        self.writeStory(issue, outputFile)

      sys.stdout.write('#')
      sys.stdout.flush()

      if storiesFound > 0 and storiesFound < storiesTotal:
        startAt += pageSize
        if startAt % 300 == 0:
          print " " + str(startAt) + " / " + str(storiesTotal)
      else:
        print " " + str(storiesTotal) + " / " + str(storiesTotal)
        break

    outputFile.close()


  def initJira(self):
    jira_options = {
      'server': self.opts.host
    }

    return JIRA(options=jira_options, basic_auth=(self.opts.user, self.opts.password) )


  def initJQL(self):
    jql_projects = 'project in (' + self.opts.projects + ')'
    jql_status = 'status in (Resolved,Closed)'
    jql_type = 'issuetype in (Story,Bug)'
    jql_since = 'resolutiondate >= "' + self.opts.since + '"'
    jql_and = " AND "
    jql_order_by = " ORDER BY resolutiondate"

    jql = jql_projects + jql_and + jql_status + jql_and + jql_since + jql_and + jql_type + jql_order_by

    if self.verbose:
      print jql

    return jql


  def calcDevTime(self, issue):
    devTime = 0
    previousStateTransitionTime = ''
    previousStateTransition = ''

    for history in issue.raw['changelog']['histories']:
      if history['items'][0]['field'] == 'status':
        devTime += self.calcIncrementalDevTime(previousStateTransitionTime, previousStateTransition, history['created'], history['items'][0]['toString'])
        previousStateTransitionTime = history['created']
        previousStateTransition = history['items'][0]['toString']

    return devTime


  def calcIncrementalDevTime(self, startTime, previousState, endTime, currentState):
    devSeconds = 0

    if previousState == "In Progress":
      start = dateutil.parser.parse(startTime)
      end = dateutil.parser.parse(endTime)

      delta = end - start

      devSeconds = delta.days*86400 + delta.seconds

    return devSeconds


  def writeStory(self, issue, outputFile):
    outputFile.write(issue.jiraNumber + "," + issue.issuetype + "," + issue.jiraStatus + "," + issue.resolutionDate + "," + issue.assignee  + "," + issue.created + "," + issue.createdby + "," + str(issue.devTimeDays) + "\n")  


  def log(msg):
    sys.stdout.write(msg + "\n")
