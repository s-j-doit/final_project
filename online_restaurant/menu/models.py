from django.db import models


class Dish(models.Model):

    # dish categories
    class Category(models.TextChoices):
        SALADS = 'Salads', 'Salads'
        SOUPS = 'Soups', 'Soups'
        CHICKEN = 'Chicken-Dishes', 'Chicken-Dishes'
        BEEF = 'Beef-Dishes', 'Beef-Dishes'
        SEAFOOD = 'Seafood-Dishes', 'Seafood-Dishes'
        VEGETABLES = 'Vegetable-Dishes', 'Vegetable-Dishes'
        BITS = 'Bits&Bites', 'Bits&Bites'
        SIDE = 'On-The-Side', 'On-The-Side'

    # dish info
    name = models.CharField(max_length=100)
    description = models.TextField()

    category = models.CharField(
        max_length=30,
        choices=Category.choices
    )

    image = models.ImageField(upload_to='dishes/images/')

    spice_level = models.PositiveSmallIntegerField(
        choices=[
            (0, '0 - Not spicy'),
            (1, '1 - Mild'),
            (2, '2 - Medium'),
            (3, '3 - Hot'),
            (4, '4 - Very hot'),
        ],
        default=0
    )

    contains_walnuts = models.BooleanField(default=False)
    is_vegetarian = models.BooleanField(default=False)

    price = models.DecimalField(
        max_digits=8,
        decimal_places=2
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = 'Dish'
        verbose_name_plural = 'Dishes'