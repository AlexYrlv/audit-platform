from fpiaioact import ActorApp

from .bus import KafkaActor


def init_actor_app():
    actor_app = ActorApp(name="ActorApp")

    actor_app.register({
        "kafka": KafkaActor(),
    })

    return actor_app
