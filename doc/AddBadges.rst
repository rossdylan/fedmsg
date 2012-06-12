.. contents::

This is a guide to adding new badges to the fedbadges system. There are 3 main
steps to adding new badges to the system. The first step is to write a new
Consumer based on FedoraBadgesConsumer. The second step is to add the badge
data to a fedmsg config file. The third step is to enable the badge in the
badges command file.

----

Authors:
- Ross Delinger (rossdylan)
Edits:
- Remy D (decause)


Creating a new Consumer
======================

To award badges a new Consumer based on FedoraBadgesConsumer is required. This
consumer sets what topic to monitor, and the name of this consumer. This name
is used to get information from the config file specific to that Consumer.::
        from badges import FedoraBadgesConsumer
        import logging
        log = logging.getLogger("moksha.hub")

        class ExampleBadgesConsumer(FedoraBadgesConsumer):
            topic = "org.fedoraproject.*"

            def __init__(self, hub):
                self.name = "examplebadge"
                super(ExampleBadgesConsumer, self).__init__(hub, self.name)

            def consume(self, msg):
                topic, body = msg.get('topic'), msg.get('body')
                if type(body) == type(""):
                    return
                body = body.get('msg')
                print body.get('action')
                if body.get('action') == 'This guy did some awesome thing!':
                    email = body.get('email')
                    log.info("Awarding 'Example Badge' to {0}".format(email))
                    badge_id = "example_badge"
                    self.award_badge(email, badge_id)


This example is very simple. The topic is set at the top of the class. This is
used to limit the messages that are sent to this Consumer. An example of a topic
that limits this consumer to only messages from a service such as bodhi would be
"org.fedoraproject.bodhi.*". In the __init__ function you can initialize other
things the consumer requires, set the name of this consumer, and then call super
to initialize the superclass which handles all the database calls and config
parsing. After __init__ comes the consume method, which is called when the hub
passes as a message. Consume is where badges are awarded. To award a badge, call
self.award_badge with the badge id, and the email of the person receiving the
badge.


Adding badge information to the config file
===========================================

When you create a new consumer you give it a name. This name is used as a
prefix to retrieve badge information from the fedmsg config files. The fedmsg
config files are actually just python files which are used to store
information. Each consumer requires it's own section in the config file. This
section is required to be <consumer name>_badges. This section is a python list
containing dictionaries of badge information. The required keys are badge_name,
badge_image, badge_desc, and badge_criteria. These items are used to bootstrap
the database on first launch of fedbadges. An example config section for the
above ExampleBadgesConsumer is as follows::
        config = dict(
            #An example badge definition
            examplebadge_badges = [
                dict(
                    badge_name='Example_Badge',
                    badge_image='http://3.bp.blogspot.com/-XhjKweGVJHI/TZBrIJugrBI/AAAAAAAAAJM/ozRJi2bLAK4/s1600/fedora-logo.png',
                    badge_desc='An Example Badge awarded for being an example',
                    badge_criteria='http://fedoraproject.org'
                    ),
            ]
        )

The convention for adding new consumer config sections is to split them out
into multiple files under fedmsg.d, however it is possible to combine the
config sections into a single config dict.

Enabling the new badges consumer
================================

To enable the new badges consumer you need to add a line to badges.py in the
fedmsg/commands folder. Add a line that says::
        kw['fedmsg.consumers.badges.<badge name>.enabled'] = True
Where <badge name> is the name of the consumer you set in step one

.. note:: Enabling new consumers may be moved to the config file in future
   versions

Who can do each step
====================

Steps one and two can be done by any user who wants to contribute to fedbadges.
Placing the consumer and config file into the proper place needs to be done by
an admin along with enabling the new consumer in the badges.py command file.
