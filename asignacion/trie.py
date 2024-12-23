"""
Archivo: trie.py
Descripción: Implementación de la estructura Trie para almacenar y buscar palabras clave de manera eficiente.
Autor: Estíbalitz Díez
Fecha: 23/12/2024
Versión: 2
"""

class TrieNode:
    """
    Clase que representa un nodo del Trie.
    """
    def __init__(self):
        self.children = {}  # Diccionario para almacenar los nodos hijos
        self.is_end_of_word = False  # Indica si el nodo marca el final de una palabra


class Trie:
    """
    Clase que representa la estructura completa del Trie.
    """
    def __init__(self):
        self.root = TrieNode()  # Nodo raíz del Trie

    def insertar_palabra(self, palabra):
        """
        Inserta una palabra en el Trie.

        Args:
            palabra (str): Palabra a insertar en el Trie.
        """
        node = self.root
        for char in palabra.lower():  # Convertir la palabra a minúsculas para búsqueda insensible a mayúsculas
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True

    def buscar_palabra(self, palabra):
        """
        Busca una palabra en el Trie.

        Args:
            palabra (str): Palabra a buscar en el Trie.

        Returns:
            bool: True si la palabra completa está en el Trie, False en caso contrario.
        """
        node = self.root
        for char in palabra.lower():  # Convertir la palabra a minúsculas para búsqueda insensible a mayúsculas
            if char not in node.children:
                return False
            node = node.children[char]
        return node.is_end_of_word
