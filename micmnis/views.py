from rest_framework import viewsets
from .models import ApothecaryItem, Origin, Use, Ingredient, SafetyNote
from .serializers import (
    ApothecaryItemSerializer, OriginSerializer, UseSerializer, IngredientSerializer, SafetyNoteSerializer
)

class ApothecaryItemViewSet(viewsets.ModelViewSet):
    queryset = ApothecaryItem.objects.all().select_related('origin').prefetch_related('uses', 'ingredients', 'safety_notes')
    serializer_class = ApothecaryItemSerializer

class OriginViewSet(viewsets.ModelViewSet):
    queryset = Origin.objects.all()
    serializer_class = OriginSerializer

class UseViewSet(viewsets.ModelViewSet):
    queryset = Use.objects.all()
    serializer_class = UseSerializer

class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer

class SafetyNoteViewSet(viewsets.ModelViewSet):
    queryset = SafetyNote.objects.all()
    serializer_class = SafetyNoteSerializer
