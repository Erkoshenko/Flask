from .ping import ping_handler
from .account import account_handlers
from .balance import balance_handlers
from .update import update_handlers
from .stats import stats_handlers

def register_handlers(app, db):
    ping_handler(app)
    account_handlers(app, db)
    balance_handlers(app, db)
    update_handlers(app, db)
    stats_handlers(app, db)