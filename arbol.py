import os  # Importar módulo para trabajar con funcionalidades del sistema operativo
import pickle  # Importar módulo para serialización de objetos
import graphviz  # Importar módulo para visualización de gráficos
from IPython.display import display  # Importar función para mostrar gráficos en el notebook
from os import listdir  # Importar función para listar archivos en un directorio
from os.path import isfile, join  # Importar funciones para verificar si un camino es un archivo y unir rutas de archivos

# Definición de la clase AVLNode para representar un nodo en el Árbol AVL
class AVLNode:
    # Constructor para inicializar un nodo AVL con una clave, tipo y tamaño
    def __init__(self, key, type, size):
        self.key = key  # Clave del nodo
        self.height = 1  # Altura del nodo
        self.type = type  # Tipo de imagen asociada al nodo
        self.size = size  # Tamaño de la imagen asociada al nodo
        self.left = None  # Referencia al hijo izquierdo
        self.right = None  # Referencia al hijo derecho

# Definición de la clase AVLTree para representar un Árbol AVL
class AVLTree:
    # Constructor para inicializar el Árbol AVL con la raíz vacía
    def __init__(self):
        self.root = None  # Raíz del árbol AVL

    # Función para obtener la altura de un nodo
    def height(self, node):
        if not node:
            return 0
        return node.height

    # Función para obtener el factor de equilibrio de un nodo
    def balance(self, node):
        if not node:
            return 0
        return self.height(node.left) - self.height(node.right)

    # Función para realizar una rotación a la derecha
    def rotate_right(self, y):
        x = y.left
        T2 = x.right

        x.right = y
        y.left = T2

        y.height = 1 + max(self.height(y.left), self.height(y.right))
        x.height = 1 + max(self.height(x.left), self.height(x.right))

        return x

    # Función para realizar una rotación a la izquierda
    def rotate_left(self, x):
        y = x.right
        T2 = y.left

        y.left = x
        x.right = T2

        x.height = 1 + max(self.height(x.left), self.height(x.right))
        y.height = 1 + max(self.height(y.left), self.height(y.right))

        return y

    # Función para insertar un nodo en el árbol AVL
    def insert(self, node, key, type, size):
        if not node:
            return AVLNode(key, type, size)

        if key < node.key:
            node.left = self.insert(node.left, key, type, size)
        else:
            node.right = self.insert(node.right, key, type, size)

        node.height = 1 + max(self.height(node.left), self.height(node.right))

        balance = self.balance(node)

        if balance > 1 and key < node.left.key:
            return self.rotate_right(node)

        if balance < -1 and key > node.right.key:
            return self.rotate_left(node)

        if balance > 1 and key > node.left.key:
            node.left = self.rotate_left(node.left)
            return self.rotate_right(node)

        if balance < -1 and key < node.right.key:
            node.right = self.rotate_right(node.right)
            return self.rotate_left(node)

        return node

    # Función para insertar un nodo en el árbol AVL
    def insert_node(self, key, type, size):
        self.root = self.insert(self.root, key, type, size)

    # Función para eliminar un nodo del árbol AVL
    def delete_node(self, key):
        self.root = self._delete_node(self.root, key)

    # Función auxiliar para eliminar un nodo del árbol AVL
    def _delete_node(self, root, key):
        if not root:
            return root

        if key < root.key:
            root.left = self._delete_node(root.left, key)
        elif key > root.key:
            root.right = self._delete_node(root.right, key)
        else:
            if root.left is None:
                temp = root.right
                root = None
                return temp
            elif root.right is None:
                temp = root.left
                root = None
                return temp

            temp = self._get_min_value_node(root.right)
            root.key = temp.key
            root.right = self._delete_node(root.right, temp.key)

        if root is None:
            return root

        root.height = 1 + max(self.height(root.left), self.height(root.right))
        balance = self.balance(root)

        if balance > 1 and self.balance(root.left) >= 0:
            return self.rotate_right(root)

        if balance < -1 and self.balance(root.right) <= 0:
            return self.rotate_left(root)

        if balance > 1 and self.balance(root.left) < 0:
            root.left = self.rotate_left(root.left)
            return self.rotate_right(root)

        if balance < -1 and self.balance(root.right) > 0:
            root.right = self.rotate_right(root.right)
            return self.rotate_left(root)

        return root

    # Función para obtener el nodo con el valor mínimo
    def _get_min_value_node(self, node):
        current = node
        while current.left:
            current = current.left
        return current

    # Función para visualizar el árbol AVL
    def visualize(self):
        dot = graphviz.Digraph(comment='AVL Tree')
        self._visualize(self.root, dot)
        return dot

    # Función auxiliar para visualizar el árbol AVL
    def _visualize(self, node, graph):
        if node:
            graph.node(str(node.key), str(node.key))
            if node.left:
                graph.edge(str(node.key), str(node.left.key))
                self._visualize(node.left, graph)
            if node.right:
                graph.edge(str(node.key), str(node.right.key))
                self._visualize(node.right, graph)

    # Función para guardar el árbol AVL en un archivo
    def save_tree(self, filename):
        with open(filename, 'wb') as file:
            pickle.dump(self.root, file)

    # Función para cargar el árbol AVL desde un archivo
    def load_tree(self, filename):
        if os.path.exists(filename):
            with open(filename, 'rb') as file:
                self.root = pickle.load(file)
                print("Árbol AVL cargado exitosamente.")
        else:
            print("No se encontró ningún archivo de árbol AVL. Se creará uno nuevo.")

    # Método para buscar un nodo en el árbol AVL.
    def searchNode(self, node, key):
    # Verifica si el nodo es nulo, en cuyo caso indica que la imagen no fue encontrada.
      if not node:
        print("Imagen no encontrada.")
        return None
    # Comprueba si el valor de búsqueda coincide con la clave del nodo actual.
      elif key == node.key:
        # Imprime la información de la imagen encontrada y la devuelve.
        print("Imagen encontrada exitosamente.\nCategoría: " + node.type + "\nTamaño: " + node.size + " bytes")
        return node
    # Si el valor de búsqueda es menor que la clave del nodo actual, se busca en el subárbol izquierdo.
      elif key < node.key:
        return self.searchNode(node.left, key)
    # Si el valor de búsqueda es mayor que la clave del nodo actual, se busca en el subárbol derecho.
      else:
        return self.searchNode(node.right, key)

# Método para filtrar nodos en el árbol AVL según un rango de tamaño.
    def filterNodes(self, node, min_size, max_size, result_tree):
    # Si el nodo es nulo, se detiene la búsqueda.
     if not node:
        return
    # Si el tamaño del nodo está dentro del rango especificado, se inserta en el árbol de resultados.
     if min_size <= int(node.size) < max_size:
        result_tree.insert_node(node.key, node.type, node.size)
    # Se continúa filtrando en el subárbol izquierdo y derecho.
     self.filterNodes(node.left, min_size, max_size, result_tree)
     self.filterNodes(node.right, min_size, max_size, result_tree)

# Método para realizar un recorrido del árbol AVL por niveles.
    def levelOrderTraversal(self):
    # Si el árbol no está vacío, se inicia el recorrido desde la raíz.
     if self.root:
        print("Recorrido del árbol AVL por niveles (recursivo):")
        self._levelOrderTraversal_([self.root], counter=0)
     else:
        print("El árbol AVL está vacío.")

# Método auxiliar para realizar el recorrido del árbol AVL por niveles.
    def _levelOrderTraversal_(self, nodes, counter):
    # Imprime el nivel actual y sus nodos.
     print("Nivel " + str(counter) + ":")
     counter = counter + 1
     next_level = []
     for node in nodes:
        print(node.key, end=" ")
        if node.left:
            next_level.append(node.left)
        if node.right:
            next_level.append(node.right)
     print()
     # Si hay nodos en el siguiente nivel, se continúa el recorrido.
     if next_level:
        self._levelOrderTraversal_(next_level, counter)

# Método para obtener el nivel de un nodo en el árbol AVL.
    def nodeLevel(self, key):
    # Inicia la búsqueda del nivel desde la raíz del árbol.
     return self._nodeLevel_(self.root, key, 1)

# Método auxiliar para obtener el nivel de un nodo en el árbol AVL.
    def _nodeLevel_(self, node, key, level):
    # Si el nodo es nulo, indica que no se encontró el nivel.
     if node is None:
        return -1
    # Si la clave del nodo coincide con el valor buscado, devuelve el nivel actual.
     if node.key == key:
        return level
    # Busca el nivel en el subárbol izquierdo y luego en el subárbol derecho.
     down_level = self._nodeLevel_(node.left, key, level + 1)
     if down_level != -1:
        return down_level
     down_level = self._nodeLevel_(node.right, key, level + 1)

     return down_level

    def balanceFactor(self, key):
    # Calcula el factor de balanceo (equilibrio) de un nodo en el árbol AVL.
     node = self.searchNode(self.root, key)
     if node:
        return self.balance(node)
     else:
        return print("La imagen no se encuentra insertada")


    def find_parent(self, key):
    # Encuentra el padre de un nodo específico en el árbol AVL.
     return self._find_parent(self.root, key)


    def _find_parent(self, node, key):
    # Método interno para encontrar el padre de un nodo en el árbol AVL.
     if not node or node.key == key:
        return None

     if (node.left and node.left.key == key) or (node.right and node.right.key == key):
        return node

     if key < node.key:
        return self._find_parent(node.left, key)
     else:
        return self._find_parent(node.right, key)


    def find_grandparent(self, key):
    # Encuentra el abuelo de un nodo específico en el árbol AVL.
     parent = self.find_parent(key)
     if parent:
        return self.find_parent(parent.key)
     else:
        return None


    def find_uncle(self, key):
    # Encuentra el tío de un nodo específico en el árbol AVL.
     grandparent = self.find_grandparent(key)
     parent = self.find_parent(key)
     if grandparent and parent:
        if grandparent.left == parent:
            return grandparent.right
        else:
            return grandparent.left
     else:
        return None

def setPath():
    # Configura las rutas para cada tipo de imagen en el dataset.
    path = input("Ingrese la ruta del dataset: ")
    bikePath = path+'\\bike'
    carPath = path+'\\cars'
    catPath = path+'\\cats'
    dogPath = path+'\\dogs'
    flowerPath = path+'\\flowers'
    horsePath = path+'\\horses'
    humanPath = path+'\\human'
    bikesList = [a for a in listdir(bikePath) if isfile(join(bikePath, a))]
    carsList = [a for a in listdir(carPath) if isfile(join(carPath, a))]
    catsList = [a for a in listdir(catPath) if isfile(join(catPath, a))]
    dogsList = [a for a in listdir(dogPath) if isfile(join(dogPath, a))]
    flowersList = [a for a in listdir(flowerPath) if isfile(join(flowerPath, a))]
    horsesList = [a for a in listdir(horsePath) if isfile(join(horsePath, a))]
    humansList = [a for a in listdir(humanPath) if isfile(join(humanPath, a))]
    return bikePath, carPath, catPath, dogPath, flowerPath, horsePath, humanPath, bikesList, carsList, catsList, dogsList, flowersList, horsesList, humansList


def setType(key, bikePath, carPath, catPath, dogPath, flowerPath, horsePath, humanPath, bikesList, carsList, catsList, dogsList, flowersList, horsesList, humansList):
    # Asigna un tipo y una ruta a una imagen basándose en su nombre y la estructura de carpetas.
    if key in bikesList:
        type = "Bike"
        path = bikePath+'/'+key
    elif key in carsList:
        type = "Car"
        path = carPath+'/'+key
    elif key in catsList:
        type = "Cat"
        path = catPath+'/'+key
    elif key in dogsList:
        type = "Dog"
        path = dogPath+'/'+key
    elif key in flowersList:
        type = "Flower"
        path = flowerPath+'/'+key
    elif key in horsesList:
        type = "Horse"
        path = horsePath+'/'+key
    elif key in humansList:
        type = "Human"
        path = humanPath+'/'+key
    return type, path


def menu():
    # Muestra el menú de opciones para interactuar con el árbol AVL.
    print("1. Insertar imagen")
    print("2. Eliminar imagen")
    print("3. Buscar imagen")
    print("4. Mostrar imágenes")
    print("5. Filtrar imágenes")
    print("6. Recorrer imágenes por niveles")
    print("7. Operaciones con nodos")
    print("8. Salir")


avl_tree = AVLTree()
if os.path.exists('avl_tree.pkl'):
    os.remove('avl_tree.pkl')
else:
    print("No se encontró ningún archivo de árbol AVL. Se creará uno nuevo.")
while (True):
    try:
        bikePath, carPath, catPath, dogPath, flowerPath, horsePath, humanPath, bikesList, carsList, catsList, dogsList, flowersList, horsesList, humansList = setPath()
        break
    except:
        print("Ruta inválida.")

while True:
    # Muestra el menú de opciones y espera la selección del usuario.
    menu()
    opcion = input("Seleccione una opción: ")
    if opcion == "1":
        while True:
            try:
                # Solicita al usuario el nombre de la imagen a agregar.
                key = input("Ingrese el nombre de la imagen que desea agregar: ")
                # Asigna el tipo y la ruta de la imagen.
                type, path = setType(key, bikePath, carPath, catPath, dogPath, flowerPath, horsePath, humanPath, bikesList, carsList, catsList, dogsList, flowersList, horsesList, humansList)
                break
            except:
                print("Nombre inválido")
        # Obtiene el tamaño de la imagen.
        size = str(os.path.getsize(path))
        # Inserta el nodo en el árbol AVL y guarda el árbol en un archivo.
        avl_tree.insert_node(key, type, size)
        avl_tree.save_tree('avl_tree.pkl')
        print("Nodo insertado exitosamente.")
    elif opcion == "2":
        # Solicita al usuario el nombre de la imagen a eliminar y la elimina del árbol.
        key = input("Ingrese el nombre de la imagen que desea eliminar: ")
        avl_tree.delete_node(key)
        avl_tree.save_tree('avl_tree.pkl')
    elif opcion == "3":
        # Solicita al usuario el nombre de la imagen a buscar y muestra información si se encuentra.
        key = input("Ingrese el nombre de la imagen que desea buscar: ")
        avl_tree.searchNode(avl_tree.root, key)
        display(avl_tree.visualize())
    elif opcion == "4":
        # Carga el árbol desde el archivo.
        avl_tree.load_tree('avl_tree.pkl')
        # Visualiza el árbol y guarda la imagen como un archivo PNG.
        dot = avl_tree.visualize() 
        dot.render("avl_tree", format="png", cleanup=True)
        print("Árbol AVL visualizado y guardado como avl_tree.png.")    
    elif opcion == "5":
        # Filtra las imágenes por tipo y tamaño y muestra el resultado.
        type_input = input("Ingrese el tipo de imagen (bike, car, cat, dog, flower, horse, human): ").lower()
        min_size = int(input("Ingrese el tamaño mínimo en bytes: "))
        max_size = int(input("Ingrese el tamaño máximo en bytes: "))
        result_tree = AVLTree()
        avl_tree.filterNodes(avl_tree.root, min_size, max_size, result_tree)
        display(result_tree.visualize())
    elif opcion == "6":
        # Realiza un recorrido del árbol por niveles y lo muestra.
        avl_tree.levelOrderTraversal()
    elif opcion == "7":
        # Realiza operaciones específicas con los nodos del árbol.
        subopcion = input("Seleccione una operación para realizar con los nodos:\na. Obtener el nivel del nodo.\nb. Obtener el factor de balanceo (equilibrio) del nodo.\nc. Encontrar el padre del nodo.\nd. Encontrar el abuelo del nodo.\ne. Encontrar el tío del nodo.\nIngrese la letra correspondiente a la operación: ")
        key = input("Ingrese el nombre del nodo: ")
        if subopcion == "a":
            # Obtiene el nivel del nodo y lo muestra.
            level = avl_tree.nodeLevel(key)
            if level:
                print(f"El nivel del nodo {key} es: {int(level)-1}")
            else:
                print(f"No se encontró el nodo {key}")
        elif subopcion == "b":
            # Obtiene el factor de balanceo del nodo y lo muestra.
            balance_factor = avl_tree.balanceFactor(key)
            if balance_factor is not None:
                print(f"El factor de balanceo del nodo {key} es: {balance_factor}")
            else:
                print(f"No se encontró el nodo {key}.")
        elif subopcion == "c":
            # Encuentra el padre del nodo y lo muestra.
            parent = avl_tree.find_parent(key)
            if parent:
                print(f"El padre del nodo {key} es: {parent.key}")
            else:
                print(f"No se encontró el nodo {key}.")
        elif subopcion == "d":
            # Encuentra el abuelo del nodo y lo muestra.
            grandparent = avl_tree.find_grandparent(key)
            if grandparent:
                print(f"El abuelo del nodo {key} es: {grandparent.key}")
            else:
                print(f"No se encontró el nodo {key}.")
        elif subopcion == "e":
            # Encuentra el tío del nodo y lo muestra.
            uncle = avl_tree.find_uncle(key)
            if uncle:
                print(f"El tío del nodo {key} es: {uncle.key}")
            else:
                print(f"No se encontró el nodo {key}.")
        else:
            print("Opción inválida.")

    elif opcion == "8":
        # Guarda el árbol en un archivo y finaliza el programa.
        avl_tree.save_tree('avl_tree.pkl')
        print("Árbol AVL guardado exitosamente.")
        print("Saliendo del programa...")
        break
    else:
        print("Opción inválida. Por favor, seleccione una opción válida.")
