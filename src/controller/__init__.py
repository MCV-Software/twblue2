""" Controller modules for TWBlue

This package contains all controllers used within TWBlue. According to `MVC pattern <https://en.wikipedia.org/wiki/Model%E2%80%93view%E2%80%93controller>`_, a controller is a special kind of module that is the bridge between the models (which handle the logic behind the application) and the views (which handle the presentation of such logic to users).

We attempt to follow the MVC pattern as close as possible, so there are some rules we should try to follow regarding our controllers:

1. Controllers should be the only objects subscribing to pubsub events. There might be small exceptions to this, for example in models which have no controllers.
2. Controllers should not include any logic that could be done in the model. Except when logic is a single function call.
3. Controllers must be the "glue" between views and models. Views and models should not be able to call to the each other or make assumptions about methods in the each other. All assumptions and calls must be made on controllers.
"""