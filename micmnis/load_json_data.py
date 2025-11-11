import json
from micmnis.models import ApothecaryItem, Origin, Use, Ingredient, SafetyNote

def load_data(file_path='data.json'):
    with open(file_path, 'r') as f:
        data = json.load(f)

    for item in data.get('apothecary_inventory', []):
        origin_obj, _ = Origin.objects.get_or_create(country=item.get('origin', 'Unknown'))

        ap_item, _ = ApothecaryItem.objects.update_or_create(
            item_id=item.get('id'),
            defaults={
                'name': item.get('name'),
                'type': item.get('type')[:10],
                'form': item.get('form', ''),
                'origin': origin_obj,
                'price_usd': item.get('price_usd') or item.get('price_per_oz_usd', 0),
                'stock_oz': item.get('stock_oz'),
                'volume_ml': item.get('volume_ml'),
                'container_size_g': item.get('container_size_g'),
                'preparation': item.get('preparation', ''),
                'dosage': item.get('dosage', ''),
                'application': item.get('application', ''),
            }
        )

        for use in item.get('uses', []):
            use_obj, _ = Use.objects.get_or_create(name=use)
            ap_item.uses.add(use_obj)

        for ing in item.get('ingredients', []):
            ing_obj, _ = Ingredient.objects.get_or_create(name=ing)
            ap_item.ingredients.add(ing_obj)

        for note in item.get('safety_notes', []):
            note_obj, _ = SafetyNote.objects.get_or_create(text=note)
            ap_item.safety_notes.add(note_obj)
