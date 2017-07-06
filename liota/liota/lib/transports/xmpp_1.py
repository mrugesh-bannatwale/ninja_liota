
import logging

import os
import ssl
import time

import socket
import sys

from liota.lib.utilities.utility import systemUUID
from sleekxmpp.xmlstream import ET, tostring
from sleekxmpp.clientxmpp import ClientXMPP
from sleekxmpp.plugins.xep_0323.device import Device

log = logging.getLogger(__name__)


def auto_generate_jabber_id(edge_system_name, server_name):
    """

    :param edge_system_name:
    :return: return auto generated jabberID
    """
    return systemUUID().get_uuid(edge_system_name) + "@" + server_name


class XMPP(ClientXMPP):
    """
    XMPP Transport implementation for LIOTA. It internally uses Python SleekXMPP library.
    """
    #change this init method according to your project.......
    # more parameters changes to be done then cross check it with mqtt and xmlstream......
    def __init__(self, jid, password, server, host='', port=0, ssl_conf=False,
                   tls_conf=True, reattempt=True, node=None, action='list', data=''):
        """
        :param jid: system id name assigned to sensor
        :param password: for authentication into server
        :param server: where you send data for liota to catch it
        :param host: specifying jabberid full name url
        :param port: assigning port for connection with server
        :param ssl_conf: certification assigning from conf file
                         and verify it with local dir cert file
        :param tls_conf: transport layer security file??
        :param reattempt: try reconnecting again and check status
        :param node: create node for client service invocation
        :param action: what do you want the created node to do
        :param data: actual data to be sent to cloud via liota gateway
        """
        self.register_plugin('xep_0030')
        self.register_plugin('xep_0059')
        self.register_plugin('xep_0060')

        self.host = host
        self.port = port
        self.tls_conf = tls_conf
        self.ssl_conf = ssl_conf
        self.reattempt = reattempt
        self.jid = jid
        self.password = password
        self.pubsub_server = server
        self.node = node
        self.data = data
        self.action = action
        self.actions = ['nodes', 'create', 'delete',
                        'publish', 'get', 'retract',
                        'purge', 'subscribe', 'unsubscribe']

        self.add_event_handler('session_start', self.start, threaded=True)
        super(XMPP, self).__init__(jid, password)
        self.connect_soc()

    def connect_soc(self):
        ClientXMPP.connect(self, address=(self.host, self.port), reattempt=True,
                                           use_tls=True, use_ssl=False)

    def start(self, event):
        self.get_roster()
        self.send_presence()

        try:
            getattr(self, self.action)()
        except:
            logging.error('Could not execute: %s' % self.action)
        self.disconnect()

    def nodes(self):
        try:
            result = self['xep_0060'].get_nodes(self.pubsub_server, self.node)
            for item in result['disco_items']['items']:
                print('  - %s' % str(item))
        except:
            logging.error('Could not retrieve node list.')

    def create(self):
        try:
            self['xep_0060'].create_node(self.pubsub_server, self.node)
        except:
            logging.error('Could not create node: %s' % self.node)

    def delete(self):
        try:
            self['xep_0060'].delete_node(self.pubsub_server, self.node)
            print('Deleted node: %s' % self.node)
        except:
            logging.error('Could not delete node: %s' % self.node)

    def publish(self):
        payload = ET.fromstring("<test xmlns='test'>%s</test>" % self.data)
        try:
            result = self['xep_0060'].publish(self.pubsub_server, self.node, payload=payload)
            id = result['pubsub']['publish']['item']['id']
            print('Published at item id: %s' % id)
        except:
            logging.error('Could not publish to: %s' % self.node)

    def get(self):
        try:
            result = self['xep_0060'].get_item(self.pubsub_server, self.node, self.data)
            for item in result['pubsub']['items']['substanzas']:
                print('Retrieved item %s: %s' % (item['id'], tostring(item['payload'])))
        except:
            logging.error('Could not retrieve item %s from node %s' % (self.data, self.node))

    def retract(self):
        try:
            result = self['xep_0060'].retract(self.pubsub_server, self.node, self.data)
            print('Retracted item %s from node %s' % (self.data, self.node))
        except:
            logging.error('Could not retract item %s from node %s' % (self.data, self.node))

    def purge(self):
        try:
            result = self['xep_0060'].purge(self.pubsub_server, self.node)
            print('Purged all items from node %s' % self.node)
        except:
            logging.error('Could not purge items from node %s' % self.node)

    def subscribe(self):
        try:
            result = self['xep_0060'].subscribe(self.pubsub_server, self.node)
            print('Subscribed %s to node %s' % (self.boundjid.bare, self.node))
        except:
            logging.error('Could not subscribe %s to node %s' % (self.boundjid.bare, self.node))

    def unsubscribe(self):
        try:
            result = self['xep_0060'].unsubscribe(self.pubsub_server, self.node)
            print('Unsubscribed %s from node %s' % (self.boundjid.bare, self.node))
        except:
            logging.error('Could not unsubscribe %s from node %s' % (self.boundjid.bare, self.node))


class IOT_Device(Device):
    """
    This is actual device that you will use to get information from your real hardware
    You will be called in the refresh method when someone is requesting information from you

    """
    def __init__(self, nodeID):
        Device.__init__(self,nodeID)
        log.debug("============Device.__init__ method called")
        self.temperature = 25 #Default data to be sent to server
        self.update_sensor_data()

    def refresh(self, fields):
        """
        The implementation of refresh method
        :param fields:
        :return:
        """
        log.debug("===========Device.update_sensor_data method called")
        self.temperature += 1
        self.update_sensor_data()

    def update_sensor_data(self):
        log.debug("========Device.update_sensor_data method called")
        self._add_field(name="Temperature", typename="numeric", unit="C")
        self._set_momentary_timestamp(self._get_timestamp())
        self._add_field_momentary_data("Temperature", self.get_temperature(),
                                       flags={"automaticReadout": "true"})

    def get_temperature(self):
        return str(self.temperature)