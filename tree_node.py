class TreeNode:
    """
    A class to represent a tree node for storing genres and their anime.
    """
    def __init__(self, name, data=None):
        """
        Initialize a tree node.

        Args:
            name (str): The name of the node (e.g., genre name or anime title).
            data (dict): Additional data associated with the node (e.g., anime details).
        """
        self.name = name
        self.data = data  # Store additional data (e.g., episodes, link)
        self.children = []  # List of child nodes

    def add_child(self, child_node):
        """
        Add a child node to this node.

        Args:
            child_node (TreeNode): The child node to add.
        """
        self.children.append(child_node)

    def __repr__(self, level=0):
        """
        String representation of the tree for debugging and visualization.
        """
        ret = "\t" * level + f"{self.name}\n"
        for child in self.children:
            ret += child.__repr__(level + 1)
        return ret

    def remove_child(self, child_node):
        """
        Remove a child node from this node.

        Args:
            child_node (TreeNode): The child node to remove.
        """
        self.children = [child for child in self.children if child != child_node]
    
    def traverse(self):
        """
        Traverse the tree starting from this node and print each node's name.
        """
        print(self.name)
        for child in self.children:
            child.traverse()
    
    def is_in(self, name):
        """
        Check if a node with the given name exists in the subtree rooted at this node.

        Args:
            name (str): The name to search for.

        Returns:
            bool: True if a node with the given name exists, False otherwise.
        """
        if self.name == name:
            return True
        for child in self.children:
            if child.is_in(name):
                return True
        return False
    
    def get_child_node(self, name):
        """
        Get a child node with the given name.

        Args:
            name (str): The name of the child node to find.

        Returns:
            TreeNode: The child node with the given name, or None if not found.
        """
        for child in self.children:
            if child.name == name:
                return child
        return None
