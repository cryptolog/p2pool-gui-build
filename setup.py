#!/usr/bin/python
# -*- coding: utf-8 -*-
# Setup script for p2pool-msi repository.

import os
import sys
import git

repolist = {}
for line in open('repolist.txt', 'rb').readlines():
    line = line.strip()
    name, url = line.split(" = ")
    print 'Checking out ' + name + ' from ' + url
    repolist[name] = url
    repo = git.Repo('./')
    if not os.path.isdir(name):
        repo.git.clone(url, name)

repostates = {}
for line in open('repostate.txt', 'rb').readlines():
    line = line.strip()
    hash, name = line.split(' ')
    repostates[name] = hash

writefile = len(repolist) != len(repostates)
for name, url in repolist.iteritems():
    repo = git.Repo(name)
    hash = str(repo.rev_parse('HEAD'))
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
