#!/usr/bin/python
import requests
import argparse
import os, sys

parser = argparse.ArgumentParser(description='Subdomain brute forcer.')
parser.add_argument('-w', action='store', dest='w', help='path to the wordlist')
parser.add_argument('-d', action='store', dest='d', help='base domain to brute (ex: google.com')
parser.add_argument('-o', action="store", dest='o', help="output file")
args = parser.parse_args()

# Set wordlist
if not args.w:
    wl = raw_input("Enter path to word list: ")
else:
    wl =  args.w

if not os.path.isfile(wl):
    sys.exit("Could not locate " + wl + ", file not found.")
else:
    try:
        f = open(wl, "r")
        wordlist = f.readlines()
    except:
        sys.exit("Could not open " + wl)

# Check for target domain
if not args.d:
    domain = raw_input("Enter target domain (EX: google.com): ")
else:
    domain = args.d

# Check for output file
if not args.o:
    outfile = raw_input("Enter output filename: ")
else:
    outfile = args.o

if not os.path.isfile(outfile):
    lf = open(outfile, "a")
    lf.write("Log Created\n")
else:
    lf = open(outfile, "a")

# Loop through word list and brute domains
for word in wordlist:
    #print "Checkingword.strip() + "." + domain
    chd = "http://" + word.strip() + "." + domain
    try:
        r = requests.get(chd, timeout=2)
        lf.write(chd+"\n")
        print chd + " found live. Added to log."
    except:
        print "No response from " + chd


