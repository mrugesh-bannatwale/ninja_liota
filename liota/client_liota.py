import logging
from optparse import OptionParser

from liota.lib.transports.xmpp_1 import IOT_Device, XMPP

if __name__ == '__main__':
    # -------------------------------------------------------------------------------------------
    #   Parsing Arguments
    # -------------------------------------------------------------------------------------------
    optp = OptionParser()

    # Output verbosity options.
    optp.add_option('-q', '--quiet', help='set logging to ERROR',
                    action='store_const', dest='loglevel',
                    const=logging.ERROR, default=logging.INFO)
    optp.add_option('-d', '--debug', help='set logging to DEBUG',
                    action='store_const', dest='loglevel',
                    const=logging.DEBUG, default=logging.INFO)

    # JID and password options.
    optp.add_option("-j", "--jid", dest="jid",
                    help="JID to use")
    optp.add_option("-p", "--password", dest="password",
                    help="password to use")

    # IoT device id
    optp.add_option("-n", "--nodeid", dest="nodeid",
                    help="I am a device get ready to be called", default=None)

    opts, args = optp.parse_args()

    # Setup logging.
    logging.basicConfig(level=opts.loglevel,
                        format='%(levelname)-8s %(message)s')

    if opts.jid is None or opts.password is None or opts.nodeid is None:
        optp.print_help()
        exit()

    # -------------------------------------------------------------------------------------------
    #   Starting XMPP with XEP0030, XEP0323, XEP0325
    # -------------------------------------------------------------------------------------------

    # we bounded resource into node_id; because client can always call using static jid
    # opts.jid + "/" + opts.nodeid
    xmpp = XMPP(opts.jid + "/" + opts.nodeid, opts.password)
    xmpp.register_plugin('xep_0030')
    xmpp.register_plugin('xep_0323')
    xmpp.register_plugin('xep_0325')

    if opts.nodeid:
        myDevice = IOT_Device(opts.nodeid)
        xmpp['xep_0323'].register_node(nodeId=opts.nodeid, device=myDevice, commTimeout=10)
        while not (xmpp.testForRelease()):
            xmpp.connect()
            xmpp.process(block=True)
            logging.debug("lost connection")
