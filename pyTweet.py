#!/usr/bin/python
# Todo: write function that takes care of authentication
# Function for authentication based on options or config file
  # If no l/p given, read from config file. If no config file available, exit with error. If store given with no l/p, exit with error. If store given with l/p, store to file

# Figure out how to parse JSON to present friends timeline
# Write a function that spits out one tweet from a timeline

import sys
from optparse import OptionParser
import urllib2
from pprint import pprint
import simplejson
import datetime
import time
import ConfigParser

# Set up the parser object to read command line options
# The value of the options are in options.DEST

parser = OptionParser()
parser.add_option("-t", "--tweet", help="The text of your status update on Twitter.com",
			action="store", dest="update")
parser.add_option("-u", "--username", help="Your username or email address on Twitter.com",
			action="store", dest="username")
parser.add_option("-p", "--password", help="Your password on Twitter.com", dest="password")
parser.add_option("-s", "--store", help="Save the login and password data to ~/.pytweetrc to use next time", action="store_true", dest="store")
parser.add_option("-a", "--all", help="View Twitter.com's public timeline",
			action="store_true", dest="timeline")

(options, args) = parser.parse_args()

# Provide a URL and get in return a response
def make_request(url, data=None):
	req = urllib2.Request(url, data)
        try:
                response = urllib2.urlopen(req)
        except IOError, e:
            if hasattr(e, 'reason'):
                print 'We failed to reach a server.'
                print 'Reason: ', e.reason
            elif hasattr(e, 'code'):
                print 'The server couldn\'t fulfill the request.'
                print 'Error code: ', e.code
        else:
                return response

# Take an element of the JSON object and pretty-print it
def print_tweet(tweet):
        return tweet['user']['name'] + ": " + tweet['text'] +"\n" + tweet['created_at'] + " in reply to " + str(tweet['in_reply_to_user_id']) + "\n"

# Show the public timeline.
if options.timeline:
	url = "http://twitter.com/statuses/public_timeline.json"
	response = make_request(url)
	print response.read()

# Tweet!
if options.update:
	url = "http://twitter.com/statuses/update.xml"
	password_manager = urllib2.HTTPPasswordMgrWithDefaultRealm()
        password_manager.add_password(None,url,options.username,options.password)
        handler = urllib2.HTTPBasicAuthHandler(password_manager)
        opener = urllib2.build_opener(handler)
        urllib2.install_opener(opener)
	data = "status=" + options.update
	response = make_request(url,data)
        if response:
                print response.read()

file = open('timeline.json')
json = simplejson.load(file)


# Take the "Sun Sep 14 19:24:43 +0000 2008" that twitter uses
# and convert that to time since epoch in seconds.
def parse_twitter_date(timestamp):
        return int(time.mktime(time.strptime(timestamp, "%a %b %d %H:%M:%S +0000 %Y")))

# Take time in seconds and convert to minutes, hours, seconds as appropriate.
# Let this take either the string or the seconds, still the same clean format.
def format_time(seconds):
        if seconds <= 60: # under a minute
                return str(seconds) + " seconds"
        elif seconds <= 3600: # under an hour
                return str(seconds / 60) + " minutes"
        elif seconds <= 216000: # under a day
                return str((seconds / 60) / 60) + " hours"
        elif seconds > 5184000:
                return str(((seconds / 60) / 60 ) / 12) + " days"
        else:
                return seconds

now = int(time.mktime(time.gmtime()))
#now = time.gmtime(now)
for i in json:
#       pprint(i)
       print print_tweet(i)
       print format_time(now - parse_twitter_date(i['created_at']))
       print i['created_at']
       print "\n"

date = json[-2]['created_at']
print date
date = time.strptime(date, "%a %b %d %H:%M:%S +0000 %Y")
print date
date = int(time.mktime(date))


f = ConfigParser.ConfigParser()
print f.read(".pytweetrc")
print f.items('authentication')

if options.username and options.password and options.store:
        my_config = file('pytweetrc', 'w')
        f = ConfigParser.ConfigParser()
        f.add_section('authentication')
        f.set('authentication','username','options.username')
        f.set('authentication','password','options.password')
        f.write(config)
