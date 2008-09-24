#!/usr/bin/python
# Todo: write function that takes care of authentication
# Function for authentication based on options or config file
  # If no l/p given, read from config file. If no config file available, exit with error. If store given with no l/p, exit with error. If store given with l/p, store to file

# Figure out how to parse JSON to present friends timeline
# Write a function that spits out one tweet from a timeline

# Figure out how to use subprocess to go to an editor and use that for the tweet
# Look into py2app. 

# Build up each tweet as an array with user (get_user), update (bold?) and date (formatted)

# What I want this program to do: default: tweet, -l list the friends timeline 
# with optional page argument, -l a particular user

# Check how long the message is. 

import sys
import os
import optparse
import urllib
import urllib2
import simplejson
import datetime
import time
import ConfigParser
from pprint import pprint

# Set the location for the configfile.
config_path = os.path.expanduser('~/.tweetrc')
update_url = "http://twitter.com/statuses/update.json"
friends_timeline_url = "http://twitter.com/statuses/friends_timeline.json"
user_timeline_url = "http://twitter.com/statuses/user_timeline.json"

# Set up the parser object to read command line options
# The value of the options are in options.DEST

usage = "Simply enter %prog to begin editing an update in $TWEET_EDITOR. If $TWEET_EDITOR is not available, $EDITOR will be used. Alternately, specify your update as an argument on the command line.\n"
usage += 'Use the "-l" option to dislpay your friends timeline, or specify "-l USER" for a particular user\'s timeline.' + "\n"
usage += "pytweet [-u USERNAME] [-p password] [UPDATE]\n"
usage += "pytweet -l [USER]"
parser = optparse.OptionParser(usage)
parser.add_option("-u", "--username", help="Your username or email address on Twitter.com",
			action="store", dest="username")
parser.add_option("-p", "--password", help="Your password on Twitter.com", dest="password")
parser.add_option("-l", "--list", help="Display your friends timeline, or specify a user to display their updates.", action="store_true", dest="list", metavar="USER")

(options, args) = parser.parse_args()


"""
 # Testing for an editor environment variable
if os.environ.__contains__("TWEET_EDITOR"):
        print "there's a tweet editor"
elif os.environ.__contains__("EDITOR"):
	print "generic editor"
else:
	print "no editor"
"""

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
def public():
	if options.timeline:
		url = "http://twitter.com/statuses/public_timeline.json"
		response = make_request(url)
		print response.read()

# A function to take care of extracting l/p with logic.
# ? Would it be cleaner to use ConfigParser defaults rather than this elaborate logic? Probably not. 
# Make this return an associative array of l/p in addition to printing.
# Read about error handling

def get_login():
	if os.path.isfile(config_path) == False: # No config file
		if options.username and options.password: # Command line options
			print ">>> Username and password specified on command line. Saving to .twitterrc."
			config_file = open(config_path, 'w')
			f = ConfigParser.ConfigParser()
			f.add_section('authentication')
			f.set('authentication','username', options.username)
			f.set('authentication','password', options.password)
			f.write(config_file)
			config_file.close()
			return { 'username': options.username, 'password': options.password }
		elif options.username or options.password: # One but not the other
			print ">>> You must provide both a login and a password, or neither."
		else: # No command line options
			print ">>> No username and password specified and no config file available. No tweet."
			return False;
	elif  os.path.isfile(config_path) == True: # We have a config file
		if options.username and options.password: # With command line options
			print ">>> Username and password specified on command line, overriding .twitterrc"
			return { 'username': options.username, 'password': options.password }
		elif options.username or options.password: # One but not the other
			print ">>> You must provide both a login and a password, or neither."
		else:
			print ">>> Reading username and password from .twitterrc"
			config_file = open(config_path, 'r')
			f = ConfigParser.ConfigParser()
			f.read(config_path)
			username = f.get('authentication', 'username')
			password = f.get('authentication', 'password')
			config_file.close()
			return { 'username': username, 'password': password }
	else:
		print "Another combo altogether?"


# Tweet!
def tweet(status):
	login = get_login()
	password_manager = urllib2.HTTPPasswordMgrWithDefaultRealm()
        password_manager.add_password(None, update_url, login['username'], login['password'])
        handler = urllib2.HTTPBasicAuthHandler(password_manager)
        opener = urllib2.build_opener(handler)
        urllib2.install_opener(opener)
	data = "status=" + urllib.quote_plus(status) # Encode the output for use as POST
	response = make_request(update_url,data)
        if response:
                output = response.read() # This captures it but also makes the tweet happen
		print output

# Takes a tweet and processes it
def format_tweet(tweet):
	return pprint(tweet)


# With a straggler argument, two things could be happening. Either we are trying
# to tweet or we are providing an argument to --list, meaning we want to show 
# a particular user's timeline.
if args:
	if options.list == None:
		tweet(args[0])
	elif options.list == True:
		get_user_timeline()




# Test json parsing
file = open('timeline.json')
json = simplejson.load(file)
print json[1]['text']
"""i = 1
for tweet in json:
	print i
	print tweet
	i = i + 1
	"""

# Take the "Sun Sep 14 19:24:43 +0000 2008" that twitter uses
# and convert that to time since epoch in seconds.
def parse_twitter_date(timestamp):
        return int(time.mktime(time.strptime(timestamp, "%a %b %d %H:%M:%S +0000 %Y")))

# Take time in seconds and convert to minutes, hours, seconds as appropriate.
# Let this take either the string or the seconds, still the same clean format.
# Figure out how to handle plural vs. singular units
def format_time(seconds):
        if seconds < 60: # under a minute
                return str(seconds) + " seconds"
        elif seconds < 3600: # under an hour
                return str(seconds / 60) + " minutes"
        elif seconds < 86400: # under a day
                return str((seconds / 60) / 60) + " hours"
        elif seconds >= 86400: # over a day ago
                return str(((seconds / 60) / 60 ) / 24) + " days"
        else:
                return seconds

def get_username(userid):
        response_file = make_request("http://twitter.com/users/show/" + str(userid) + ".json")
        response_parsed = simplejson.load(response_file)
        return response_parsed['name']

def get_user_timeline():
	return "hi"



#if options.list:
def get_friends_timeline():
	login = get_login()
	#timeline = make_request(friends_timeline_url)
	password_manager = urllib2.HTTPPasswordMgrWithDefaultRealm()
        password_manager.add_password(None, friends_timeline_url, login['username'], login['password'])
        handler = urllib2.HTTPBasicAuthHandler(password_manager)
        opener = urllib2.build_opener(handler)
        urllib2.install_opener(opener)
	# data = "status=" + urllib.quote_plus(status) # Encode the output for use as POST
	response = make_request(friends_timeline_url)
	json = simplejson.load(response)
	print ">>> Getting friends timeline"
	pprint(json)

def get_user_timeline(user):
	timeline = make_request(user_timeline_url, "id=" + user)
	json = simplejson.load(timeline)
	print ">>> Printing user timeline"
	print json





'''
now = int(time.mktime(time.gmtime()))
#now = time.gmtime(now)
for i in json:
#       pprint(i)
       print print_tweet(i)
       diff = now - parse_twitter_date(i['created_at'])
       print str(format_time(diff)) + " ago"
       print (diff)
       print i['created_at']
       print "\n"

date = json[-2]['created_at']
print date
date = time.strptime(date, "%a %b %d %H:%M:%S +0000 %Y")
print date
date = int(time.mktime(date))
'''
