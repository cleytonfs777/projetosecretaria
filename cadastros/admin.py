from django.contrib import admin
from .models import Militar, Empenho

class EmpenhoInline(admin.TabularInline):  # ou admin.StackedInline, dependendo da sua preferência de visualização.
    model = Militar.empenhos.through
    extra = 1

class MilitarAdmin(admin.ModelAdmin):
    inlines = [EmpenhoInline]

admin.site.register(Militar, MilitarAdmin)
admin.site.register(Empenho)

