#!/usr/bin/env python

import socket
import gzip
from StringIO import StringIO
import json
import pprint

  

class HoneyClient:

    def __init__(self, id):
        #todo - put in config or paramter
        self.TCP_IP = '130.'
        self.TCP_PORT = 8012
        self.BUFFER_SIZE = 1024


        self.id = str(id)
        self.nounce = 0
         #self.public_key = self.private_key.public_key


    #TODO
    def sign(self,message):    					  	
#		 key = open(privateKey, "r").read() '''xml reading folgt'''
#		 rsakey = RSA.importKey(key)
#		 signer = PKCS1_v1_5.new(rsakey)
#		 digest = SHA512.new()
#		 digest.update(b64decode(message))
#		 sign = signer.sign(digest)
#		 print b64encode(sign)end
    	str = ''
    	return str
   
    def do_request(self, request):
        self.nounce +=1
        request = str(self.nounce) + "|" + self.id + "|" + request + "<ENDOFDATA>"

        #TODO, use sha512 as hasing method

        #signature = self.private_key.sign(request)
        signature = ''
        request = signature + "|" + request

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.TCP_IP, self.TCP_PORT))
        s.send(request)
        data = s.recv(1024*64)
        s.close()
        
        
        
        return gzip.GzipFile(fileobj=StringIO(data)).read()

    def get_orderbook(self, honey_id):
        market = self.do_request("6|" + str(honey_id))
        market = json.loads(market.split("|")[-1])

        result = {}
        n = 0
        for i in market["OrdBStr"].split("~"):
            result[market["Ru"][n]["Name"]] = json.loads(i)
            n += 1

        return result
    
      


#MESSAGE = str(nounce) + "|234|"  + "GETPUBLICKEY<ENDOFDATA>"


MESSAGE = "|" +"1" + "|777888|"  + "1|29511823567<ENDOFDATA>"
MESSAGE = "|" +"1" + "|777888|"  + '''7|{"Cat":2,"FromID":0,"ToID":5}<ENDOFDATA>'''

''',"RunnerAND":null,"Title":null,"Comp":null,"TypeOR":null,"PeriodOR":null,"ToSettle":false,"OnlyMyCreatedMarkets":false,"ChangedAfter":"0001-01-01T00:00:00","OnlyActive":true,"FromClosT":"0001-01-01T00:00:00","ToClosT":"0001-01-01T00:00:00",'''

if __name__ == "__main__":
    print 'start'
    h = HoneyClient(777888)
    print h.do_request('''7|{"Comp":"Germany - Bundesliga", "MinPop":1,"NoZombie":true,"OnlyActive":true,"Cat":1,"FromID":0,"ToID":10}''')
    #print h.do_request('''6|30036717090<ENDOFDATA>''')
    #print h.get_orderbook(30036717090)

    #print gzip.GzipFile(fileobj=StringIO(data)).read()




   