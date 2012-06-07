# -*- coding; utf-8 -*-
# Author: Ross Delinger
# Description: Consumer for producing openbadges by listening for messages on fedmsg

from paste.deploy.converters import asbool
from moksha.api.hub.consumer import Consumer
from dbapi import TahrirDatabase

import logging
log = logging.getLogger("moksha.hub")


class FedoraBadgesConsumer(Consumer):

    def __init__(self, hub, name):
        self.name = name
        self.badges = {}
        self.hub = hub
        self.DBSession = None
        ENABLED = 'fedmsg.consumers.badges.{0}.enabled'.format(self.name)
        if not asbool(hub.config.get(ENABLED, False)):
            log.info('fedmsg.consumers.badges.{0} disabled'.format(self.name))
            return

        global_settings = hub.config.get("badges_global")

        database_uri = global_settings.get('database_uri', '')
        if database_uri == '':
            raise Exception('Badges consumer requires a database uri')
            return
        self.tahrir = TahrirDatabase(database_uri)
        self.DBSession = self.tahrir.session_maker
        issuer = global_settings.get('badge_issuer')
        self.issuer_id = self.tahrir.add_issuer(
                issuer.get('issuer_origin'),
                issuer.get('issuer_name'),
                issuer.get('issuer_org'),
                issuer.get('issuer_contact')
                )

        badges_settings = hub.config.get("{0}_badges".format(self.name))
        for badge in badges_settings:
            self.tahrir.add_badge(
                    badge.get('badge_name'),
                    badge.get('badge_image'),
                    badge.get('badge_desc'),
                    badge.get('badge_criteria'),
                    self.issuer_id
                    )
        return super(FedoraBadgesConsumer, self).__init__(hub)


    def award_badge(self, email, badge_id, issued_on=None):
        person_id = hash(email)
        self.tahrir.add_person(person_id, email)
        self.tahrir.add_assertion(badge_id, person_id, issued_on)

    def consume(self, msg):
        """
        Consume a single message, we pass here because every subclass is going
        to want to parse this slightly differently
        """
        pass
