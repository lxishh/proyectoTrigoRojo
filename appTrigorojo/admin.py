from django.contrib import admin
from appTrigorojo.models import Producto, Categoria

class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion', 'cantidad', 'precio', 'categoria', 'fecha_ingreso')
    list_filter = ('categoria', 'fecha_ingreso')  # Filtros disponibles en el admin
# Register your models here.
admin.site.register(Producto, ProductoAdmin)
admin.site.register(Categoria)