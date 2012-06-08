# -*- coding: utf-8 -*-
# Author: Ross Delinger
# Description: API For interacting with the Tahrir database

from model import Badge, Issuer, Assertion, Person
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from datetime import datetime


class TahrirDatabase(object):
    def __init__(self, dburi):
        self.session_maker = sessionmaker(bind=create_engine(dburi))

    def badge_exists(self, badge_id):
        session = scoped_session(self.session_maker)
        return session.query(Badge).filter_by(id=badge_id).count() != 0

    def add_badge(self, name, image, desc, criteria, issuer_id):
        session = scoped_session(self.session_maker)
        badge_id = name.lower()

        if not self.badge_exists(badge_id):
            new_badge = Badge(
                    name=name,
                    image=image,
                    description=desc,
                    criteria=criteria,
                    issuer_id=issuer_id
                    )
            session.add(new_badge)
            session.commit()

    def person_exists(self, person_email):
        session = scoped_session(self.session_maker)
        return session.query(Person).filter_by(email=person_email).count() != 0

    def get_person(self,person_email):
        session = scoped_session(self.session_maker)
        return session.query(Person).filter_by(email=person_email).one()

    def add_person(self, person_id, email):
        session = scoped_session(self.session_maker)
        if not self.person_exists(email):
            new_person = Person(
                    id=person_id,
                    email=email
                    )
            session.add(new_person)
            session.commit()

    def issuer_exists(self, issuer_id):
        session = scoped_session(self.session_maker)
        return session.query(Issuer).filter_by(id=issuer_id).count() != 0

    def add_issuer(self, origin, name, org, contact):
        session = scoped_session(self.session_maker)
        issuer_id = hash(origin + name)
        if not self.issuer_exists(issuer_id):
            new_issuer = Issuer(
                    id=issuer_id,
                    origin=origin,
                    name=name,
                    org=org,
                    contact=contact
                    )
            session.add(new_issuer)
            session.commit()
        return issuer_id

    def add_assertion(self, badge_id, person_email, issued_on):
        session = scoped_session(self.session_maker)
        if issued_on == None:
            issued_on = datetime.now()
        if self.person_exists(person_email) and self.badge_exists(badge_id):
            new_assertion = Assertion(
                    badge_id=badge_id,
                    person_id=self.get_person(person_email).id,
                    issued_on=issued_on
                    )
            session.add(new_assertion)
            session.commit()
