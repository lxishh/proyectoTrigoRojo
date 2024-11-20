from django.shortcuts import render, get_object_or_404
from appTrigorojo.models import Categoria, Producto

# Create your views here.
def index(request):
    categorias = Categoria.objects.all()
    context = {'categorias': categorias}
    return render(request, 'index.html', context)

def login(request):
    return render(request, 'login.html')

def administracion(request):
    return render(request, 'administracion.html')

def productos_view(request):
    productos = Producto.objects.all()
    context = {'productos':productos}
    return render(request, 'productos.html', context)

def ventas_view(request):
    return render(request, 'ventas.html')

def productos_por_categoria(request, categoria_id):
    categoria = get_object_or_404(Categoria, id=categoria_id)
    productos = Producto.objects.filter(categoria=categoria)
    context = {'categoria': categoria, 'productos': productos}
    return render(request, 'productos_por_categoria.html', context)