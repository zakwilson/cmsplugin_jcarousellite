#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: bcabezas@apsl.net

""" Registro de las clases en el admin de django """

from django.contrib import admin
from .models import  SliderImage, SliderAlbum

class SliderImageAdmin(admin.ModelAdmin):
    list_display = ('thumb', 'name','description',  'order')
admin.site.register(SliderImage, SliderImageAdmin)

class SliderAlbumAdmin(admin.ModelAdmin):
    filter_horizontal = 'images',
    
admin.site.register(SliderAlbum, SliderAlbumAdmin)
