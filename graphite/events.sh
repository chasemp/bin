#!/bin/bash
curl -X POST http://graphite.da/events/ -d '{"what": "did_stuff99", "tags" : "fun"}'
