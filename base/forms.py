# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django import forms
from .models import Kitchen, Category

class KitchenForm(forms.ModelForm):

    class Meta:
        model = Kitchen
        fields = ['kitchen_name', 'kitchen_logo', 'about', 'contact', 'address_line_1', 'address_line_2', 'fb_link', 'insta_link']

    def __init__(self, *args, **kwargs):
        super(KitchenForm, self).__init__(*args, **kwargs)
        self.fields['kitchen_name'].widget.attrs['readonly'] = True
        # self.fields['mail'].widget.attrs['readonly'] = True
        # self.fields['slug'].widget.attrs['readonly'] = True


class CategoryForm(forms.ModelForm):

    class Meta:
        model = Category
        fields = ['category_title', 'active']
