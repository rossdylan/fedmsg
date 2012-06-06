# -*- coding; utf-8 -*-
# Author: Ross Delinger
# Description: Consumer for producing openbadges by listening for messages on fedmsg

from paste.deploy.converters import asbool
from moksha.api.hub.consumer import Consumer
from model import Badge, Issuer, Assertion, Person
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from datetime import date

import logging
log = logging.getLogger("moksha.hub")


class FedoraBadgesConsumer(Consumer):

    def __init__(self, hub, name):
        self.name = name
        self.DBSession = None
        self.badges = {}
        ENABLED = 'fedmsg.consumers.badges.{0}.enabled'.format(self.name)
        if not asbool(hub.config.get(ENABLED, False)):
            log.info('fedmsg.consumers.badges.{0} disabled'.format(self.name))

        global_settings = hub.config.get("badges_global")

        database_uri = global_settings.get('database_uri', '')
        if database_uri == '':
            raise Exception('Badges consumer requires a database uri')
        self.DBSessionMaker = sessionmaker(bind=create_engine(database_uri))
        self.DBSession = scoped_session(self.DBSessionMaker)

        issuer = global_settings.get('badge_issuer')
        self.issuer_id = self.add_issuer(
                issuer.get('issuer_origin'),
                issuer.get('issuer_name'),
                issuer.get('issuer_org'),
                issuer.get('issuer_contact')
                )

        badges_settings = hub.config.get("{0}_badges".format(self.name))
        for badge in badges_settings:
            self.add_badge(
                    badge.get('badge_name'),
                    badge.get('badge_image'),
                    badge.get('badge_desc'),
                    badge.get('badge_criteria'),
                    self.issuer_id
                    )
        return super(FedoraBadgesConsumer, self).__init__(hub)

    def badge_exists(self, badge_id):
        """
        Convience function to check if a badge with the specified ID exists

        :type badge_id: str
        :param badge_id: ID of the badge to check
        """

        return self.DBSession.query(Badge.id).filter_by(id=badge_id).count() != 0

    def add_badge(self, name, image, desc, criteria, issuer_id):
        """
        Add a new badge to the database

        :type id: str
        :param id: The Badge's ID

        :type name: str
        :param name: Name of this Badge

        :type image: str
        :param image: url for this Badge's png

        :type desc: str
        :param desc: description of this badge

        :type: criteria: str
        :param criteria: Why this badge is awarded

        :type issuer_id: str
        :param issuer_id: ID of the Issuer who issued this badge
        """

        if not self.badge_exists(id):
            new_badge = Badge(
                        id=id,
                        name=name,
                        image=image,
                        description=desc,
                        criteria=criteria,
                        issuer_id=issuer_id
                        )
            self.DBSession.add(new_badge)
            self.DBSession.commit()

        if not id in self.badges:
            self.badges[id] = issuer_id

    def person_exists(self, id):
        """
        Check if a person with this ID exists in our database

        :type id: int
        :param id: the ID of this person
        """

        return self.DBSession.query(Person.id).filter_by(id=id).count() != 0

    def add_person(self, id, email):
        """
        Add a new Person to the database

        :type id: int
        :param id: ID of this Person

        :type email: str
        :param email: the Email of this Person
        """

        if not self.person_exists(id):
            new_person = Person(
                    id=id,
                    email=email
                    )
            self.DBSession.add(new_person)
            self.DBSession.commit()

    def issuer_exists(self, id):
        return self.DBSession.query(Issuer.id).filter_by(id=id).count() != 0

    def add_issuer(self, origin, name, org, contact):
        id = hash(origin + name)
        if not self.issuer_exists(id):
            new_issuer = Issuer(
                    id=id,
                    origin=origin,
                    name=name,
                    org=org,
                    contact=contact
                    )
            self.DBSession.add(new_issuer)
            self.DBSession.commit()
        return id

    def award_badge(self, email, badge_id, issued_on=None):
        person_id = hash(email)
        self.add_person(person_id, email)
        self.add_assertion(badge_id, person_id, issued_on)

    def add_assertion(self, badge_id, person_id, issued_on):
        if issued_on == None:
            issued_on = date.now()
        if self.person_exists(person_id) and self.badge_exists(badge_id):
            new_assertion = Assertion(
                    badge_id=badge_id,
                    person_id=person_id,
                    issued_on=issued_on
                    )
            self.DBSession.add(new_assertion)
            self.DBSession.commit()

    def consume(self, msg):
        """
        Consume a single message, we pass here because every subclass is going
        to want to parse this slightly differently
        """
        pass
