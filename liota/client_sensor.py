import logging
from optparse import OptionParser

from liota.lib.transports.xmpp_1 import XMPP
import liota.lib.transports.xmpp_1

if __name__ == '__main__':
    # -------------------------------------------------------------------------------------------
    #   Parsing Arguments
    # -------------------------------------------------------------------------------------------
    optp = OptionParser()

    # JID and password options.
    optp.add_option("-j", "--jid", dest="jid",
                    help="JID to use")
    optp.add_option("-p", "--password", dest="password",
                    help="password to use")

    # IoT sensor jid
    optp.add_option("-c", "--sensorjid", dest="sensorjid",
                    help="Another device to call for data on", default=None)

    # Output verbosity options.
    optp.add_option('-q', '--quiet', help='set logging to ERROR',
                    action='store_const', dest='loglevel',
                    const=logging.ERROR, default=logging.INFO)
    optp.add_option('-d', '--debug', help='set logging to DEBUG',
                    action='store_const', dest='loglevel',
                    const=logging.DEBUG, default=logging.INFO)

    opts, args = optp.parse_args()

    # Setup logging.
    logging.basicConfig(level=opts.loglevel,
                        format='%(levelname)-8s %(message)s')

    if opts.jid is None or opts.password is None or opts.sensorjid is None:
        optp.print_help()
        exit()

    # -------------------------------------------------------------------------------------------
    #   Starting XMPP with XEP0030, XEP0323, XEP0325
    # -------------------------------------------------------------------------------------------
    xmpp = XMPP(opts.jid, opts.password, opts.sensorjid)
    xmpp.register_plugin('xep_0030')
    xmpp.register_plugin('xep_0323')
    xmpp.register_plugin('xep_0325')

    if opts.sensorjid:
        logging.debug("will try to call another device for data")
        xmpp.connect()
        xmpp.process(block=True)
        logging.debug("ready ending")

    else:
        print "noopp didn't happen"
