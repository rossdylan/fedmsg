import badge

class ExampleBadgesConsumer(badge.FedoraBadgesConsumer):
    topic = "org.fedoraproject.*"

    def __init__(self, hub):
        self.name = "examplebadge"
        super(ExampleBadgesConsumer, self).__init__(hub, self.name)

    def consume(self, msg):
        topic, body = msg.get('topic'), msg.get('body')

        if body.startswith("example_thing"):
            parts = body.split(" ")[1:]
            email = parts[0]
            badge_id = "example_badge"
            self.award_badge(email, badge_id)




