from datetime import timedelta
from moksha.api.hub.producer import PollingProducer
import zmq

import fedmsg.encoding
import logging

log = logging.getLogger(__name__)

class HeartbeatProducer(PollingProducer):
    short_topic = "_heartbeat"
    topic = "org.fedoraproject." + short_topic

    frequency = timedelta(seconds=2)

    def poll(self):
        # FIXME -- this should use fedmsg.publish
        try:
            self.hub.send_message(
                topic=self.topic,
                message=fedmsg.encoding.dumps({'msg': "lub-dub"}),
            )
        except zmq.ZMQError, e:
            log.warn("Could not emit heartbeat: %r" % e)
