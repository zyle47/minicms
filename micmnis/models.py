from django.db import models
from django.core.validators import MinValueValidator


class Origin(models.Model):
    country = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.country


class ApothecaryItem(models.Model):
    TYPE_CHOICES = [
        ("HERB", "Herb"),
        ("TINC", "Tincture"),
        ("BALM", "Balm"),
        ("OIL", "Essential Oil"),
        ("OTHER", "Other"),
    ]

    item_id = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    origin = models.ForeignKey(Origin, on_delete=models.SET_NULL, null=True, blank=True)

    # Basic info
    price_usd = models.DecimalField(
    max_digits=7, decimal_places=2, validators=[MinValueValidator(0)], null=True, blank=True
    )
    stock_oz = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    volume_ml = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    container_size_g = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)


    # Preparation / usage
    preparation = models.CharField(max_length=200, blank=True, null=True)
    dosage = models.CharField(max_length=200, blank=True, null=True)
    application = models.CharField(max_length=200, blank=True, null=True)


    # Metadata
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.item_id})"


class Use(models.Model):
    """E.g. 'Headache relief', 'Immune support'"""
    name = models.CharField(max_length=100, unique=True)
    items = models.ManyToManyField(ApothecaryItem, related_name="uses", blank=True)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """Represents herbal or chemical ingredients."""
    name = models.CharField(max_length=100, unique=True)
    items = models.ManyToManyField(ApothecaryItem, related_name="ingredients", blank=True)

    def __str__(self):
        return self.name


class SafetyNote(models.Model):
    """Warnings like 'Do not ingest'."""
    text = models.CharField(max_length=150)
    items = models.ManyToManyField(ApothecaryItem, related_name="safety_notes", blank=True)

    def __str__(self):
        return self.text
