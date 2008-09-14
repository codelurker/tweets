#!/usr/bin/python

import sys
from optparse import OptionParser
import urllib2

# Set up the parser object to read command line options
# The value of the options are in options.DEST

parser = OptionParser()
parser.add_option("-t", "--tweet", help="The text of your status update on Twitter.com",
			action="store", dest="update")
parser.add_option("-u", "--username", help="Your username or email address on Twitter.com", 
			action="store", dest="username")
parser.add_option("-p", "--password", help="Your password on Twitter.com", dest="password")
parser.add_option("-a", "--all", help="View Twitter.com's public timeline", 
			action="store_true", dest="timeline")

(options, args) = parser.parse_args()

# Provide a URL and get in return a response
def make_request(url):
	req = urllib2.Request(url)
	response = urllib2.urlopen(req)
	return response

if options.timeline:
	url = "http://twitter.com/statuses/public_timeline.rss"
	timeline = make_request(url)
	print timeline.read()

