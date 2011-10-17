# Why?
I got tired of having to come inside to change the song that
was on Spotify, modify the volume, etc.  I couldn't find any good
iphone apps to do this for me, so I wrote this thing that runs as a webapp
you can access from your iphone.

# How?
The main file runs on the same machine as Spotify, and basically
just receives web requests, executes applescript that does the actions you tell it, queries
information from Spotify, etc, then renders HTML for an iphone.

At first I tried writing it in PHP and just running on Apache, but doing
that means that whatever applescript you execute runs as the Apache user,
which (rightfully) doesn't have permissions to touch Spotify.  So instead
I wrote it with Tornado in Python.

# How to use
0.  Install Tornado (http://www.tornadoweb.org/)
1.  Start up Spotify.
2.  Run `python spotnado.py`
3.  Hit http://<your computer's IP>:8888 from your iphone or browser
