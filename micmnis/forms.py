from django import forms
from .models import ApothecaryItem, Use, Ingredient, SafetyNote

class ApothecaryItemForm(forms.ModelForm):
    uses = forms.ModelMultipleChoiceField(
        queryset=Use.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple
    )
    ingredients = forms.ModelMultipleChoiceField(
        queryset=Ingredient.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple
    )
    safety_notes = forms.ModelMultipleChoiceField(
        queryset=SafetyNote.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = ApothecaryItem
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Pre-select existing M2M values when editing
        if self.instance.pk:
            self.fields['uses'].initial = self.instance.uses.all()
            self.fields['ingredients'].initial = self.instance.ingredients.all()
            self.fields['safety_notes'].initial = self.instance.safety_notes.all()

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
            instance.uses.set(self.cleaned_data['uses'])
            instance.ingredients.set(self.cleaned_data['ingredients'])
            instance.safety_notes.set(self.cleaned_data['safety_notes'])
        return instance

# Form for Use Model
class UseForm(forms.ModelForm):
    class Meta:
        model = Use
        fields = ['name', 'items']
        widgets = {
            'items': forms.CheckboxSelectMultiple(),
        }

# Form for Ingredient Model
class IngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = ['name', 'items']
        widgets = {
            'items': forms.CheckboxSelectMultiple(),
        }

# Form for SafetyNote Model
class SafetyNoteForm(forms.ModelForm):
    class Meta:
        model = SafetyNote
        fields = ['text', 'items']
        widgets = {
            'items': forms.CheckboxSelectMultiple(),
        }