from django import forms
from appTrigorojo.models import Producto

class FormularioProducto(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ('nombre', 'descripcion', 'cantidad', 'precio', 'categoria')
        labels = {
            'nombre': 'Nombre del producto:',
            'descripcion': 'Descripción:',
            'cantidad': 'Cantidad disponible:',
            'precio': 'Precio:',
            'categoria': 'Categoría:',
        }

