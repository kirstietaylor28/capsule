# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from .models import Hat


class create_hat(admin.ModelAdmin):
	list_display = ['style']
	class Meta:
		model = Hat


# Register your models here.
admin.site.register(Hat, create_hat)
