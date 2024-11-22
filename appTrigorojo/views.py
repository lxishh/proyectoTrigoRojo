from django.shortcuts import render, redirect, get_object_or_404
from appTrigorojo.models import Categoria, Producto
from appTrigorojo.forms import FormularioProducto
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import logout
from django.contrib.auth.models import User, Group
from django.contrib import messages
from django.db import connection

# Create your views here.

def index(request):
    categorias = Categoria.objects.all()
    context = {'categorias': categorias}
    return render(request, 'index.html', context)

# Esta def solamente se ocupa para poder hacer uso del content block
def administracion(request):
    return render(request, 'administracion.html')

#def que te lleva a la template de login
def login(request):
    return render(request, 'login.html')

def salir(request):
    logout(request)
    return redirect('index')

# Funciones para verificar si el usuario es Propietario o Vendedor
def es_propietario(user):
    return user.groups.filter(name='Propietario').exists()

def es_vendedor(user):
    return user.groups.filter(name='Vendedor').exists()


#Funcion que llama al template de lista de usuarios y donde se le pasan los usuarios
def lista_usuarios(request): 

    # Obtiene todos los usuarios, pero excluye superusuarios
    usuarios = User.objects.filter(is_superuser=False)  

    #contexto
    context = {'usuarios': usuarios}

    return render(request, 'lista_usuarios.html', context)


#Funcion que llama al template de crear_usuario (donde es un formulario) y los campos se le pasan
def crear_usuario(request):

    #Valida si el formulario tiene un metodo POST
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
        return redirect('/productos')   # Redirigir a la vista de productos
    elif es_propietario(request.user):
        return redirect('/productos')  # Redirigir a la vista de productos para el propietario
    elif es_vendedor(request.user):
        return redirect('/ventas')  # Redirigir a la vista de ventas para el vendedor
    else:
        return redirect('index')  # Si no es ni propietario ni vendedor, redirigir al inicio





# Función para ejecutar procedimientos almacenados
def ejecutar_procedimiento(proc_nombre, params=()): #se define que se debe pasar el nombre del procedimiento y los parametros respectivos
    with connection.cursor() as cursor:
        cursor.callproc(proc_nombre, params)
        if proc_nombre in ['listar_productos']:  # Solo obtener resultados si es un SELECT
            return cursor.fetchall()
        return None

# Vista para listar productos usando el procedimiento almacenado
def listar_productos(request):
    productos_raw = ejecutar_procedimiento('listar_productos')

    # Asume que el procedimiento devuelve las columnas en este orden
    productos = [
        {
            'id': p[0],
            'nombre': p[1],
            'descripcion': p[2],
            'cantidad': p[3],
            'precio': p[4],
            'categoria': p[5],
            'fecha_ingreso': p[6],
        }
        for p in productos_raw
    ]

    categorias = Categoria.objects.all()
    context = {
        'productos': productos,
        'categorias': categorias,
    }
    return render(request, 'productos.html', context)


# Vista para registrar un producto usando el procedimiento almacenado
def registrar_producto(request):
    form = FormularioProducto()
    if request.method == 'POST':
        form = FormularioProducto(request.POST)
        if form.is_valid():
            nombre = form.cleaned_data['nombre']
            descripcion = form.cleaned_data['descripcion']
            cantidad = form.cleaned_data['cantidad']
            precio = form.cleaned_data['precio']
            categoria_id = form.cleaned_data['categoria'].id  # Asumimos que se está pasando un objeto de categoría
            
            # Llamamos al procedimiento almacenado para registrar el producto
            ejecutar_procedimiento('registrar_producto', [nombre, descripcion, cantidad, precio, categoria_id])
            return redirect('/productos')
        
    context = {'form': form}
    return render(request, 'registrar_productos.html', context)

# Vista para actualizar un producto usando el procedimiento almacenado
def actualizar_producto(request, id):
    producto = Producto.objects.get(id=id)
    form = FormularioProducto(instance=producto)
    
    if request.method == 'POST':
        form = FormularioProducto(request.POST, instance=producto)
        if form.is_valid():
            nombre = form.cleaned_data['nombre']
            descripcion = form.cleaned_data['descripcion']
            cantidad = form.cleaned_data['cantidad']
            precio = form.cleaned_data['precio']
            categoria_id = form.cleaned_data['categoria'].id  # Asumimos que se está pasando un objeto de categoría
            
            # Llamamos al procedimiento almacenado para actualizar el producto
            ejecutar_procedimiento('actualizar_producto', [id, nombre, descripcion, cantidad, precio, categoria_id])
            return redirect('/productos')
    
    context = {'form': form}
    return render(request, 'registrar_productos.html', context)

# Vista para eliminar un producto usando el procedimiento almacenado
def eliminar_producto(request, id):
    # Llamamos al procedimiento almacenado para eliminar el producto
    ejecutar_procedimiento('eliminar_producto', [id])
    return redirect('/productos')


#Vista que llama a los modelos de categoria y productos, y luego el html hace que se muestren bien
def productos_por_categoria(request, categoria_id):
    categoria = get_object_or_404(Categoria, id=categoria_id)
    productos = Producto.objects.filter(categoria=categoria)
    context = {'categoria': categoria, 'productos': productos}
    return render(request, 'productos_por_categoria.html', context)

def ventas_view(request):
    return render(request, 'ventas.html')