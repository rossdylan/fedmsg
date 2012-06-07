import badges
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




