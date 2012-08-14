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
import fedmsg
from fedmsg.commands import command

extra_args = [
    (['--websocket-server-port'], {
        'dest': 'moksha.livesocket.websocket.port',
        'type': int,
        'help': 'Port on which to host the websocket server.',
        'default': None,
    }),
]


@command(name="fedmsg-hub", extra_args=extra_args, daemonizable=True)
def hub(**kw):
    """ Run the fedmsg hub. """

    # Check if the user wants the websocket server to run
    if kw['moksha.livesocket.websocket.port']:
        kw['moksha.livesocket.backend'] = 'websocket'

    # Rephrase the fedmsg-config.py config as moksha *.ini format.
    # Note that the hub we kick off here cannot send any message.  You should
    # use fedmsg.publish(...) still for that.
    moksha_options = dict(
        zmq_subscribe_endpoints=','.join(
            ','.join(bunch) for bunch in kw['endpoints'].values()
        ),
    )
    kw.update(moksha_options)

    from moksha.hub import main
    main(options=kw)
