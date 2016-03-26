from flask import current_app
import psycopg2

try:
    from flask import _app_ctx_stack as stack
except ImportError:
    from flask import _request_ctx_stack as stack


def Connect():
    return psycopg2.connect(
        database="uber",
        user="uber_app",
        password="q94EMtInmu7jBj8sUi3qVQ2yYo8bYWva",
        host="localhost",
        port="9000"
    )

class Postgres(object):

    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        # app.config.setdefault('SQLITE3_DATABASE', ':memory:')
        # Use the newstyle teardown_appcontext if it's available,
        # otherwise fall back to the request context
        if hasattr(app, 'teardown_appcontext'):
            app.teardown_appcontext(self.teardown)
        else:
            app.teardown_request(self.teardown)

    def connect(self):
        return Connect()

    def teardown(self, exception):
        ctx = stack.top
        if hasattr(ctx, 'db'):
            ctx.db.close()

    @property
    def connection(self):
        ctx = stack.top
        if ctx is not None:
            if not hasattr(ctx, 'db'):
                ctx.db = self.connect()
            return ctx.db
