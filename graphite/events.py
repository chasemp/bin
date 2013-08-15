#!/usr/bin/env python
import json
import urllib2

one = {'what': 'did_it', 'tags' : 'fun'}
req = urllib2.Request('http://graphite.da/events/',
                      data=json.dumps(one),
                      headers={'Content-type': 'text/plain'})
r = urllib2.urlopen(req)

print r.read()


