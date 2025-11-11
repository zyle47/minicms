from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ApothecaryItemViewSet, OriginViewSet, UseViewSet, IngredientViewSet, SafetyNoteViewSet
)
from . import views_html

router = DefaultRouter()
router.register(r'origins', OriginViewSet)
router.register(r'uses', UseViewSet)
router.register(r'ingredients', IngredientViewSet)
router.register(r'safety_notes', SafetyNoteViewSet)
router.register(r'inventory', ApothecaryItemViewSet, basename='apothecaryitem')

urlpatterns = [
    path('api/', include(router.urls)),

    # HTML CRUD
    path('', views_html.inventory_list, name='inventory_list'),
    path("ajax/search/", views_html.ajax_inventory_search, name="ajax_inventory_search"),
    # path('login/', views_html.login_view, name='login'),
    # Item URLs
    path('item/<int:pk>/', views_html.inventory_detail, name='inventory_detail'),
    path('item/new/', views_html.inventory_create, name='inventory_create'),
    path('item/<int:pk>/edit/', views_html.inventory_update, name='inventory_update'),
    path('item/<int:pk>/delete/', views_html.inventory_delete, name='inventory_delete'),

    # Uses URLs
    path('use/create/', views_html.create_use, name='create_use'),
    path('use/<int:pk>/edit/', views_html.edit_use, name='edit_use'),
    path('use/', views_html.use_list, name='use_list'),  # You can create a list view for use items
    
    # Ingredient URLs
    path('ingredient/create/', views_html.create_ingredient, name='create_ingredient'),
    path('ingredient/<int:pk>/edit/', views_html.edit_ingredient, name='edit_ingredient'),
    path('ingredient/', views_html.ingredient_list, name='ingredient_list'),  # List view for ingredients
    
    # SafetyNote URLs
    path('safety_note/create/', views_html.create_safety_note, name='create_safety_note'),
    path('safety_note/<int:pk>/edit/', views_html.edit_safety_note, name='edit_safety_note'),
    path('safety_note/', views_html.safety_note_list, name='safety_note_list'),  # List view for safety notes
]
