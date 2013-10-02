import logging
import re
import webapp2

from google.appengine.api import mail
from google.appengine.ext.webapp.mail_handlers import InboundMailHandler

from config import *

p_to = re.compile('^FwdTo: ([\w\.@]+)$')
p_cc = re.compile('^FwdCc: ([\w\.@]+)$')
p_bcc = re.compile('^FwdBcc: ([\w\.@]+)$')
p_key = re.compile('Key: ([^ .]+)$')

class RelayHandler(InboundMailHandler):
    def receive(self, mail_message):
        logging.info('Received mail from ' + mail_message.sender)
        
        to = []
        cc = []
        bcc = []
        key = ''
        
        raw = str(mail_message.body)
        body = ''
        
        for line in raw.split('\n'):
            line = line.strip()
            
            m = p_to.match(line)
            
            if m is not None:
                to.append((m.group(0), m.group(1),))
                continue
            
            m = p_cc.match(line)
            
            if m is not None:
                cc.append((m.group(0), m.group(1),))
                continue
            
            m = p_bcc.match(line)
            
            if m is not None:
                bcc.append((m.group(0), m.group(1),))
                continue
            
            m = p_key.match(line)
            
            if m is not None:
                key = m.group(1)
                continue
            
            body += line + '\n'
        
        if key == appkey:
            if to or cc or bcc:
                message = mail.EmailMessage(sender=originator, subject=mail_message.subject)
                message.body = body.lstrip()
                
                if to:
                    message.to = [addr[1] for addr in to]
                
                if cc:
                    message.cc = [addr[1] for addr in cc]
                
                if bcc:
                    message.bcc = [addr[1] for addr in bcc]
                
                logging.info('Forwarding mail to recipients')
                
                message.send()
            else:
                logging.info('Dropping mail (no forward recipients)')
        else:
            logging.info('Dropping mail (invalid application key)')


app = webapp2.WSGIApplication([RelayHandler.mapping()], debug=False)
