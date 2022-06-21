from django.core.management.base import BaseCommand

import requests
# from django.core.exceptions import ObjectDoesNotExist
from .constants import CATEGORIES
from purbeurre.products.models import Categories, Products


####################################################################
"""   SCRIPT TO INITIALIZE THE DB THROUGH OPEN FOOD FACTS' API   """
####################################################################


class DBpopulator(BaseCommand):
    def __init__(self):
        #  stores api answers
        self.response = None
        # stores api answers in json
        self.json_response = None
        # dictionnary used by requests for api requests
        self.criteria = None
        self.urlapi = "https://fr.openfoodfacts.org/cgi/search.pl"

    @staticmethod
    def populate_categories():
        """This method will populate the DB with data from the API"""
        for cat in CATEGORIES:
            Categories.objects.get_or_create(name=cat)

    def create_crits(self, tag_0, page_size):
        """This method will create a dictionnary in order to request the API"""
        self.criteria = {
            "action":  "process",
            "json":  1,
            "tagtype_0":  "categories",
            "tag_contains_0":  "contains",
            "tag_0":  tag_0,
            "page_size":  page_size,
            "sort_by":  "unique_scans_n",
            'tagtype_1': 'countries',
            'tag_contains_1': 'contains',
            'tag_1': 'france',
            'fields': 'product_name_fr,url,image_url,nutriscore_grade,'
                      'nutriments',
            }

    def request(self):
        """This method will reqquest the API on specific criteria"""
        self.response = requests.get(self.urlapi, params=self.criteria)

    def populate_products(self, category):
        """This method will populate the DB with data from the API"""
        self.json_response = self.response.json()['products']
        for rec in self.json_response:
            print(rec)
            # extracts all the needed info of a given product in order to
            # store it in DB
            # rec.get('product_name_fr', None)
            try:
                name = rec['product_name_fr']
                url = rec['url']
                image_url = rec['image_url']
                nutriscore = rec['nutriscore_grade']
                energy = rec.get('nutriments', {}).get('energy-kcal_100g', 0)
                fat = rec.get('nutriments', {}).get('fat_100g', 0)
                saturated_fat = rec.get('nutriments', {}).get('saturated-fat_100g', 0)
                sugar = rec.get('nutriments', {}).get('sugars_100g', 0)
                salt = rec.get('nutriments', {}).get('salt_100g', 0)
                category = Categories.objects.get(name=category)
            except KeyError:
                continue
            # keeping only products for which we have nutrigrade info
            if nutriscore in ('a', 'b', 'c', 'd', 'e'):
                Products.objects.update_or_create(name=name,
                                        url=url,
                                        image=image_url,
                                        nutriscore=nutriscore,
                                        energy=energy,
                                        fat=fat,
                                        saturated_fat=saturated_fat,
                                        sugar=sugar,
                                        salt=salt,
                                        category=category,
                                        defaults={'name': name,
                                                  'url': url,
                                                  'image': image_url,
                                                  'nutriscore': nutriscore,
                                                  'energy': energy,
                                                  'fat': fat,
                                                  'saturated_fat': saturated_fat,
                                                  'sugar': sugar,
                                                  'salt': salt,
                                                  'category': category
                                                 }
                                                )
        Products.objects.filter(name="").delete()


if __name__ == '__main__':

    def database_init():
        """This method takes needed actions to create and populate the DB"""
        dbpopulator = DBpopulator()
        dbpopulator.populate_categories()
        # we populate products table categories by categories
        for cat in CATEGORIES:
            dbpopulator.create_crits(cat, 1000)
            dbpopulator.request()
            dbpopulator.populate_products(cat)
        print("Congratulations, you have initialized the DB!")

    database_init()
