# coding=utf-8

from xmsg.core.xMsg import xMsg
from xmsg.core.xMsgTopic import xMsgTopic


class PeriodicDataSubscriber(xMsg):

    def __init__(self, name, topic):
        super(PeriodicDataSubscriber, self).__init__(name)
        self.topic = xMsgTopic.build(self.myname)

    def subscribe(self, callback):
        return xMsg.subscribe(self, self.topic, self.connect(), callback)
