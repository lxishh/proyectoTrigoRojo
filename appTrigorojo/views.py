from django.shortcuts import render, redirect, get_object_or_404
from appTrigorojo.models import Categoria, Producto
from appTrigorojo.forms import FormularioProducto
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import logout
from django.contrib.auth.models import User, Group
from django.contrib import messages

# Create your views here.
def index(request):
    categorias = Categoria.objects.all()
    context = {'categorias': categorias}
    return render(request, 'index.html', context)

# esta def solamente se ocupa para poder hacer uso del content block
def administracion(request):
    return render(request, 'administracion.html')

def login(request):
    return render(request, 'login.html')

def salir(request):
    logout(request)
    return redirect('index')

# Funciones para verificar si el usuario es Propietario/Vendedora
def es_propietario(user):
    return user.groups.filter(name='Propietario').exists()

def es_vendedor(user):
    return user.groups.filter(name='Vendedor').exists()

def lista_usuarios(request):
    # Verifica que el usuario sea Propietario
    if not request.user.groups.filter(name='Propietario').exists():
        return redirect('..')  

    # Obtiene todos los usuarios, pero excluye superusuarios
    usuarios = User.objects.filter(is_superuser=False)  

    #contexto
    context = {'usuarios': usuarios}

    return render(request, 'lista_usuarios.html', context)


def crear_usuario(request):
    # Verifica que el usuario sea Propietario
    if not request.user.groups.filter(name='Propietario').exists():
        return redirect('..')  

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        group_name = request.POST.get('group')

        # Validar que no se asigne el grupo 'Propietario'
        if group_name == 'Propietario':
            messages.error(request, "No tienes permiso para crear usuarios con el grupo Propietario.")
            return redirect('crear_usuario')

        # Crear el nuevo usuario
        user = User.objects.create_user(username=username, email=email, password=password)

        # Asignar el grupo
        group = Group.objects.get(name=group_name)
        user.groups.add(group)

        messages.success(request, f"El usuario {username} ha sido creado con éxito.")
        return redirect('usuarios')  # O la página que desees redirigir después de la creación

    # Pasar todos los grupos al template excepto 'Propietario'
    grupos = Group.objects.exclude(name='Propietario')
    return render(request, 'crear_usuario.html', {'grupos': grupos})


def actualizar_usuario(request, id):
    # Verifica que el usuario sea Propietario
    if not request.user.groups.filter(name='Propietario').exists():
        return redirect('..')

    # Obtener el usuario a editar
    usuario = get_object_or_404(User, id=id)

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        group_name = request.POST.get('group')

        # Actualizar información del usuario
        usuario.username = username
        usuario.email = email

        # Reasignar el grupo
        if group_name:
            group = Group.objects.get(name=group_name)
            usuario.groups.clear()  # Elimina todos los grupos actuales
            usuario.groups.add(group)

        usuario.save()
        messages.success(request, f"El usuario {usuario.username} ha sido actualizado con éxito.")
        return redirect('usuarios')  # O la página que desees redirigir después de la actualización

    # Filtrar los grupos, excluyendo 'Propietario' y otros si es necesario
    grupos = Group.objects.exclude(name='Propietario')  # Excluir el grupo 'Propietario'

    # Contexto inicial para el formulario
    context = {
        'usuario': usuario,
        'grupos': grupos,
    }
    return render(request, 'crear_usuario.html', context)


def eliminar_usuario(request, id):
    # Verifica que el usuario sea Propietario
    if not request.user.groups.filter(name='Propietario').exists():
        return redirect('..')  # Redirigir si no es propietario

    # Obtén el usuario que se desea eliminar
    usuario = get_object_or_404(User, id=id)

    # Eliminar el usuario
    usuario.delete()

    # Mensaje de éxito
    messages.success(request, f"El usuario {usuario.username} ha sido eliminado con éxito.")
    
    # Redirigir a la lista de usuarios
    return redirect('usuarios')  # Asegúrate de que 'usuarios' sea el nombre correcto de la URL de lista de usuarios

@login_required
def perfil_redirect(request):
    if request.user.is_superuser:  # Verificar si es superusuario
        return redirect('/admin/')  # Redirigir al panel de administración
    elif es_propietario(request.user):
        return redirect('/productos')  # Redirigir a la vista de productos para el propietario
    elif es_vendedor(request.user):
        return redirect('/ventas')  # Redirigir a la vista de ventas para el vendedor
    else:
        return redirect('index')  # Si no es ni propietario ni vendedor, redirigir al inicio


def listar_productos(request):
    categoria = request.GET.get('categoria', None)  # Filtro por nombre de categoría
    
    # Obtener todos los productos
    productos = Producto.objects.all()
    
    # Filtrar productos por nombre de categoría si se especifica
    if categoria:
        productos = productos.filter(categoria__nombre=categoria)

    # Obtener las categorías distintas para los filtros
    categorias = Categoria.objects.values_list('nombre', flat=True).distinct()

    # Pasar los productos y las categorías al contexto
    context = {
        'productos': productos,
        'categorias': categorias,
    }

    # Renderizar la página con el contexto
    return render(request, 'productos.html', context)

def registrar_producto(request):
    form = FormularioProducto()
    if request.method == 'POST':
        form = FormularioProducto(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/productos')
    else:
        form = FormularioProducto()
    context = {'form':form}
    return render(request, 'registrar_productos.html', context)

def actualizar_producto(request, id):
    producto = Producto.objects.get(id=id)
    form = FormularioProducto(instance=producto)
    if request.method == 'POST':
        form = FormularioProducto(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('/productos')
    else:
        form = FormularioProducto(instance=producto)
    context = {'form':form}
    return render(request, 'registrar_productos.html', context)

def eliminar_producto(request, id):
    producto = Producto.objects.get(id=id)
    producto.delete()
    return redirect('/productos')

def productos_por_categoria(request, categoria_id):
    categoria = get_object_or_404(Categoria, id=categoria_id)
    productos = Producto.objects.filter(categoria=categoria)
    context = {'categoria': categoria, 'productos': productos}
    return render(request, 'productos_por_categoria.html', context)

def ventas_view(request):
    return render(request, 'ventas.html')