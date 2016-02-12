import sys

from jira import JIRA
from Issue import Issue

class JiraProcessor:
    opts = None
    verbose = False

    def __init__(self, opts):
        self.opts = opts
        self.verbose = self.opts.verbose

    def processEpic(self, epic):
        outputFile = open(self.opts.outputFile, 'a')
        jql = self.initEpicJQL(epic)
        self.processWorkFromJiraClient(jql, outputFile)

    def processCompleted(self):
        outputFile = open(self.opts.outputFile, 'w')
        jql = self.initJQL()
        self.processWorkFromJiraClient(jql, outputFile)
    
    def processWorkFromJiraClient(self, jql, outputFile):
        jira = self.initJira()
        pageSize = 20
        startAt = 0
        
        while True:
            issues = jira.search_issues(jql, fields=self.opts.fields, maxResults=pageSize, startAt=startAt, expand='changelog')
            
            storiesFound = len(issues)
            storiesTotal = issues.total
            
            for i in issues:
                issue = Issue(i)
                self.writeStory(issue, outputFile)
            
            sys.stdout.write('#')
            sys.stdout.flush()
            
            if storiesFound > 0 and storiesFound < storiesTotal:
                startAt += pageSize
                if startAt % 500 == 0:
                    print(" " + str(startAt) + " / " + str(storiesTotal))
            else:
                print(" " + str(storiesTotal) + " / " + str(storiesTotal))
                break
        
        outputFile.close()

    def initJira(self):
        jira_options = {
            'server': self.opts.host
        }

        return JIRA(options=jira_options, basic_auth=(self.opts.user, self.opts.password))

    def initEpicJQL(self, epic):
        jql_projects = 'project in (' + self.opts.projects + ')'
        jql_type = 'issuetype in (Story,Bug)'
        jql_epic = '"Epic Link" = ' + epic
        jql_and = " AND "
        jql_order_by = " ORDER BY resolutiondate"

        jql = jql_projects + jql_and + jql_epic + jql_and + jql_type + jql_order_by
        
        if self.verbose:
            print(jql)

        return jql
      

    def initJQL(self):
        jql_projects = 'project in (' + self.opts.projects + ')'
        jql_status = 'status in (Resolved,Closed)'
        jql_type = 'issuetype in (Story,Bug)'
        jql_since = 'resolutiondate >= "' + self.opts.since + '"'
        jql_and = " AND "
        jql_order_by = " ORDER BY resolutiondate"
        
        jql = jql_projects + jql_and + jql_status + jql_and + jql_since + jql_and + jql_type + jql_order_by
        
        if self.verbose:
            print(jql)
        
        return jql

    def writeStory(self, issue, outputFile):
        outputFile.write(issue.jiraNumber + "," + issue.epicLink + "," + issue.issuetype + "," + issue.jiraStatus + "," + issue.resolutionDate + "," + issue.assignee + "," + issue.created + "," + issue.createdby + "," + str(issue.statusInfo.get('Open', 0)) + "," + str(issue.statusInfo.get('In Progress', 0)) + "," + str(issue.statusInfo.get('Delivered To QA', 0)) + "\n")

    def log(self, msg):
        sys.stdout.write(msg + "\n")
