import unicodedata
from tabulate import tabulate

def normalizar_texto(texto):
   #Normaliza el texto eliminando acentos y convirtiendo a minúsculas
    return ''.join(
        char for char in unicodedata.normalize('NFKD', texto.lower())
        if unicodedata.category(char) != 'Mn'
    )
    
# Definición de la clase Producto para representar elementos en el inventario
class Producto: 
    # Constructor de la clase que inicializa los atributos
    def __init__(self, nombre, categoria, referencia, precio, cantidad):
        self.__nombre_normalizado = normalizar_texto(nombre) # Atributos privados (encapsulamiento) usando doble guión bajo. Esto previene el acceso directo desde fuera de la clase
        self.__categoria_normalizada = normalizar_texto(categoria)
        self.__nombre = nombre
        self.__categoria=categoria
        self.__set_referencia(referencia) # Llamada al método privado de validación de referencia
        self.__set_precio(precio)
        self.__set_cantidad(cantidad)

# Métodos getter para acceder a los atributos privados de manera controlada
    def get_nombre(self):
        return self.__nombre

    def get_categoria(self):
        return self.__categoria
    
    def get_referencia(self):
        return self.__referencia

    def get_precio(self):
        return self.__precio

    def get_cantidad(self):
        return self.__cantidad
    
    def get_nombre_normalizado(self):
        return self.__nombre_normalizado
    
    def get_categoria_normalizada(self):
        return self.__categoria_normalizada

# Métodos setter privados con validaciones para prevenir valores incorrectos
    def __set_referencia(self, referencia):
        if referencia <= 0:
            raise ValueError("Introduzca una referencia válida (debe ser >0)")
        self.__referencia = referencia
        
    def __set_precio(self, precio):
        if precio <= 0:
            raise ValueError("El precio debe ser superior a 0€")
        self.__precio = precio

    def __set_cantidad(self, cantidad):
        if cantidad < 0:
            raise ValueError("La cantidad no puede ser negativa")
        self.__cantidad = cantidad
        
    # Métodos públicos para actualizar referencia, precio y/o cantidad que reutilizan los métodos de validación    
    def actualizar_referencia(self, nueva_referencia):
        self.__set_referencia(nueva_referencia)

    def actualizar_precio(self, nuevo_precio):
        self.__set_precio(nuevo_precio)

    def actualizar_cantidad(self, nueva_cantidad):
        self.__set_cantidad(nueva_cantidad)

    # Método especial para representación en cadena del objeto
    def __str__(self):
        # Da formato a la información del producto para que se lea bien
        return f"Producto: {self.__nombre} | Categoría: {self.__categoria} | Referencia: {self.__referencia:010d} | Precio: {self.__precio:.2f}€ | Stock: {self.__cantidad}"

# Definición de la clase Inventario para gestionar los productos y sus operaciones asociadas
class Inventario:
    #Inicializa un invetario vacio
    def __init__(self):
        # Listas privadas para almacenar los productos
        self.__productos = []
        self.__nombres_normalizados = set()
        self.__categorias_formato = {} #usamos un diccionario para mantener la referencia a las categorías originales

    def agregar_producto(self, producto):
        #Agrega un nuevo producto
        nombre_norm = producto.get_nombre_normalizado()
        categoria_norm = producto.get_categoria_normalizada()
        
        # Previene la adición de productos o categorías con nombres duplicados
        if nombre_norm in self.__nombres_normalizados:
            raise ValueError(f"Ya existe un producto con el nombre {producto.get_nombre()}") 
        #si la categoria normalizada ya existe, se usa la categoría original
        if categoria_norm in self.__categorias_formato:
            #Asignala categoría original al producto para mantener la consistencia
            categoria_origen = self.__categorias_formato[categoria_norm]
        else:
            #si es una nueva categoría la guarda como categoría original
            self.__categorias_formato[categoria_norm] = producto.get_categoria() 
        
        #añade el producto y su nombre normalizado
        self.__productos.append(producto)
        self.__nombres_normalizados.add(nombre_norm)
        print(f"Producto '{producto.get_nombre()}' agregado a la categoría '{producto.get_categoria()}'")

    def actualizar_producto(self, nombre, nueva_referencia=None, nuevo_precio=None, nueva_cantidad=None):
        #Actualiza la referencia, el precio o cantidad de un producto existente
        producto = self.buscar_producto(nombre)
        if not producto:
            # Busca el producto y lanza error si no existe
            raise ValueError(f"No se encontró el producto '{nombre}'") 

#Actualiza los atributos seleccionados de un producto existente
        if nueva_referencia is not None:
            producto.actualizar_referencia(nueva_referencia)
        if nuevo_precio is not None:
            producto.actualizar_precio(nuevo_precio)
        if nueva_cantidad is not None:
            producto.actualizar_cantidad(nueva_cantidad)
        print(f"Producto '{nombre}' actualizado")

 #Elimina un producto del inventario
    def eliminar_producto(self, nombre):
       
        producto = self.buscar_producto(nombre)
        if not producto:
            raise ValueError(f"No se encontró el producto '{nombre}'")
        
        print("\nProducto a eliminar:")
        print(producto)
        
        confirmacion = input("\n¿Está seguro que desea eliminar este producto? (s/n): ").lower()
        if confirmacion == 's':
            self.__productos.remove(producto)
            #Confirmación antes de eliminar el producto para descartar arrepentimientos
            print(f"Producto '{nombre}' eliminado")  
        else:
            print("\nOperación cancelada - El producto no fue eliminado, vuelve a intentarlo")

    def mostrar_inventario(self):
        #Muestra todos los productos en el inventario
        if not self.__productos:
            print("El inventario está vacío") 
            return
            
        #preparamos los datos para que se vean como una tabla
        headers = ["Nombre Producto", "Categoría", "Ref.", "Precio (€)", "Uds."]
        tabla_inventario = []
        
        #ordenamos los productos por  categoría y nombre
        productos_ordenados = sorted(self.__productos,
                                     key=lambda x: (x.get_categoria_normalizada(), x.get_nombre_normalizado()))
        
        for producto in productos_ordenados:
            tabla_inventario.append([
                producto.get_nombre(),
                producto.get_categoria(),
                f"{producto.get_referencia():010d}",
                f"{producto.get_precio():.2f}",
                producto.get_cantidad()
            ])
       #mostrar la tabla con formato
        print("\n=== Inventario de Productos en almacén ===")
        print(tabulate(
            tabla_inventario,
            headers=headers,
            tablefmt="grid",  #formato de cuadrícula
            stralign="left",  #alineación de texto a la izquierda
            numalign="right"  #alineación de números a la derecha
        ))
        print(f"\nTotal de Productos: {len(self.__productos)}")
        
        #muestra un resumen por categorías
        print("\nResumen por categorías:")
        categorias = {}
        for producto in self.__productos:
            categoria = producto.get_categoria()
            if categoria not in categorias:
                categorias[categoria] = 0
            categorias[categoria] += 1
        for categoria, cantidad in sorted(categorias.items()):
            print(f"-{categoria}:{cantidad} producto(s)")

    def buscar_producto(self, nombre):
       #Busca un producto por nombre y lo devuelve si existe
        nombre_norm = normalizar_texto(nombre)
        for producto in self.__productos:
            if producto.get_nombre_normalizado() == nombre_norm: 
                return producto
        return None


"""Función principal que maneja el menú"""
def main():
    inventario = Inventario()
    
    # Bucle principal del menú
    while True:
        print("\n===  Gestor de Inventario ===")
        print("1. Agregar nuevo producto")
        print("2. Actualizar producto existente")
        print("3. Eliminar producto")
        print("4. Mostrar inventario")
        print("5. Buscar producto")
        print("6. Salir")
        
        try: # Solicita que elijas una opción y la ejecuta
            opcion = int(input("\nSeleccione una opción: "))
            
            # Estructura de control de las diferentes opciones del menú
            if opcion == 1: # Agrega un producto
                nombre = input("Nombre del producto: ").strip()
                if not nombre:
                   raise ValueError("El producto tiene que tener nombre")
                categoria = input("Categoría: ").strip()
                if not categoria:
                   raise ValueError("La categoría no puede estar vacía")
                referencia = int(input("Referencia:"))
                precio = float(input("Precio: "))
                cantidad = int(input("Cantidad: "))
                
                producto = Producto(nombre, categoria, referencia, precio, cantidad)
                inventario.agregar_producto(producto)
                
            elif opcion == 2: # Actualiza un producto
                nombre = input("Nombre del producto a actualizar: ").strip()
                if not nombre:
                    raise ValueError("El producto tiene que tener nombre")
                actualizar_referencia = input("¿Desea actualizar la referencia? (s/n): ").lower() == 's'
                actualizar_precio = input("¿Desea actualizar el precio? (s/n): ").lower() == 's'
                actualizar_cantidad = input("¿Desea actualizar la cantidad? (s/n): ").lower() == 's'
                
                nueva_referencia = int(input("Nueva referencia: ")) if actualizar_referencia else None
                nuevo_precio = float(input("Nuevo precio: ")) if actualizar_precio else None
                nueva_cantidad = int(input("Nueva cantidad: ")) if actualizar_cantidad else None
                
                inventario.actualizar_producto(nombre, nueva_referencia, nuevo_precio, nueva_cantidad)
                
            elif opcion == 3: # Elimina un producto
                nombre = input("Nombre del producto a exterminar: ").strip()
                if not nombre:
                    raise ValueError("El producto tiene que tener nombre")

                while True:
                    try:
                        inventario.eliminar_producto(nombre)
                        break  # Sale del bucle si la operación fue exitosa
                    except ValueError as e:
                        print(f"Error: {str(e)}")
                        opcion = input("\n¿Desea intentar con otro nombre? (s/n): ").lower()
                        if opcion != 's':
                            print("Volver al menú principal")
                            break
                        nombre = input("Nombre del producto a exterminar: ").strip()
                        if not nombre:
                            raise ValueError("El producto tiene que tener nombre")
                
            elif opcion == 4:  # Muestra el inventario
                inventario.mostrar_inventario()
                
            elif opcion == 5:  # Busca un producto
                nombre = input("Producto a buscar: ")
                producto = inventario.buscar_producto(nombre)
                if producto:
                    print("\nLo encontré:")
                    print(producto)
                else:
                    print(f"No se encontró, lo siento '{nombre}'")
                
            elif opcion == 6: # Sale del programa
                print("Cerrando programa. Hasta pronto")
                break
                
            else:
                print("Opción no válida. Por favor, intente nuevamente.")
                
        except ValueError as e: # Manejo de errores de validación
            print(f"Error: {str(e)}")
        except Exception as e: # Manejo de errores inesperados
            print(f"Error inesperado: {str(e)}")

# Punto de entrada del programa
if __name__ == "__main__":
    main()
