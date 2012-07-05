# -*- coding:utf-8 -*-
# author: bcabezas@apsl.net

from django.db import models

from cms.models.fields import PlaceholderField
from cms.models import CMSPlugin
from easy_thumbnails.files import get_thumbnailer
from django.conf import settings
from django.contrib.staticfiles.finders import find as staticfiles_find
import os
import re

class SliderImage(models.Model):
    """Image class that user django-filer"""
    name = models.CharField(max_length=150, blank=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="jcslider")
    order = models.PositiveIntegerField(default=100)

    class Meta:
        verbose_name = u'Image'
        verbose_name_plural = u'Images'
        ordering = ('order', 'name',)

    def __unicode__(self):
        if self.name:
            name = self.name
        else:
            try:
                name = self.image.file.name.split("/")[-1]
            except:
                name = unicode(self.image)
        return "%s"  % name

    def thumb(self):
        thumbnail_options = dict(size=(92, 37), crop=True)
        url =  get_thumbnailer(self.image).get_thumbnail(thumbnail_options).url
        return '<img src="%s">' % url
    thumb.allow_tags = True
    thumb.short_description = 'Image'


class SliderAlbum(models.Model):
    """Image gallery for slider"""
    name = models.CharField(max_length=150)
    images = models.ManyToManyField(SliderImage, blank=True)

    class Meta:
        verbose_name = u'Slider Album'
        verbose_name_plural = u'Sliders Album'

    def __unicode__(self):
        return self.name or ""


class SliderPlugin(CMSPlugin):
    title = models.CharField('Title', max_length=255, null=True, blank=True)
    album = models.ForeignKey(SliderAlbum)
    anim_speed = models.PositiveIntegerField(default=500, help_text="Animation Speed (ms)")
    pause_time = models.PositiveIntegerField(default=3000, help_text="Pause time (ms)")
    image_width = models.PositiveIntegerField(null=True, blank=True,
            help_text="Width for images. Only requided for flexible theme types. Blank for theme spec auto.detection")
    image_height = models.PositiveIntegerField(null=True, blank=True,
            help_text="Height for images. Only requided for flexible theme types. Blank for theme spec auto.detection")
    show_ribbon = models.BooleanField(default=True, help_text="Show ribbon logo")

    def __unicode__(self):
        if self.title:
            return self.title

    # def read_theme_css(self):
    #     cssfile = staticfiles_find("nivo/themes/%(theme)s/%(theme)s.css" % self.__dict__)
    #     return open(cssfile).read()

    # def get_theme_type(self):
    #     """ Get geometry type from the doc header of css theme file"""
    #     css = self.read_theme_css()
    #     rawstr = r""".*Skin Type: (?P<gtype>\w+?)\s"""
    #     match_obj = re.search(rawstr, css,  re.MULTILINE| re.DOTALL)
    #     gtype = match_obj.group('gtype')
    #     return gtype

    # def get_theme_geometry(self):
    #     """ Get with and heigth from the doc header of css theme file"""
    #     css = self.read_theme_css()
    #     rawstr = r"""Image Width: (?P<width>\d+).*Image Height: (?P<height>\d+)"""
    #     match_obj = re.search(rawstr, css,  re.MULTILINE| re.DOTALL)
    #     width = match_obj.group('width')
    #     height = match_obj.group('height')
    #     return (width, height)

    def save(self, *args, **kwargs):
        # if self.get_theme_type() != 'flexible':
        #     width, height = self.get_theme_geometry()
        #     self.image_width = width
        #     self.image_height = height
        super(SliderPlugin, self).save(*args, **kwargs)

    search_fields = ('title',)
