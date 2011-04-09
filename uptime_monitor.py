#!/usr/bin/python

def color_print(msg, color=None):
    """
    Print colored console output.
    
    Color choices are: 
        'gray'
        'green'
        'red'
        'yellow'
        'purple'
        'magenta'
        'cyan'
    
    Example::
        color_print("Here is a message...", 'red')
    """
    if not msg:
        print "You must pass a message to the color_print function!"
        return
    
    # Declare closing.
    end = '\033[0m'
    
    # Declare print colors.
    colors = {
        'gray': '\033[90m',
        'green': '\033[92m',
        'red': '\033[91m',
        'yellow': '\033[93m',
        'purple': '\033[94m',
        'magenta': '\033[95m',
        'cyan': '\033[96m',
    }
    
    if color in colors.keys():
        print colors[color] + str(msg) + end
    else:
        print msg

def mail(gmail_user, gmail_pw, to, subject='(No Subject)', text='', html=None, attach=None):
    """
    Send email through google.
    """
    import smtplib
    from email.MIMEMultipart import MIMEMultipart
    from email.MIMEBase import MIMEBase
    from email.MIMEText import MIMEText
    from email import Encoders
    
    if html:
        msg = MIMEMultipart('alternative')
    else:
        msg = MIMEMultipart()
        
    # Check to see if they entered a GMail user/password, which is required.
    if not gmail_user and not gmail_pw:
        print """You must supply a GMail username (gmail_user) and 
password (gmail_pw) to send an email!"""
        return
        
    msg['From'] = gmail_user
    msg['To'] = to
    msg['Subject'] = subject
    
    if html:
        msg.attach(MIMEText(html, 'html'))
        
    msg.attach(MIMEText(text, 'text'))
    
    # Attach the file, if given.
    if attach:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(open(attach, 'rb').read())
        Encoders.encode_base64(part)
        part.add_header('Content-Disposition',
           'attachment; filename="%s"' % os.path.basename(attach))
        msg.attach(part)
        
    mailServer = smtplib.SMTP("smtp.gmail.com", 587)
    mailServer.ehlo()
    mailServer.starttls()
    mailServer.ehlo()
    mailServer.login(gmail_user, gmail_pw)
    mailServer.sendmail(gmail_user, to, msg.as_string())
    # Should be mailServer.quit(), but that crashes...
    mailServer.close()
    
    # Log message to console.
    color_print('\nMessage sent!', 'green')
    color_print('    To: %s\n    Subject: %s' % (msg['To'], msg['Subject']), 'green')

def monitor_uptime(url, recipients=None, gmail_user=None, gmail_pass=None):
    """
    Monitor a url to see if it is online. If it is does not return a 200 code, 
    then (optionally) send an email out through GMail.
    
    Example::
        monitor_uptime("http://www.google.com/", 
                    ["to_address@example.com", "3334445555@txt.att.net"], 
                    "example@gmail.com", 
                    "my_gmail_password")
    """
    from datetime import datetime, timedelta
    import httplib
    from urlparse import urlparse
    
    color_print("\nChecking if %s is online" % url, 'green')
    
    # Connect to the url and get it's status and other details.
    site = urlparse(url)
    conn = httplib.HTTPConnection(site[1])
    conn.request("HEAD", site[2])
    status = conn.getresponse()
    status_code = status.status
    
    # Get the clean URL (without protocol)
    full_url = site.geturl()
    clean_url = site.netloc + site.path
    
    # If the request was anything but a 200/302 code (meaning the site is up), 
    # log and report the downtime.
    if status_code != (200 || 302):
        
        color_print("\nSite is down with a %s error code\n" % status_code, 'red')
        
        # If they have set up email sending, send out a message.
        if recipients and gmail_user and gmail_pass:
            
            # Construct the subject and message.
            subject = "%(site)s is down!!! (code %(code)s)" % {
                'site': clean_url,
                'code': status_code,
            }
            msg_text = """%(site)s is down with status code %(code)s!""" % {
                'site': full_url,
                'code': status_code,
            }
            msg_html = """<p><strong>%(site)s is down status code %(code)s!</strong></p>""" % {
                'site': full_url,
                'code': status_code,
            }
            
            # Send the message to all the recipients.
            recipients = recipients if not isinstance(recipients, basestring) else [recipients]
            for to_address in recipients:
                mail(gmail_user, gmail_pass, to_address, subject, msg_text, msg_html)
            color_print("\nNotification sent!\n", 'green')
            
        # Return False so that we can do something if the site is down.
        return False
    
    # If the status_code is 200, then the site is up
    color_print("\nSite is online (status 200)!\n", 'green')
    
    # Return true if 
    return True
