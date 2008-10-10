Tweets
1. Introduction
2. Dependencies
3. Usage
4. Notes
5. License

1. Introduction

Tweets is a command-line client for Twitter.com written in Python. It supports
viewing a user's friends timeline, user timelines, and updating a user's status.

2. Dependencies

Tweets is written in Python, so you must have Python installed in order to run
it. Tweets also requires the simplejson module for Python, for parsing the
JavaScript Object Notation (JSON) data that Twitter.com returns. This module is
available at ____ and will be included in the standard library of Python 2.6.

3. Usage

Using Tweets is simple. To view a user's timeline:
$ tweets -l xyzuser
Where xyzuser is a username whose timeline you would like to view.

To view your friends timeline:
$ tweets -u myusername -p mypassword -l
Where mysuername and mypassword correspond to the username and password for your
account on Twitter.com. 

To update your status:
$ tweets 'Writing the README file for tweets'
Note that using double quotes will allow shell expansion of $, !, and other
special characters, so in most cases, single quotes are preferable.

After you supply a username and password to Tweets once, it stores this
information in ~/.tweetsrc so that you don't have to type it out
each time. 

4. Notes
Tweets was written by Alexander Kahn (alexanderkahn@gmail.com). Thank you to
everyone who helped me in this process, including users of #python on 
irc.freenode.net. Thanks to Stuart Colville (http://url), author of TweetyPy,
for inspiration, and to Hamish Lawson for TextFormatter.py (http://url).

Future versions of Tweets will make use of the Twitter.py API module.

If you'd like to contribute code or ideas, please file a pull request at GitHub (http://url)
or contact me at alexanderkahn@gmail.com.

5. License
Tweets is licensed under the GNU General Public License (GPL) Version 3. 

