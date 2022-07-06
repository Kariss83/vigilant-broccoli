from django.core.management.base import BaseCommand
from products.dbpopulator import DBpopulator
from products.constants import CATEGORIES


class Command(BaseCommand):
    help = 'Populating the DB with the categories inside the CATEGORIES'

    def handle(self, *args, **options):
        """This method takes needed actions to create and populate the DB"""
        dbpopulator = DBpopulator()
        dbpopulator.populate_categories()
        # we populate products table category by category
        for cat in CATEGORIES:
            dbpopulator.create_crits(cat, 1000)
            dbpopulator.request()
            dbpopulator.populate_products(cat)
        self.stdout.write(self.style.SUCCESS('DB initialisée avec succès.'))
