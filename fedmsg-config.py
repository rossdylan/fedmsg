config = dict(
    # This is a dict of possible addresses from which fedmsg can send
    # messages.  fedmsg.init(...) requires that a 'name' argument be passed
    # to it which corresponds with one of the keys in this dict.
    endpoints={
        # This is the output side of the relay to which all other
        # services can listen.
        "relay_outbound": "tcp://*:4001",

        # For other, more 'normal' services, fedmsg will try to guess the
        # name of it's calling module to determine which endpoint definition
        # to use.  This can be overridden by explicitly providing the name in
        # the initial call to fedmsg.init(...).
        #"bodhi.marat": "tcp://*:3001",
        #"fas.marat": "tcp://*:3002",
        #"fedoratagger.marat": "tcp://*:3003",
        #"mediawiki.marat": "tcp://*:3004",
        #"pkgdb.marat": "tcp://*:3005",

        #"busmon.marat": "tcp://*:3006",
    },

    # This is the address of an active->passive relay.  It is used for the
    # fedmsg-logger command which requires another service with a stable
    # listening address for it to send messages to.
    # It is also used by the git-hook, for the same reason.
    # It is also used by the mediawiki php plugin which, due to the oddities of
    # php, can't maintain a single passive-bind endpoint of it's own.
    relay_inbound="tcp://127.0.0.1:2003",


    # Set this to dev if you're hacking on fedmsg or an app.
    # Set to stg or prod if running in the Fedora Infrastructure
    environment="dev",

    # Default is 0
    high_water_mark=0,

    io_threads=1,

    # Options for the fedmsg-irc service.
    irc=[
        dict(
            network='irc.freenode.net',
            port=6667,
            nickname='fedmsg-bot',
            channel='test-fedmsg',
            make_pretty=True,
            filters=dict(
                topic=[],
                body=['lub-dub'],
            )
        ),
        dict(
            network='irc.freenode.net',
            port=6667,
            nickname='fedmsg-bot',
            channel='test-fedmsg2',
            make_pretty=True,
            filters=dict(
                topic=[],
                body=['lub-dub'],
            ),
        ),
    ],

    # Options for the fedmsg-fedbadges services
    badges_global = dict(
            database_uri='sqlite:///fedbadges.db',
            badge_issuer=dict(
                issuer_id='Fedora Project',
                issuer_origin='http://badges.fedora.com',
                issuer_name='Fedora Project',
                issuer_org='http://fedora.org',
                issuer_contact='rdelinge@redhat.com'
                )
    ),

    examplebadge_badges = [
            dict(
                badge_name='Example_Badge',
                badge_image='http://3.bp.blogspot.com/-XhjKweGVJHI/TZBrIJugrBI/AAAAAAAAAJM/ozRJi2bLAK4/s1600/fedora-logo.png',
                badge_desc='An Example Badge awarded for being an example',
                badge_criteria='Being an example'
                ),
    ],
    ## For the fedmsg-hub and fedmsg-relay. ##

    # We almost always want the fedmsg-hub to be sending messages with zmq as
    # opposed to amqp or stomp.
    zmq_enabled=True,

    # When subscribing to messages, we want to allow splats ('*') so we tell the
    # hub to not be strict when comparing messages topics to subscription
    # topics.
    zmq_strict=False,
)
