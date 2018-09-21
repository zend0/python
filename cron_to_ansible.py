#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys


def job_format(x):
    return "{}".format(x) if x.isdigit() else "'{}'".format(x)

def gen_ansible_task(mi, h, d, mo, w, j):
    task = ''
    if mi != '*':
        task +=  ' '*4 + 'minute: {}\n'.format(job_format(mi))
    if h != '*':
        task +=  ' '*4 + 'hour: {}\n'.format(job_format(h))
    if d != '*':
        task +=  ' '*4 + 'day: {}\n'.format(job_format(d))
    if mo != '*':
        task +=  ' '*4 + 'month: {}\n'.format(job_format(mo))
    if w != '*':
        task +=  ' '*4 + 'weekday: {}\n'.format(job_format(w))
    task += ' '*4 + 'job: {}'.format(j)
    return task


if __name__ == "__main__":
    try:
        with open(sys.argv[1]) as cron:
            count= 0
            for line in cron:
                line = line.strip()
                if len(line) > 0 and not line.startswith('#'):
                    minute, hour, day, month, weekday = line.split()[:5]
                    job = ' '.join(line.split()[5:])
                    print('  - name: {} #{}\n'.format(sys.argv[1], count) + gen_ansible_task(minute, hour, day, month, weekday, job))
                    count += 1
    except Exception as e:
        sys.exit("\033[91mERROR: %s\033[0m" % (str(e)))
