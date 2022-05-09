from django.db import models
from purbeurre.accounts.models import CustomUser

# Create your models here.
class Categories(models.Model):
    """Cet objet représente une catégorie"""
    name = models.CharField(max_length=200, 
                            help_text='Entrez le nom d\'une catégorie.')

    def __str__(self):
        """Cette fonction est obligatoirement requise par Django.
           Elle retourne une chaîne de caractère pour identifier l'instance de 
           la classe d'objet."""
        return self.name

class Products(models.Model):
    name = models.CharField(max_length=255)
    url = models.URLField(max_length=255)
    image = models.URLField(max_length=255)
    nutriscore = models.CharField(max_length=255)
    energy = models.FloatField()
    fat = models.FloatField()
    saturated_fat = models.FloatField()
    sugar = models.FloatField()
    salt = models.FloatField()
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

# Table de jonction pour les catégories
class ProductCategory(models.Model):
    """  """
    id_product = models.ForeignKey(Products, on_delete=models.CASCADE)
    id_category = models.ForeignKey(Categories, on_delete=models.CASCADE)

# Table qui va sauver les favoris des utilisateurs
class Favorites(models.Model):
    searched_product = models.ForeignKey(Products,
                                        on_delete=models.CASCADE,
                                        related_name='searched_product')
    substitution_product = models.ForeignKey(Products,
                                        on_delete=models.CASCADE,
                                        related_name='substitution_product')
    user = models.ForeignKey(CustomUser,
                            on_delete=models.CASCADE,
                            related_name='user')

    class Meta:
        ordering = ['id']
        constraints = [
            models.UniqueConstraint(
                fields=['searched_product', 'substitution_product', 'user'],
                name='no_double')
        ]