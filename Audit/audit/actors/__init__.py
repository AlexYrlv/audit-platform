from fpiaioact import ActorApp

from .bus import KafkaActor

def init(app: ActorApp) -> ActorApp:
    app.register({
        "audit": KafkaActor()
    })
    return app
