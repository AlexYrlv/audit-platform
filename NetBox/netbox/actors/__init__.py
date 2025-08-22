from fpiaioact import ActorApp
from .grpc import NetBoxActor

def init(app: ActorApp) -> ActorApp:
    app.register({
        "netbox": NetBoxActor("NetBoxService")
    })
    return app