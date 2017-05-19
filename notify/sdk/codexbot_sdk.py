import asyncio

from notify.sdk.lib.db import Db
from .lib.logging import Logging
from .components.broker import Broker
from .lib.server import Server
from .config import SERVER


class CodexBot:

    def __init__(self, application_name, queue_name, host, port, db_config, token):
        """
        Initiates SDK
        :param queue_name: - name of queue that this tool delegates to core
        """

        # Get event loop
        self.event_loop = asyncio.get_event_loop()

        self.application_name = application_name
        self.token = token

        self.logging = self.init_logging()
        self.db = self.init_db(db_config)
        self.server = self.init_server()
        self.broker = self.init_broker(application_name, queue_name)

        self.broker.start()

    def init_logging(self):
        return Logging()

    def init_server(self):
        return Server(self.event_loop, SERVER['host'], SERVER['port'])

    def init_broker(self, application_name, queue_name):
        return Broker(self, self.event_loop, application_name, queue_name)

    def init_db(self, db_config):
        self.logging.debug("Initialize db.")
        db_name = "module_{}".format(self.application_name)
        return Db(db_name, db_config[0], db_config[1])

    def log(self, message):
        self.logging.debug(message)

    def start_server(self):
        self.server.start()

    def set_routes(self, routes):
        self.server.set_routes(routes)

    def register_commands(self, commands):
        self.broker.api.register_commands(commands)