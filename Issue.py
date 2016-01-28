import dateutil.parser
from dateutil.tz import *

from datetime import datetime

class Issue:
  issueType = ""
  jiraNumber = ""
  jiraStatus = ""
  resolutionDate = ""
  assignee = ""
  createdBy = ""
  created = ""
  devTimeDays = 0
  statusInfo = {}
  epicLink = ""

  def __init__(self, issue):
    self.jiraNumber = self.emptyIfNone(issue.raw["key"])
    self.jiraStatus = self.emptyIfNone(issue.raw["fields"]["status"]["name"])
    self.resolutionDate = self.emptyIfNone(issue.raw["fields"]["resolutiondate"])

    if issue.raw["fields"]["assignee"] is not None:
      self.assignee = self.emptyIfNone(issue.raw["fields"]["assignee"]["displayName"])

    self.createdby = self.emptyIfNone(issue.raw["fields"]["creator"]["displayName"])
    self.created = self.emptyIfNone(issue.raw["fields"]["created"])
    self.issuetype = self.emptyIfNone(issue.raw["fields"]["issuetype"]["name"])
    self.epicLink = self.emptyIfNone(issue.raw["fields"]["customfield_10006"])
    
    self.statusInfo = {}
    self.calcStatusTimes(issue)

  def emptyIfNone(self, val):
    if val is not None:
      return val

    return ""

  def zeroIfNone(self, val):
    if val is not None:
      return val
  
    return 0

  def calcStatusTimes(self, issue):
    previousStateTransitionTime = self.created
    previousStateTransition = 'Open'

    for history in issue.raw['changelog']['histories']:
      if history['items'][0]['field'] == 'status':
        if previousStateTransition <> '':
          self.addStatusTime(previousStateTransition, self.calcIncrementalStatusTime(previousStateTransitionTime, previousStateTransition, history['created']))

        previousStateTransitionTime = history['created']
        previousStateTransition = history['items'][0]['toString']

    now = unicode(datetime.now(tzlocal()))
    increment = self.calcIncrementalStatusTime(previousStateTransitionTime, previousStateTransition, now)
    self.addStatusTime(previousStateTransition, increment)


  def calcIncrementalStatusTime(self, startTime, state, endTime):
    statusSeconds = 0
    start = self.dateWithTimezone(startTime)
    end = self.dateWithTimezone(endTime)

    # print 'start', startTime, '(', start, ') end ', endTime, '(', end, ')'

    delta = end - start

    statusSeconds = delta.days*86400.0 + delta.seconds

    return statusSeconds

  def dateWithTimezone(self, dt):
    localDt = dateutil.parser.parse(dt)
    if localDt.tzinfo == None:
      localDt.replace(tzinfo=tzlocal())

    return localDt

  def addStatusTime(self, status, statusTime):
    currentTime = self.statusInfo.get(status, None)
    if currentTime is None:
      currentTime = 0
    currentTime += self.secondsToDays(statusTime)
    self.statusInfo[status] = currentTime

  def secondsToDays(self, seconds):
    return seconds/86400.0
