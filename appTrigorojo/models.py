from django.db import models

# Create your models here.
class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)  # Descripción opcional 
    imagen = models.ImageField(upload_to='categorias/', blank=True, null=True)  # Imagen opcional 

    class Meta:
        db_table = 'categorias'  # Nombre de la tabla en la base de datos
        verbose_name = 'categoria'
        verbose_name_plural = 'categorias'

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    cantidad = models.PositiveIntegerField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    fecha_ingreso = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'productos'  # Nombre de la tabla en la base de datos
        verbose_name = 'producto'
        verbose_name_plural = 'productos'

    def __str__(self):
        return self.nombre