from fedmsg.commands import command

extra_args = []

@command(extra_args=extra_args)
def badges(**kw):
    moksha_options = dict(
            zmq_subscribe_endpoints=','.join(kw['endpoints'].values()),
    )
    kw.updates(moksha_options)
    kw['fedmsg.consumers.badges.examplebadge.enabled'] = True

    from moksha.hub import main
    main(options=kw)
