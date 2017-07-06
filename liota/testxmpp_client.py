#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import logging
import getpass
import os
import ssl

from optparse import OptionParser

from liota.lib.transports.xmpp_1 import XMPP

if __name__ == '__main__':
    # Setup the command line arguments.
    optp = OptionParser()
    optp.version = '%%prog 0.1'
    optp.usage = "Usage: %%prog[options] <jid> " + \
                 'nodes|create|delete|purge|subscribe|unsubscribe|publish|retract|get' + \
                 ' [<node> <data>]'

    optp.add_option('-q', '--quiet', help='set logging to ERROR',
                    action='store_const',
                    dest='loglevel',
                    const=logging.ERROR,
                    default=logging.ERROR)
    optp.add_option('-d', '--debug', help='set logging to DEBUG',
                    action='store_const',
                    dest='loglevel',
                    const=logging.DEBUG,
                    default=logging.ERROR)
    optp.add_option('-v', '--verbose', help='set logging to COMM',
                    action='store_const',
                    dest='loglevel',
                    const=5,
                    default=logging.ERROR)

    # JID and password options.
    optp.add_option("-j", "--jid", dest="jid",
                    help="JID to use")
    optp.add_option("-p", "--password", dest="password",
                    help="password to use")
    opts, args = optp.parse_args()

    # Setup logging.
    logging.basicConfig(level=opts.loglevel,
                        format='%(levelname)-8s %(message)s')

    if len(args) < 2:
        optp.print_help()
        exit()

    if opts.jid is None:
        opts.jid = raw_input("Username: ")
    if opts.password is None:
        opts.password = getpass.getpass("Password: ")

    if len(args) == 2:
        args = (args[0], args[1], '', '', '')
    elif len(args) == 3:
        args = (args[0], args[1], args[2], '', '')
    elif len(args) == 4:
        args = (args[0], args[1], args[2], args[3], '')

    # Setup the Pubsub client
    xmpp = XMPP(opts.jid, opts.password,
                server=args[0],
                node=args[2],
                action=args[1],
                data=args[3])

    # If you are working with an OpenFire server, you may need
    # to adjust the SSL version used:
    xmpp.ssl_version = ssl.PROTOCOL_SSLv3

    # If you want to verify the SSL certificates offered by a server:
    # uopdate the directory path for certifaicate when it is created
    xmpp.ca_certs = "path/to/ca/cert"

    # Connect to the XMPP server and start processing XMPP stanzas.
    if xmpp.connect():
        # If you do not have the dnspython library installed, you will need
        # to manually specify the name of the server if it does not match
        # the one in the JID.
        xmpp.process(block=True)
    else:
        print("Unable to connect.")
