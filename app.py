import os

from tornado.web import Application
from tornado.ioloop import IOLoop

from motor.motor_tornado import MotorClient

from models import instance, document_templates
from urls import url_patterns


class MainApplication(Application):
    """Used to set up the main application including urls."""

    def __init__(self, templates):
        self.templates = templates
        super().__init__(url_patterns, debug=True)

    def create_indexes(self):
        for template in self.templates.values():
            template.ensure_indexes()


def main():
    instance.init(db=MotorClient(os.environ["DATABASE_URL"])["workforce_app"])
    app = MainApplication(templates=document_templates)
    app.create_indexes()
    app.listen(int(os.environ.get("PORT", 5000)))

if __name__ == "__main__":
    main()
    IOLoop.current().start()
