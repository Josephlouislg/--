import importlib
from project.tasks import register_tasks, init_celery
from project.server import create_base_app


if __name__ == '__main__':
    app = create_base_app()
    celery = init_celery(app)
    worker = celery.Worker()
    with app.app_context():
        worker.start()
