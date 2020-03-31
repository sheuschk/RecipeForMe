from app import app, db
from app.models import Cocktail, Ingredient


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Cocktail': Cocktail, 'Ingredient': Ingredient}
