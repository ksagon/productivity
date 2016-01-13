class Issue:
  issueType = ""
  jiraNumber = ""
  jiraStatus = ""
  resolutionDate = ""
  assignee = ""
  createdBy = ""
  created = ""
  devTimeDays = 0
  
  def __init__(self, issue, devTimeSeconds):
    self.jiraNumber = self.emptyIfNone(issue.raw["key"])
    self.jiraStatus = self.emptyIfNone(issue.raw["fields"]["status"]["name"])
    self.resolutionDate = self.emptyIfNone(issue.raw["fields"]["resolutiondate"])
    
    if issue.raw["fields"]["assignee"] is not None:
      self.assignee = self.emptyIfNone(issue.raw["fields"]["assignee"]["displayName"])

    self.createdby = self.emptyIfNone(issue.raw["fields"]["creator"]["displayName"])
    self.created = self.emptyIfNone(issue.raw["fields"]["created"])
    self.issuetype = self.emptyIfNone(issue.raw["fields"]["issuetype"]["name"])
    self.devTimeDays = self.secondsToDays(self.zeroIfNone(devTimeSeconds))

  def emptyIfNone(self, val):
    if val is not None:
      return val

    return ""

  def zeroIfNone(self, val):
    if val is not None:
      return val
  
    return 0

  def secondsToDays(self, seconds):
    return seconds/86400.0
