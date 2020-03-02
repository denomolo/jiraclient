#!/usr/bin/env python3
import requests
from requests.auth import HTTPBasicAuth
from dateutil.parser import parse
import json


class JiraClient:
    def __init__(self, jiraserver, jiraport, jirauser, jirapass):
        self.jiraserver = jiraserver
        self.jiraport = jiraport
        self.jirauser = jirauser
        self.jirapass = jirapass
        self.jiraURL = "https://" + jiraserver + ":" + jiraport + "/rest/api/2"
        self.headers = {'Content-Type': 'application/json'}

    def restRequest(self, url, method, payload):
        try:
            auth = (self.jirauser, self.jirapass)
            if (method == 'get'):
                return requests.get(url,
                                    auth=HTTPBasicAuth(self.jirauser,
                                    self.jirapass), headers=self.headers,
                                    params=payload)
            if (method == 'put'):
                requests.put(url,
                             auth=HTTPBasicAuth(self.jirauser, self.jirapass),
                             headers=self.headers, data=payload)
                return ("OK")
        except Exception as e:
            return e.exceptions

    # function name: getVersionsByProject
    # Mandatory: Project Name
    # Returns  : json of all project versions

    def getVersionsByProject(self, prjName):
        payload = ""
        url = self.jiraURL + "/project/" + prjName + "/versions"
        method = "get"
        resp = self.restRequest(url, method, payload)
        return resp

    # function name: getArchiveList
    # Mandatory: Project Name, Archivation Interval
    # Returns  : json subset of all project versions that need to be archived

    def getArchiveList(self, prj_name, a_interval):
        v_list = self.getVersionsByProject(prj_name)
        j_data = v_list.json()
        a_data = []
        for c in j_data:
            is_archived = c["archived"]
            if (not is_archived):
                try:
                    u_release = parse(c["userReleaseDate"])
                    u_date = u_release.date()
                    release = parse(c["releaseDate"])
                    r_date = release.date()
                    if ((r_date < a_interval) or (u_date < a_interval)):
                        a_data.append(c)
                except KeyError as error:
                    a_data.append(c)
        return json.dumps(a_data)

    def archiveVersion(self, v_id):
        payload = '{ "id": "%s","archived": true}' % v_id
        method = "put"
        url = self.jiraURL + "/version/" + v_id
        return (self.restRequest(url, method, payload))

    # This function was written to extend this class to find and assign
    # attributes to jira users.
    def searchUser(self, s_str):
        payload = ''
        url = self.jiraURL + '/user/search?username=' + s_str
        method = 'get'
        resp = self.restRequest(url, method, payload)
        return resp

    def getAllUsers(self):
        results = []
        start_at = 0
        step = 50
        done = False
        while not done:
            payload = ''
            url = '%s/group/member?groupname=users&includeInactiveUsers=false&startAt=%d&maxResults=%d' % (self.jiraURL, start_at, step)
            method = 'get'
            resp = self.restRequest(url, method, payload)
            data = json.loads(resp.text)
            start_at += step
            results.append(data["values"])
            if (int(data["total"]) < start_at):
                done = True
        return results
