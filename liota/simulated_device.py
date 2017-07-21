import random
import time
from liota.device_comms.xmpp_device_comms import XmppDeviceComms


def simulated_event_device():
    xmpp_conn = XmppDeviceComms("bob@127.0.0.1", "m1ndst1x", "127.0.0.1", "5222")
    # xmpp_conn.create_node("pubsub.127.0.0.1", "/vmware11")
    n = 0
    while (n < 6):
        n = n + 1
        time.sleep(2)
        random_no = random.randint(1, 300)
        xmpp_conn.publish("pubsub.127.0.0.1", "/vmware11", "hello" + str(random_no))


if __name__ == "__main__":
    try:
        simulated_event_device()
    except:
        print "failed"
