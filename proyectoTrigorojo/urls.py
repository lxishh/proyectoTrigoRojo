"""proyectoTrigorojo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from appTrigorojo import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('administracion/', views.administracion),
    path('login/', views.login, name='login'),
    path('salir/', views.salir),
    path('accounts/', include('django.contrib.auth.urls')),
    path('perfil_redirect/', views.perfil_redirect, name='perfil_redirect'),
    path('lista_usuarios/', views.lista_usuarios, name='usuarios'),
    path('crear_usuario/', views.crear_usuario, name='crear_usuario'),
    path('actualizar_usuario/<int:id>/', views.actualizar_usuario, name='actualizar_usuario'),
    path('eliminar_usuario/<int:id>/', views.eliminar_usuario, name='eliminar_usuario'),
    path('categoria/<int:categoria_id>/productos/', views.productos_por_categoria, name='productos_por_categoria'),
    path('productos/', views.listar_productos),
    path('registrar_producto/', views.registrar_producto),
    path('actualizar_producto/<int:id>', views.actualizar_producto),
    path('eliminar_producto/<int:id>', views.eliminar_producto),
    path('ventas/', views.ventas_view),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # Esto sirve las imágenes y archivos de medios
