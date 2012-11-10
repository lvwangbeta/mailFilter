# -*- coding: utf-8 -*-

import imaplib
import email

def open_connection(host, user,  password):
    print 'Connecting to ', host
    connection = imaplib.IMAP4_SSL(host)
    print 'Login as ', user
    connection.login(user, password)
    return connection

if __name__ == '__main__':
    c = open_connection('imap.gmail.com', 'mailaddress', 'password')
    print c.list()
    try:
        c.select('INBOX', readonly=True)
        type, msg_ids = c.search(None, 'ALL')
        print type, msg_ids
        for num in msg_ids[0].split(' '):
            typ, msg_data = c.fetch(num, 'RFC822')           
            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_string(response_part[1])
                    for part in msg.walk():
                        if  part.get_content_type() == 'text/plain':
                            f = open("./username/" + num + r".txt", 'w')
                            f.write(part.get_payload(decode=True))
                            f.close()
                            
            print num
                                  
    finally:
        try:
            c.close()
        except:
            pass
        c.logout()
