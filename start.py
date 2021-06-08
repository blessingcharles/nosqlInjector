import argparse

from injector import Injector
from templates.banner import banner , print_line
from templates.colors import *

if __name__ == '__main__':

    print_line(blue,reset)
    banner(yellow,reset)
    print_line(blue,reset)

    parser = argparse.ArgumentParser(description="nosql injector automation")
    parser.add_argument("-u","--url",dest="url",help="enter a valid url")
    parser.add_argument("-d","--data" ,dest="data",help="provide the json params eg: -d email,password default[email,password]",default="email,password")
    parser.add_argument("-w","--wordlist",dest="wordlist",help="default set to [payloads/payload.txt]" , default="payloads/payload.txt")
    parser.add_argument("-A","--brute-force-admin",dest="admin",action="store_true",default=False,help="bruteforce for admin accounts [default false]")
    parser.add_argument("-dos",dest="dos",action="store_true",default=False,help="dos the server (works by injecting sleep() onlyif where query found) [default false]")
    parser.add_argument("-t",dest="threads",type=int,default=10,help="dos the server workers [default 10]")

    parser.add_argument("-v","--verbose",action="store_true",default=False,dest="verbose",help="set for verbose output")

    parser = parser.parse_args()

    url = parser.url 
    data = parser.data.split(",")
    wordlist = parser.wordlist
    verbose = parser.verbose
    admin = parser.admin
    dos = parser.dos
    threads = parser.threads

    if not url :
        print(f"{red}provide an url or try python3 injector.py --help {reset}")
        quit()


    injector = Injector(url,data,wordlist,verbose,threads)
    injector.start()

    if admin : injector.bruteforce_admin()
    if dos : injector.dos()

