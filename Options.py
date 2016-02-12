import ConfigParser, getopt, sys

class Options:
    verbose = False
    outputFile = ""
    since = ""
    host = ""
    user = ""
    password = ""
    projects = ""
    fields = "issuetype,summary,status,resolutiondate,assignee"
    epics = ""
    
    def __init__(self, iniFile, argv):
        self._initFromIni(iniFile)
        self._parseOpts(argv)
    
    def _initFromIni(self, iniFile):
        config = ConfigParser.SafeConfigParser()
        config.read(iniFile)
        
        if config.has_option('general', 'verbose'):
            self.verbose = config.getboolean('general', 'verbose')
        
        if config.has_option('jira', 'host'):
            self.host = config.get('jira', 'host')
        
        if config.has_option('jira', 'user'):
            self.user = config.get('jira', 'user')
        
        if config.has_option('jira', 'password'):
            self.password = config.get('jira', 'password')
        
        if config.has_option('jira', 'projects'):
            self.projects = config.get('jira', 'projects')
        
        if config.has_option('jira', 'fields'):
            self.fields = config.get('jira', 'fields')
        
        if config.has_option('jira', 'epics'):
            self.epics = config.get('jira', 'epics')
        
        if config.has_option('general', 'output'):
            self.outputFile = config.get('general', 'output')
        
        if config.has_option('general', 'since'):
            self.since = config.get('general', 'since')
    
    def _parseOpts(self, argv):
        try:
            opts, args = getopt.getopt(argv,"?vh:u:p:s:o:e:",["verbose", "host=", "user=", "password=", "since=", "projects=", "output=", "epics="])
        except getopt.GetoptError:
          self.printHelp()
          sys.exit(-1)
    
        for opt, arg in opts:
            if opt == '-?':
                self.printHelp()
            elif opt in ("-v", "--verbose"):
                self.verbose = True
            elif opt in ("-h", "--host"):
                self.host = arg
            elif opt in ("-u", "--user"):
                self.user = arg
            elif opt in ("-p", "--password"):
                self.password = arg
            elif opt in ("--projects"):
                self.projects = arg
            elif opt in ("-o", "--output"):
                self.outputFile = arg
            elif opt in ("-s", "--since"):
                self.since = arg
            elif opt in ("-e", "--epics"):
                self.epics = arg

    def printHelp(self):
        print("""
Usage: test.py [OPTIONS]
Options
  -?: print this help
  -v, --verbose: be chatty
  -h, --host: the url of the Jira host
  -u, --user: the Jira user
  -p, --password: the password for the Jira user
  -s, --since: the earliest date to look back to for delivery
  -e, --epics: the comma delimited list of epics to process
  -o, --output: the file to send output, if null will write to stdout
  --projects: the list of Jira projects from which to pull issues
    """)
