import click
from app import app, db
from app.models import Post, VkPublic, Task, User


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Post': Post, 'VkPublic': VkPublic, 'Task': Task,
            'User': User}


@click.group()
def cli():
    pass


@cli.command()
def run():
    from app import app
    host = app.config['HOST']
    port = app.config['PORT']

    # if __name__ != '__main__':
    #     gunicorn_logger = logging.getLogger('gunicorn.error')
    #     app.logger.handlers = gunicorn_logger.handlers
    #     app.logger.setLevel(gunicorn_logger.level)
    # else:

    app.run(host=host, port=port)
    print('ha')


if __name__ == '__main__':
    cli()
