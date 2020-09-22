import click
from app.models import Recipe, Ingredient
import json
import csv


def register(app):
    fnames = ['name', 'desc', 'ing']

    @app.cli.group()
    def data():
        """Commands to progress data from the db"""
        """Both commands are just for test purposes"""
        pass

    @data.command()
    @click.argument('name')
    def download(name):
        """Download all Cocktails and Ingredients as Excel"""
        # flask data download name
        cts = Recipe.query.all()
        all_cocktails = []
        for cocktail in cts:
            save = {"name": cocktail.name, "desc": cocktail.desc, "ing": {}}
            for ing in cocktail.ingredients:
                save['ing'][ing.name] = ing.quantity
            # all_cocktails.append(json.dumps(save))
            all_cocktails.append(save)
        with open(f"{name}.csv", 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fnames)
            for cocktail_str in all_cocktails:
                writer.writerow(cocktail_str)

    @data.command()
    @click.argument('name')
    def upload(name):
        """Upload an Excel with the Schema of the download and save them to the db"""
        with open(f"{name}.csv", newline='', encoding='utf8') as csvfile:
            reader = csv.DictReader(csvfile, fieldnames=fnames)
            for row in reader:
                print(row['name'])
                print(row['ing'])
                ings_corrected = row['ing'].replace("'", "\"")
                ings = json.loads(ings_corrected)
                print(type(ings))
                print()
            # Further code to save it to the db. See create function for inspiration.

