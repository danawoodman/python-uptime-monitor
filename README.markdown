# Python Uptime Monitor

## Description

Monitor a url to see if it is online. If it is does not return a 200 code, then (optionally) send an email out through GMail.

This script is especially useful if run periodically with Cron so that downtime can be caught quickly (more on this below).


## Usage

Usage is strait forward, just put the `uptime_monitor.py` file on the `PythonPath` and then import it and run the `monitor_uptime` method. 

Create a file somewhere that will call the `uptime_monitor.py` file, like your home folder (e.g. `/home/user/monitor_site.py`):

    import os
    import sys
    
    # Add path to the uptime_monitor.py file so we can import it.
    sys.path.append(os.path.abspath('~/uptime_monitor/'))
    
    from uptime_monitor import monitor_uptime
    
    # Check if the url is up.
    if not monitor_uptime("http://www.google.com/", 
                ["to_address@example.com", "3334445555@txt.att.net"], 
                "example@gmail.com", 
                "my_gmail_password"):
        # Do things here like restart the server, etc...

... where the first parameter is the url to check, the second is the list of recipient addresses to notify in case the site is down and the last two parameters are your GMail username and password respectively.

For safety, set the file permissions of the `monitor_site.py` file to only allow your user full access and other users execute only access:

    chmod 711 ~/monitor_site.py

You can now run:

    python ~/monitor_site.py

... to check if your site is online.

To make this script really useful though, run it from a crontab. First, edit your crontab file:

    crontab -e

Then add in a cronjob like this (note the first block is useful for referencing how to write a crontab job):

    # ------------- minute (0 - 59)
    # | ----------- hour (0 - 23)
    # | | --------- day of month (1 - 31)
    # | | | ------- month (1 - 12)
    # | | | | ----- day of week (0 - 6) (Sunday=0)
    # | | | | |
    # * * * * * command to be executed
    
    # Check the uptime of the website every minute.
    * * * * * /usr/local/bin/python2.6 ~/monitor_site.py

... where `/usr/local/bin/python2.6` is the location to your Python executable and `~/monitor_site.py` is the path to the `monitor_site.py` file. This will run the `monitor_site.py` every minute. You can schedule backups however often you want using crontab.

If you enable emails you'll get an email any time the site is down.


## Credits

Copyright &copy; 2011 Dana Woodman <dana@danawoodman.com>


## License

Released under an MIT license.
