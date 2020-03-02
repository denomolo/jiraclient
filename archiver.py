#!/usr/bin/env python3
from optparse import OptionParser
from jiraclient import JiraClient
import json
import datetime
import time

INTERVAL = 30
GRACE = 10


def get_interval_date(interval):
    today = datetime.date.today()
    delta = datetime.timedelta(days=int(interval))
    cutoff = today - delta
    return (cutoff)


def logger(log_message):
    print(time.strftime("%Y-%m-%d %H:%M:%S"), ": ", log_message)


help_text = "usage: %prog " \
            "-S/--server jira_server " \
            "-U/--user jira_user " \
            "-P/--pass user_password " \
            "-X/--port jira_port " \
            "-l/--list project_list " \
            "-I/--interval archive interval"
parser = OptionParser(usage=help_text)
parser.add_option("-U", "--user",
                  dest="jirauser",
                  help="The jira user for running the archiver",
                  metavar="User")
parser.add_option("-P", "--pass",
                  dest="jirapass",
                  help="The jira user's password for running the archiver",
                  metavar="Pass")
parser.add_option("-S", "--server", dest="jiraserver",
                  help="The jira server for running the archiver",
                  metavar="Server")
parser.add_option("-X", "--port",
                  dest="jiraport",
                  help="The jira server port for running the archiver",
                  metavar="Port")
parser.add_option("-L", "--list",
                  dest="project_list",
                  help="Comma delimited list of projects to archive",
                  metavar="List")
parser.add_option("-I", "--interval",
                  dest="interval",
                  help="Interval to archive, defaults to "
                  + str(INTERVAL)
                  + " days",
                  metavar="Interval")

(options, args) = parser.parse_args()

if options.jirauser is None or \
   options.jirapass is None or \
   options.jiraserver is None or \
   options.jiraport is None:
    parser.error("All values are required")

if options.project_list is None:
    parser.error("Must provide at least one project to archive")

jiraserver = options.jiraserver
jiraport = options.jiraport
jirauser = options.jirauser
jirapass = options.jirapass
a_interval = options.interval
d_cutoff = get_interval_date(a_interval)

project_list = options.project_list.split(',')
cli = JiraClient(jiraserver, jiraport, jirauser, jirapass)

for project in project_list:
    archive_list = json.loads(cli.getArchiveList(project, d_cutoff))
    max_archive = len(archive_list)
    opt_archive = max_archive - GRACE
    i = 0
    logger("Archive Project: %s" % project)
    logger("Cutoff date: %s" % d_cutoff)
    logger("Length: %i" % opt_archive)

    for line in archive_list:
        v_id = line["id"]
        if (i < opt_archive):
            logger("Archiving %s returned %s"
                   % (v_id, cli.archiveVersion(v_id)))
            i += 1
        else:
            logger("Not archiving %s" % v_id)
