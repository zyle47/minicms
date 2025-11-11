from rest_framework import serializers
from .models import ApothecaryItem, Origin, Use, Ingredient, SafetyNote


class OriginSerializer(serializers.ModelSerializer):
    class Meta:
        model = Origin
        fields = ['id', 'country']


class UseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Use
        fields = ['id', 'name']


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['id', 'name']


class SafetyNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = SafetyNote
        fields = ['id', 'text']


class ApothecaryItemSerializer(serializers.ModelSerializer):
    origin = OriginSerializer(read_only=True)
    origin_id = serializers.PrimaryKeyRelatedField(
        queryset=Origin.objects.all(), source='origin', write_only=True, required=False
    )

    uses = UseSerializer(many=True, read_only=True)
    use_ids = serializers.PrimaryKeyRelatedField(
        queryset=Use.objects.all(), many=True, source='uses', write_only=True, required=False
    )

    ingredients = IngredientSerializer(many=True, read_only=True)
    ingredient_ids = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all(), many=True, source='ingredients', write_only=True, required=False
    )

    safety_notes = SafetyNoteSerializer(many=True, read_only=True)
    safety_note_ids = serializers.PrimaryKeyRelatedField(
        queryset=SafetyNote.objects.all(), many=True, source='safety_notes', write_only=True, required=False
    )

    class Meta:
        model = ApothecaryItem
        fields = [
            'id',
            'item_id',
            'name',
            'type',
            'form',
            'origin',
            'origin_id',
            'price_usd',
            'stock_oz',
            'volume_ml',
            'container_size_g',
            'preparation',
            'dosage',
            'application',
            'last_updated',
            'uses',
            'use_ids',
            'ingredients',
            'ingredient_ids',
            'safety_notes',
            'safety_note_ids',
        ]
