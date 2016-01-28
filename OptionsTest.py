#!/usr/bin/python

import unittest, ConfigParser

from Options import Options

class OptionsTest(unittest.TestCase):
  def testHelp(self):
    args = ["-?"]
    opt = Options('agileProgress.ini', args)

  def testHost(self):
    args = ["-h", "jira.edo.local"]
    opt = Options('agileProgress.ini', args)
    
    assert opt.host == 'jira.edo.local'

  def testSince(self):
    args = ["-s", "2015-01-01"]
    opt = Options('agileProgress.ini', args)
    
    assert opt.since == '2015-01-01'

  def testDefaultFileIni(self):
    args = []
    opt = Options('agileProgress.ini', args)

    assert opt.outputFile == 'agileProgress.csv'

  def testVerbose(self):
    args = ["-v"]
    opt = Options('agileProgress.ini', args)

    assert opt.verbose == True

  def testUser(self):
    args = ['-u', 'bob.user']
    opt = Options('agileProgress.ini', args)

    assert opt.user == 'bob.user'

  def testPassword(self):
    args = ['-p', 'password']
    opt = Options('agileProgress.ini', args)

    assert opt.password == 'password'

  def testProjects(self):
    args = ['--projects', '"Project 1", Project_2']
    opt = Options('agileProgress.ini', args)

    assert opt.projects == '"Project 1", Project_2'

  def testFields(self):
    args = []
    opt = Options('agileProgress.ini', args)

    assert opt.fields == 'issuetype,summary,status,resolutiondate,assignee,creator,created,customfield_10006'

  def testOutput(self):
    args = ['-o', 'bobs-progress.csv']
    opt = Options('agileProgress.ini', args)

    assert opt.outputFile == 'bobs-progress.csv'

if __name__ == "__main__":
  unittest.main()
