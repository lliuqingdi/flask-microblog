from app import db, cli, create_app
from app.models import User, Post
from config import Config

app = create_app(Config)
cli.register(app)


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post}


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
