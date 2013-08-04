#!/usr/bin/env python
"""
Create a blogging config in your home dir like: /Users/<user>/.blogpy.ini
[DEFAULT]
cmd used to open the editor
editor = nano +7
path to mynt generated files and templates
mynt_root = /Users/<user>/blog/
posts_dir = _posts
path to webroot
webroot = /Users/<user>/git/chasemp/
"""

import sys
import os
import tempfile
import datetime
import argparse
import os.path as p
import StringIO
from ConfigParser import SafeConfigParser

parser = argparse.ArgumentParser(description='blogging from cli')
parser.add_argument('-t', action="store", dest="title", help='blog title')
parser.add_argument('-a', action='store', dest='assoc',
                    default='',
                    help='Add repeated values to a list',
                    )
parser.add_argument("--deploy", help="deploys only",  action="store_true")
parser.add_argument("--show", help="show only",  action="store_true")


def build():
    os.system('mynt gen -f %s %s' % (mynt_root, webroot))

def deploy():
    build()
    os.chdir(webroot)
    print os.system('git add -A')
    print os.system("git commit -m '%s'" % args.title)
    print os.system('git push origin master')

def show():
    build()
    try:
        os.system('mynt serve %s' % (webroot))
    except socket.error:
        'socket in use!'

def username():
    return os.getenv('USER')


#Get configuration from user config file
home = os.path.expanduser('~')
config_file = os.path.join(home, '.blogpy.ini')
fparser = SafeConfigParser()
fparser.read(config_file)
editor = fparser.get('DEFAULT', 'editor')
mynt_root = fparser.get('DEFAULT', 'mynt_root')
posts_dir = fparser.get('DEFAULT', 'posts_dir')
webroot = fparser.get('DEFAULT', 'webroot')

args = parser.parse_args()
if args.deploy:
    deploy()
    sys.exit(0)
elif args.show:
    show()
    sys.exit(0)
elif not args.title:
    parser.print_help()
    sys.exit(1)

output = StringIO.StringIO()
now = datetime.datetime.now()

base = """---
layout: post.html
title: %s
tags: [%s]
---""" % (args.title.replace('-', ' '), args.assoc)
month = '{0}'.format(str(now.month).zfill(2))
day = '{0}'.format(str(now.day).zfill(2))
filename = "%s-%s-%s-%s.md" % (now.year, month, day, args.title)
mynt_root = p.join(mynt_root, posts_dir)
new_post =  p.join(mynt_root, filename)
f = tempfile.NamedTemporaryFile(delete=False)
with open(f.name, 'a') as f:
    f.write(base)
os.system('%s %s' % (editor, f.name))
f.close()

with open(f.name, 'r') as f:
    blog_post = f.read()

if not blog_post:
    print 'blog post empty bailing!'
    sys.exit(0)

output.write(blog_post)
print 'new blog post found!', new_post

with open(new_post, 'w') as f:
    f.write(output.getvalue())

print open(new_post, 'r').read()
