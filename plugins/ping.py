#!/usr/bin/env python
# coding: utf-8


import re
from subprocess import Popen, PIPE
import sys

import plugins


def _get_match_groups(ping_output, regex):
    match = regex.search(ping_output)
    if not match:
        return False
    else:
        return match.groups()


def system_command(Command, newlines=True):
    Output = ""
    Error = ""
    try:
        #Output = subprocess.check_output(Command,stderr = subprocess.STDOUT,shell='True')
        proc = Popen(Command.split(), stdout=PIPE)
        Output = proc.communicate()[0]
    except:
        pass

    if Output:
        if newlines == True:
            Stdout = Output.split("\\n")
        else:
            Stdout = Output
    else:
        Stdout = []
    if Error:
        Stderr = Error.split("\n")
    else:
        Stderr = []

    return (Stdout,Stderr)


def collect_ping(hostname):
    if sys.platform == "linux" or sys.platform == "linux2":
        response = str(system_command("ping -W 5 -c 1 " + hostname, False)[0])
        matcher = re.compile(r'(\d+.\d+)/(\d+.\d+)/(\d+.\d+)/(\d+.\d+)')
        minping, avgping, maxping, jitter = _get_match_groups(response, matcher)
        response = avgping
    elif sys.platform == "darwin":
        # print system_command("ping -W 5 -c 2 " + hostname, False)
        response = str(system_command("ping -c 1 " + hostname, False)[0])
        # matcher = re.compile(r'min/avg/max/stddev = (\d+)/(\d+)/(\d+)/(\d+) ms')
        # min, avg, max, stddev = _get_match_groups(response, matcher)
        matcher = re.compile(r'(\d+.\d+)/(\d+.\d+)/(\d+.\d+)/(\d+.\d+)')
        matched = _get_match_groups(response, matcher)
        if matched == False:
            response = 0
        else:
            minping, avgping, maxping, jitter = matched
            response = avgping
    elif sys.platform == "win32":
        response = system_command("ping "+hostname+" -n 1")
    else:
        response = system_command("ping -W -c 1 " + hostname)
    return {'avgping': response, 'host': hostname}



class Plugin(plugins.BasePlugin):


    def run(self, config):
        data = {}
        my_hosts = config.get('ping', 'hosts').split(',')
        data['ping'] = []
        for host in my_hosts:
            data['ping'].append(collect_ping(host))
        return data['ping']



if __name__ == '__main__':
    Plugin().execute()
