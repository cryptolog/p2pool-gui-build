#!/usr/bin/python
# -*- coding: utf-8 -*-
# Setup script for p2pool-msi repository.

import os
import sys
import subprocess

repo = None

def run(cmdline):
    if repo:
        dispatch.dispatch(dispatch.request(cmdline))
    else:
        subprocess.check_call(['git'] + cmdline, shell=False)

repolist = {}
for line in open('repolist.txt', 'rb').readlines():
    line = line.strip()
    print line
    name, url = line.split(" = ")
    repolist[name] = url
    if not os.path.isdir(name):
        run(['clone', url, name])

if not repo:
    print 'Initial clones completed, exiting.'
    sys.exit(0)

repostates = {}
for line in open('repostate.txt', 'rb').readlines():
    line = line.strip()
    hash, name = line.split(' ')
    repostates[name] = hash

writefile = len(repolist) != len(repostates)
for name, url in repolist.iteritems():
    repo = hg.repository(ui.ui(), path=name)
    hash = repo['.'].hex()
    if hash != repostates.get(name):
        print name, 'has changed'
        repostates[name] = hash
        writefile = True

if writefile:
    fp = open('repostate.txt', 'wb')
    for name in sorted(repostates.keys()):
        if name in repolist:
            fp.write( '%s %s\n' % (repostates[name], name) )
    fp.close()
    print 'Updated repostate.txt'
else:
    print 'repostate.txt is up to date'
