"""
Definition of forms.
"""

from django import forms
from django.forms import ModelForm

from app.models import Product, StoreCategory
from shop.models import Category, SubCategory
from .models import *

# Create the form class.
class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = [
                'online_image_url',
                'product_category',
                'name' ,
                'store',
                'description',
                'price',
                'link']
        
        
class StoreCategoryForm(ModelForm):
    class Meta:
        model = StoreCategory
        fields = [
                'image',
                'name' ,
                'link']
class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = [
                'name',
                'slug',
                'online_image',
                'online_link',
                ]
        
class SubCategoryForm(ModelForm):
    class Meta:
        model = SubCategory
        fields = [
                'name',
                'slug',
                'category',
                ]