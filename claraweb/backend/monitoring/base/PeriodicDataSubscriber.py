# coding=utf-8

from xmsg.core.xMsg import xMsg
from xmsg.core.xMsgTopic import xMsgTopic
from xmsg.net.xMsgAddress import ProxyAddress


class PeriodicDataSubscriber(xMsg):

    def __init__(self, fe_host, topic):
        super(PeriodicDataSubscriber, self).__init__(topic)
        self.fe_host = ProxyAddress(fe_host)
        self.topic = xMsgTopic.build(self.myname)

    def subscribe_to_frontend(self, callback):
        return xMsg.subscribe(self, self.fe_host, self.topic, callback)
