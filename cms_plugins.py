#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: bcabezas@apsl.net

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from .models import SliderPlugin

class CMSSliderPlugin(CMSPluginBase):
    model = SliderPlugin
    name = 'Slider Plugin'
    render_template = 'jcarousellite/slider.html'
    text_enabled = False
    admin_preview = False

    def render(self, context, instance, placeholder):
        if instance.image_height and instance.image_width:
            size = (instance.image_width, instance.image_height)
        else:
            size = None
        context.update({
            'object': instance,
            'placeholder': placeholder,
            'images': instance.album.images.all(),
            'size': size,
        })
        return context

plugin_pool.register_plugin(CMSSliderPlugin)
