import socket
import json
import pprint

MESSAGE = "|" +"1" + "|777888|"  + '''7|{"Comp":"Germany - Bundesliga 2", "MinPop":0,"NoZombie":true,"OnlyActive":true,"Cat":1,"FromID":0,"ToID":40}<ENDOFDATA>'''

''',"RunnerAND":null,"Title":null,"Comp":null,"TypeOR":null,"PeriodOR":null,"ToSettle":false,"OnlyMyCreatedMarkets":false,"ChangedAfter":"0001-01-01T00:00:00","OnlyActive":true,"FromClosT":"0001-01-01T00:00:00","ToClosT":"0001-01-01T00:00:00",'''


print "start"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("130.", 8012))
s.send(MESSAGE)
data = s.recv(64*16384)
s.close()

import gzip
from StringIO import StringIO
result = gzip.GzipFile(fileobj=StringIO(data)).read()
events = json.loads(result.split("|")[-1])


print len(events)


result_list = []

for e in events:
    if e["OrdBStr"] != "~":
        #pprint.pprint(e)
        new_event = {}

        #category: sport
        new_event["categories"] = [3]

        new_event["closing_date"] = e["ClosD"]
        new_event["resolution_date"] = e["SettlD"]


        if e["Comp"] == "Germany - Bundesliga" and e["Descr"] == "Match":
            new_event["source_url"] = "http://www.bundesliga.com/en/"
            new_event["tags"] = [18]
            new_event["title"] = e["Title"]
            new_event["description"] = "What will be the outcome of the Bundesliga match: " + e["Title"] +"?"

            outcome_list = [{},{},{}]
            outcome_list[0]["name"] = e["Ru"][0]["Name"]
            outcome_list[1]["name"] = e["Ru"][1]["Name"]
            outcome_list[2]["name"] = e["Ru"][2]["Name"]
            new_event["outcome_names"] = outcome_list

        else:
            print "No rules for:" +  e["Comp"] + e["Descr"]
            continue

        #print e["OrdBStr"]
        new_event["order_book"] = {}
        n = 0
        for i in e["OrdBStr"].split("~"):
            new_event["order_book"][e["Ru"][n]["Name"]] = json.loads(i)
            n += 1

        #new_event["order_book"] = json.loads(str(e["OrdBStr"].split("~")))


         #pprint.pprint(new_event)
         #pprint.pprint(new_event)
         #print json.dumps(new_event)
        #new_event_ = f.create_event(json.dumps(new_event))
        #print new_event_
        result = {}
        #result["id"] = new_event_["id"]
        result["order_book"] = new_event["order_book"]
        result["id_honey"] = e["ID"]
        result_list.append(result)

print result_list