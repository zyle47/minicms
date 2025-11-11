from django.shortcuts import render, get_object_or_404, redirect
from .models import ApothecaryItem, Origin, Use
from django.db.models import Q
from .forms import ApothecaryItemForm  # if you separated your form earlier
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required

# ----------------------------
# CRUD Views
# ----------------------------

# List view


def inventory_list(request):
    query = request.GET.get("q", "")
    type_filter = request.GET.get("type", "")
    origin_filter = request.GET.get("origin", "")
    use_filter = request.GET.get("use", "")

    items = ApothecaryItem.objects.all().select_related("origin").prefetch_related("uses")

    # Search logic
    if query:
        items = items.filter(
            Q(name__icontains=query)
            | Q(item_id__icontains=query)
            | Q(form__icontains=query)
        )

    # Filter by type
    if type_filter:
        items = items.filter(type=type_filter)

    # Filter by origin
    if origin_filter:
        items = items.filter(origin__country=origin_filter)

    # Filter by use
    if use_filter:
        items = items.filter(uses__name=use_filter)

    # Build dropdown filter lists
    types = ApothecaryItem.TYPE_CHOICES
    origins = Origin.objects.all().order_by("country")
    uses = Use.objects.all().order_by("name")

    context = {
        "items": items.distinct(),
        "query": query,
        "type_filter": type_filter,
        "origin_filter": origin_filter,
        "use_filter": use_filter,
        "types": types,
        "origins": origins,
        "uses": uses,
    }

    return render(request, "micmnis/inventory_list.html", context)


# Detail view
def inventory_detail(request, pk):
    item = get_object_or_404(ApothecaryItem, pk=pk)
    return render(request, 'micmnis/inventory_detail.html', {'item': item})

# Create view
@login_required
def inventory_create(request):
    if request.method == 'POST':
        form = ApothecaryItemForm(request.POST)
        if form.is_valid():
            form.save()  # Save the instance
            form.save_m2m()  # Ensure the many-to-many relationships are saved
            return redirect('inventory_list')
    else:
        form = ApothecaryItemForm()
    return render(request, 'micmnis/inventory_form.html', {'form': form})


# Update view
@login_required
def inventory_update(request, pk):
    item = ApothecaryItem.objects.get(pk=pk)
    
    if request.method == 'POST':
        form = ApothecaryItemForm(request.POST, instance=item)
        
        if form.is_valid():
            form.save()  # Save the instance
            form.save_m2m()  # Ensure the many-to-many relationships are saved
            
            return redirect('inventory_detail', pk=item.pk)  # Redirect to the detail page of the item
        else:
            return render(request, 'micmnis/inventory_edit.html', {'form': form})

    else:
        form = ApothecaryItemForm(instance=item)
        return render(request, 'micmnis/inventory_edit.html', {'form': form})


# Delete view
@login_required
def inventory_delete(request, pk):
    item = get_object_or_404(ApothecaryItem, pk=pk)
    if request.method == 'POST':
        item.delete()
        return redirect('inventory_list')
    return render(request, 'micmnis/inventory_confirm_delete.html', {'item': item})


def ajax_inventory_search(request):
    """Returns filtered table HTML for AJAX updates"""
    query = request.GET.get("q", "")
    type_filter = request.GET.get("type", "")
    origin_filter = request.GET.get("origin", "")
    use_filter = request.GET.get("use", "")
    sort = request.GET.get("sort", "name")

    items = ApothecaryItem.objects.all().select_related("origin").prefetch_related("uses")

    if query:
        items = items.filter(
            Q(name__icontains=query)
            | Q(item_id__icontains=query)
            | Q(origin__country__icontains=query)
            | Q(type__icontains=query)
        )

    if type_filter:
        items = items.filter(type=type_filter)
    if origin_filter:
        items = items.filter(origin__country=origin_filter)
    if use_filter:
        items = items.filter(uses__name=use_filter)

    # Sorting support
    if sort:
        if sort.startswith("-"):
            items = items.order_by(sort)
        else:
            items = items.order_by(sort)

    html = render_to_string("micmnis/partials/inventory_table.html", {"items": items.distinct()})
    return JsonResponse({"html": html})

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Use, Ingredient, SafetyNote
from .forms import UseForm, IngredientForm, SafetyNoteForm

# View to create a new Use
def create_use(request):
    if request.method == 'POST':
        form = UseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('use_list')  # Redirect to a list view after saving
    else:
        form = UseForm()
    return render(request, 'micmnis/use/create_use.html', {'form': form})

# View to edit an existing Use
def edit_use(request, pk):
    use = get_object_or_404(Use, pk=pk)
    if request.method == 'POST':
        form = UseForm(request.POST, instance=use)
        if form.is_valid():
            form.save()
            return redirect('use_list')  # Redirect to list after saving
    else:
        form = UseForm(instance=use)
    return render(request, 'micmnis/use/edit_use.html', {'form': form, 'use': use})

# View to create a new Ingredient
def create_ingredient(request):
    if request.method == 'POST':
        form = IngredientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('ingredient_list')  # Redirect to list after saving
    else:
        form = IngredientForm()
    return render(request, 'micmnis/ingredient/create_ingredient.html', {'form': form})

# View to edit an existing Ingredient
def edit_ingredient(request, pk):
    ingredient = get_object_or_404(Ingredient, pk=pk)
    if request.method == 'POST':
        form = IngredientForm(request.POST, instance=ingredient)
        if form.is_valid():
            form.save()
            return redirect('ingredient_list')  # Redirect to list after saving
    else:
        form = IngredientForm(instance=ingredient)
    return render(request, 'micmnis/ingredient/edit_ingredient.html', {'form': form, 'ingredient': ingredient})

# View to create a new SafetyNote
def create_safety_note(request):
    if request.method == 'POST':
        form = SafetyNoteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('safety_note_list')  # Redirect to list after saving
    else:
        form = SafetyNoteForm()
    return render(request, 'micmnis/safety_note/create_safety_note.html', {'form': form})

# View to edit an existing SafetyNote
def edit_safety_note(request, pk):
    safety_note = get_object_or_404(SafetyNote, pk=pk)
    if request.method == 'POST':
        form = SafetyNoteForm(request.POST, instance=safety_note)
        if form.is_valid():
            form.save()
            return redirect('safety_note_list')  # Redirect to list after saving
    else:
        form = SafetyNoteForm(instance=safety_note)
    return render(request, 'micmnis/safety_note/edit_safety_note.html', {'form': form, 'safety_note': safety_note})


# views.py

def use_list(request):
    uses = Use.objects.all()
    return render(request, 'micmnis/use/use_list.html', {'uses': uses})

def ingredient_list(request):
    ingredients = Ingredient.objects.all()
    return render(request, 'micmnis/ingredient/ingredient_list.html', {'ingredients': ingredients})

def safety_note_list(request):
    safety_notes = SafetyNote.objects.all()
    return render(request, 'micmnis/safety_note/safety_note_list.html', {'safety_notes': safety_notes})
