# Clase TrieNode (nodo del Trie)
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False


# Clase Trie (estructura completa del Trie)
class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insertar_palabra(self, palabra):
        """
        Inserta una palabra en el Trie.
        """
        node = self.root
        for (
            char
        ) in (
            palabra.lower()
        ):  # Convertimos la palabra a minúsculas para búsqueda insensible a mayúsculas
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True

    def buscar_palabra(self, palabra):
        """
        Busca una palabra en el Trie. Devuelve True si la palabra completa está en el Trie.
        """
        node = self.root
        for (
            char
        ) in (
            palabra.lower()
        ):  # Convertimos la palabra a minúsculas para búsqueda insensible a mayúsculas
            if char not in node.children:
                return False
            node = node.children[char]
        return node.is_end_of_word
