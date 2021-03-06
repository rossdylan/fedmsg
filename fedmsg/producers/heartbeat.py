# This file is part of fedmsg.
# Copyright (C) 2012 Red Hat, Inc.
#
# fedmsg is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# fedmsg is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with fedmsg; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA
#
# Authors:  Ralph Bean <rbean@redhat.com>
#
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
