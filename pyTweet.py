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

if options.timeline:
	url = "http://twitter.com/statuses/public_timeline.json"
	response = make_request(url)
	print response.read()

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
