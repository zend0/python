#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This script converts the existing crontab file into the yaml file for ansible
run: cron_to_ansible.py <your_crontab_file>
"""

import sys
import re


class CronConverter:

    def __init__(self):
        self.envs = dict()
        self.tasks = list()
        self.taskid = 0

    def job_format(self, x):
        return "{0}".format(x) if x.isdigit() else "'{0}'".format(x)

    def env_add(self, k, v):
        self.envs[k] = "'{0}'".format(v) if v.startswith('"') and v.endswith('"') else v

    def env_list(self):
        if len(self.envs) > 0:
            print("\x1b[33mcron_vars:\x1b[0m")
            for k, v in self.envs.items():
                print(' '*2 + '- name: {0}\n'.format(k) + ' '*4 + 'value: {0}'.format(v))

    def task_add(self, mi, h, d, mo, w, j):
        task = ['name: {0} #{1}'.format(sys.argv[1], self.taskid)]
        if mi != '*':
            task.append('minute: {0}'.format(self.job_format(mi)))
        if h != '*':
            task.append('hour: {0}'.format(self.job_format(h)))
        if d != '*':
            task.append('day: {0}'.format(self.job_format(d)))
        if mo != '*':
            task.append('month: {0}'.format(self.job_format(mo)))
        if w != '*':
            task.append('weekday: {0}'.format(self.job_format(w)))
        task.append('job: {0}'.format(j))

        self.tasks.append(task)
        self.taskid += 1

    def task_list(self):
        if len(self.tasks) > 0:
            print("\x1b[33mcron_jobs_for_host:\x1b[0m")
            for t in self.tasks:
                for v in range(len(t)):
                    if v == 0:
                        print(' '*2 + '- {0}'.format(t[v]))
                    else:
                        print(' ' * 4 + '{0}'.format(t[v]))


if __name__ == "__main__":
    converter = CronConverter()
    try:
        with open(sys.argv[1]) as cron:
            for line in cron:
                line = line.strip()
                if len(line) > 0 and not line.startswith('#'):
                    if re.match(r'^[A-Z]+[ ]?=[ ]?.*', line) is not None:
                        result = re.match(r'(^[A-Z]+)[ ]?=[ ]?(.*)', line)
                        converter.env_add(result.group(1), result.group(2))
                    else:
                        minute, hour, day, month, weekday = line.split()[:5]
                        job = ' '.join(line.split()[5:])
                        converter.task_add(minute, hour, day, month, weekday, job)
    except Exception as e:
        sys.exit("\x1b[91mERROR: {0}\x1b[0m".format(e))

    converter.env_list()
    converter.task_list()
