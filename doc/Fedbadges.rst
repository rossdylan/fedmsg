Overview - Fedora Badges
========================

.. contents::

This is a grand overview of the entire plan for Fedora Badges. It deals with
fedmsg plugins for various fedora infrastructure applications, Consumers listening
on the fedmsg bus who award badges, The database storing badge user, and assertion data,
and the Web front end Tahrir which ties Fedora Badges into Open badges global ecosystem.

----

The source of this document is hosted at
https://github.com/rossdylan/fedmsg

Authors:
- Ross Delinger (rossdylan)

How data moves through the system
=================================

Fedora Badges relies heavily on moving data around the Fedora Infrastructure
applications. For Examplem, to award a badge for a users first successful build on Koji,
we need to know when it happened. To facilitate this all the major applications that make up
the infrastructure will be tied into Fedora Messaging. With this we can have a unifed way of
moving data. The Fedora Badges Service will sit and listen on this messaging bus and when a
message it understands is recieved it will award a badge based on the message.
So far the time line for data moving through the systme is like this:
1) User of an application does something.
2) Application emits message over Fedora Messaging.
3) The Fedora Badges services recieves the message
4) Fedora badges issues a badge based on that message

Now a badge has been issued a badge, from here the information about that issued badge
is dumped into a shared database. This database is shared between the Fedora badges
services listening on the message bus, and the Fedora badges website which is based on
`Tahrir <https://github.com/ralphbean/tahrir>`_. Using this web frontend users can claim their badges
and add them to their Open Badges `Backpack <http://beta.openbadges.org/backpack/login>`_.

Architecture of the Fedora Badges Service
=========================================

This service runs as a fedmsg consumer. The consumer listens on the fedmsg bus and when it receives a message
it will act in some way. For simplicities sake there will be a base class that all Consumers awarding badges
will inherit from. This super class handles database work, and getting values from config files. Classes that
inherit from this super class only need to define a topic, a name, and then the code they want to run whenever
a message is recieved. A simple example of such a subclass follows:::
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

This code is pretty simple, most of the code is actually just there to parse the message received and check to see if
a badge needs to be awarded.

Fedora Badges Config Files
--------------------------

Since the core Fedora Badges service runs as a consume under fedmsg the config files for fedora badges are located
in the same place as fedmsg and have the same format. This format is one of standard python files.
There are two main configuration sections for Fedora Badges. The first section is the global config section which
stores information on the database, and defines the issuer to issue badges with. An example of such a config section is as follows:::
        config = dict(
            # Options for the fedmsg-fedbadges services
            badges_global = dict(
                database_uri='mysql://fedbadges:password@localhost/fedbadges',
                    badge_issuer=dict(
                        issuer_id='Fedora Project',
                        issuer_origin='http://badges.fedoraproject.com',
                        issuer_name='Fedora Project',
                        issuer_org='http://fedoraproject.org',
                        issuer_contact='example@redhat.com'
                        )
            ),
        )

The second config section for Fedora Badges is specific to each new Consumer. Each subclass of FedoraBadgesConsumer needs to
set a name. In the example one section above, the name is 'examplebadge'. This name is used to go into the fedmsg config
files and get sections labeled with that name. Right now all this does is get all the Open Badge definitions out of the config
files and into the database. An example of this type of config section is below:::
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

.. note:: These config sections are seperated out into seperate files (badges-global.py and example-badge.py)
   if you wanted to combine these into a single file you would remove the 'config = dict(' lines and then combine the rest

The Database
------------

The database for Fedora Badges is based on the database structure Ralph Bean created for Tahrir. This database has 4 tables.
1) Person
   - ID
   - email
2) Badge
   - ID
   - Image
   - description
   - criteria
   - assertions
   - issuer_id
3) Issuer
   - ID
   - origin
   - name
   - org
   - contact
   - badges
4) Assertion
   - ID
   - badge_id
   - person_id
   - salt
   - issued_on
   -recipient

The fedora badges services running under fedmsg write the badge and issuer information stored in their config files to
the database on boot. Then when they want to award a badge to someone, they start by adding the person getting the badge
to the database if it doesn't already exist, and then creates an assertion tieing that Badge and user together in the database.
The web frontend then takes this data and uses it to display information on who has reiceived what badges from which issuer. It also
provides a host for the assertions created so the wider Open Badges ecosystem can access Fedora Badges
