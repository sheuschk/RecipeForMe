from app import create_app, db, cli
from app.models import Cocktail, Ingredient

app = create_app()
cli.register(app)


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Cocktail': Cocktail, 'Ingredient': Ingredient}
