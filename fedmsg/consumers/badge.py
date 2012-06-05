# -*- coding; utf-8 -*-
# Author: Ross Delinger
# Description: Consumer for producing openbadges by listening for messages on fedmsg

import fedmsg
import fedmsg.json

from paste.deploy.converters import asbool
from moksha.api.hub.consumer import Consumer
from model import Badge, Issuer, Assertion, Person
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import logging
log = logging.getLogger("moksha.hub")


class FedoraBadgesConsumer(Consumer):

    def __init__(self, hub, name):
        self.name = name
        self.DBSession = None

        ENABLED = 'fedmsg.consumers.{0}.enabled'.format(name)
        if not asbool(hub.config.get(ENABLED, False)):
            log.info('fedmsg.consumers.{0} disabled'.format(name))

        global_settings = hub.config.get("badges_global")
        database_uri = global_settings.get('database_uri', '')
        if database_uri == '':
            raise Exception('Badges consumer requires a database uri')
        self.DBSession = sessionmaker(engine=create_engine(database_uri))
        badges_settings = hub.config.get("{0}_badges".format(self.name))
        for badge in badges_settings:
            self.add_badge(
                    badge.get('badge_id'),
                    badge.get('badge_name'),
                    badge.get('badge_image'),
                    badge.get('badge_desc'),
                    badge.get('badge_criteria'),
                    badge.get('issuer_id')
                    )

    def badge_exists(self, badge_id):
        """
        Convience function to check if a badge with the specified ID exists

        :type badge_id: str
        :param badge_id: ID of the badge to check
        """

        return self.DBSession.query(Person.id).filter_by(id=badge_id).count() == 0

    def add_badge(self, id, name, image, desc, criteria, issuer_id):
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

    def consume(self, msg):
        pass
