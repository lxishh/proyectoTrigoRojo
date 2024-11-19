from django.shortcuts import render, get_object_or_404
from appTrigorojo.models import Categoria, Producto

# Create your views here.
def index(request):
    categorias = Categoria.objects.all()
    data = {'categorias': categorias}
    return render(request, 'index.html', data)


def login(request):
    return render(request, 'login.html')

def administracion(request):
    return render(request, 'administracion.html')

def productos_view(request):
    return render(request, 'productos.html')

def ventas_view(request):
    return render(request, 'ventas.html')

def productos_por_categoria(request, categoria_id):
    categoria = get_object_or_404(Categoria, id=categoria_id)
    productos = Producto.objects.filter(categoria=categoria)
    data = {'categoria': categoria, 'productos': productos}
    return render(request, 'productos_por_categoria.html', data)