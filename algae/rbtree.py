from __future__ import (absolute_import, division, with_statement)
from dpc.functions import identity
from functools import partial
from operator import lt

class RedBlackTree(object):
    """A binary search tree which guarantees that basic operations take place
in O(lg n) time.  The terminology and basic algorithmic structure is taken
from Cormen, Leiserson, Rivest, Stein, _Introduction to Algorithms_ (Second
Edition), pp. 273-301.

Each node of the tree has a color, which is either red or black.  The
red-black tree must satisfy the following properties:
1. Every node is either red or black.
2. The root node is black.
3. Every leaf node (None) is black.
4. If a node is red, then both of its children are black.
5. For each node, all paths from the node to descendant leaves contain the
   same number of black nodes.
"""
    def __init__(self, init=None, cmp=lt, key=identity):
        super(RedBlackTree, self).__init__()
        self.root = None
        self.compare_nodes = cmp
        self.get_node_key = key

        if init is not None:
            self.update(init)
        return

    @staticmethod
    def __is_red(node):
        return node is not None and node.red

    @staticmethod
    def __get_left(node):
        if node is None:
            return None
        return node.left

    @staticmethod
    def __get_right(node):
        if node is None:
            return None
        return node.right

    @staticmethod
    def __get_parent(node):
        if node is None:
            return None
        return node.parent

    @staticmethod
    def __get_grandparent(node):
        return RedBlackTree.__get_parent(RedBlackTree.__get_parent(node))

    @staticmethod
    def __get_uncle(node):
        parent = RedBlackTree.__get_parent(node)
        gp = RedBlackTree.__get_parent(parent)
        gp_left = RedBlackTree.__get_left(gp)
        if gp_left is parent:
            return RedBlackTree.__get_right(gp)
        else:
            return gp_left

    def __left_rotate(self, x):
        """Perform a left rotation on the specified node.  The right child of
the node must not be None.

    |                  |
    x                  y
   / \      --->      / \
  a   y              x   c
     / \            / \
    b   c          a   b
"""
        y = x.right
        x.right = y.left
        if y.left is not None:
            y.left.parent = x
        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x.parent.left is x:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y
        return

    def __right_rotate(self, x):
        """Perform a right rotation on the specified node.  The left child of
the node must not be None.

      |                |
      x                y
     / \    --->      / \
    y   c            a   x
   / \                  / \
  a   b                b   c
"""
        y = x.left
        x.left = y.right
        if y.right is not None:
            y.right.parent = x
        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x.parent.left is x:
            x.parent.left = y
        else:
            x.parent.right = y
        y.right = x
        x.parent = y
        return

    def find_node_floor(self, key):
        key = self.get_node_key(key)
        node = self.root
        last_smaller_node = None

        while node is not None:
            node_key = self.get_node_key(node.key)
            if self.compare_nodes(key, node_key):
                # key < node_key; move left.  Don't update last_smaller_node
                # since this node is bigger.
                node = node.left
            elif self.compare_nodes(node_key, key):
                # key > node_key; move right
                last_smaller_node = node
                node = node.right
            else:
                # Exact match; return this node.
                return node
        
        return last_smaller_node

    def find_node_ceil(self, key):
        key = self.get_node_key(key)
        node = self.root
        last_bigger_node = None

        while node is not None:
            node_key = self.get_node_key(node.key)
            if self.compare_nodes(key, node_key):
                # key < node_key; move left.
                last_bigger_node = node
                node = node.left
            elif self.compare_nodes(node_key, key):
                # key > node_key; move right.  Don't update last_bigger_node
                # since this node is smaller.
                node = node.right
            else:
                # Exact match; return this node.
                return node
        
        return last_bigger_node

    def find_node(self, key):
        node = self.root
        key = self.get_node_key(key)

        while node is not None:
            node_key = self.get_node_key(node.key)
            if self.compare_nodes(key, node_key):
                # key < node; move left.
                node = node.left
            elif self.compare_nodes(node_key, key):
                # key > node; move right
                node = node.right
            else:
                # Found it
                return node
        return None

    def __rb_insert(self, z):
        y = None
        x = self.root
        z_key = self.get_node_key(z.key)

        while x is not None:
            y = x
            if self.compare_nodes(z_key, self.get_node_key(y.key)):
                x = x.left
            else:
                x = x.right
        
        z.parent = y
        if y is None:
            self.root = z
        elif self.compare_nodes(z_key, self.get_node_key(y.key)):
            y.left = z
        else:
            y.right = z

        z.red = True
        self.__rb_insert_fixup(z)
        return

    def __rb_insert_fixup(self, z):
        while RedBlackTree.__is_red(z.parent):
            # Since the parent is red, it's guaranteed to be non-nil (nil
            # nodes are black).  Since the parent is red, grandparent is also
            # non-nil (since the root can't be red).
            parent = z.parent
            grandparent = parent.parent
            gp_left = grandparent.left
            gp_right = grandparent.right

            if parent is gp_left:
                uncle = gp_right
                if RedBlackTree.__is_red(uncle):
                    # Case 1: z, parent, and uncle are red.  Since the
                    # grandparent is black, we swap the colors of the
                    # parent/uncle and grandparent, and restart from the
                    # grandparent.
                    parent.red = uncle.red = False
                    grandparent.red = True
                    z = grandparent
                    continue
                else:
                    if z is parent.right:
                        # Case 2: parent is red, uncle is black, and z is
                        # its parent's right child.  Rotate the parent left
                        # (to put this node into the parent's spot) and fall
                        # through to case 3.
                        z, parent = parent, z
                        self.__left_rotate(z)
                    
                    # Case 3: parent is red, uncle is black, and node is its
                    # parent's left child.  Rotate the parent into the
                    # grandparent's spot, but preserve the colors of those
                    # spots: the old parent/new grandparent is black, and
                    # the old grandparent/new parent is red.
                    parent.red = False
                    grandparent.red = True
                    self.__right_rotate(grandparent)
                    break
            else:
                # This is just the mirror image of the above case; uncle is
                # now on the left.
                uncle = gp_left

                if RedBlackTree.__is_red(uncle):
                    # Case 1
                    parent.red = uncle.red = False
                    grandparent.red = True
                    z = grandparent
                    continue
                else:
                    if z is parent.left:
                        # Case 2.
                        z, parent = parent, z
                        self.__right_rotate(z)
                    
                    # Case 3
                    parent.red = False
                    grandparent.red = True
                    self.__left_rotate(grandparent)
                    break
        self.root.red = False
        return

    def __rb_delete(self, z):
        # y is the actual node we're going to remove.  If it's a live node,
        # we'll move its contents to z.
        if z.left is None or z.right is None:
            # There's an empty branch here, so we can remove y and replace it
            # with its child.
            y = z
        else:
            # Otherwise, remove the successor node, which will have an empty
            # left.
            y = z.successor

        # Either y.left or y.right is None.  x is the non-None child, if any,
        # which will replace y.
        if y.left is not None:
            x = y.left
        else:
            x = y.right

        # If x isn't a leaf node, we need to set its parent.
        if x is not None:
            x.parent = y.parent

        # Make y's parent point to x now.
        if y.parent is None:
            self.root = x
        elif y.parent.left is y:
            y.parent.left = x
        else:
            y.parent.right = x

        # Copy the key and value from y to z (if z is a live node)
        if y is not z:
            z.key = y.key
            z.value = y.value

        if not y.red and x is not None:
            self.__rb_delete_fixup(x)
        
        return y

    def __rb_delete_fixup(self, x):
        while x is not self.root and not x.red:
            # x is not the root, so x.parent is non-nil.
            if x is x.parent.left:
                # w is the uncle node.  Since x is black, w cannot be nil;
                # otherwise, x and w will have different black heights,
                # and they're both children of x.parent.
                w = x.parent.right

                if w.red:
                    # Case 1: w is red; thus, both of w's children are black.
                    # We perform a left rotation on x's parent to move w into
                    # that spot, converting this into case 2.
                    w.red = False
                    x.parent.red = True
                    self.__left_rotate(x.parent)
                    w = x.parent.right

                if not w.left.red and not w.right.red:
                    # Case 2:
                    w.red = True
                    x = x.parent
                else:
                    # Case 3:
                    if not w.right.red:
                        w.left.red = False
                        w.red = True
                        self.__right_rotate(w)
                        w = x.parent.right
                    
                    # Case 4:
                    w.red = x.parent.red
                    x.parent.red = False
                    w.right.red = False
                    self.__left_rotate(x.parent)
                    x = self.root
            else:
                # w is the uncle node.  Since x is black, w cannot be nil;
                # otherwise, x and w will have different black heights,
                # and they're both children of x.parent.
                w = x.parent.left

                if w.red:
                    # Case 1: w is red; thus, both of w's children are black.
                    # We perform a left rotation on x's parent to move w into
                    # that spot, converting this into case 2.
                    w.red = False
                    x.parent.red = True
                    self.__right_rotate(x.parent)
                    w = x.parent.left

                if not w.left.red and not w.right.red:
                    # Case 2:
                    w.red = True
                    x = x.parent
                else:
                    # Case 3:
                    if not w.left.red:
                        w.right.red = False
                        w.red = True
                        self.__left_rotate(w)
                        w = x.parent.left
                    
                    # Case 4:
                    w.red = x.parent.red
                    x.parent.red = False
                    w.right.red = False
                    self.__right_rotate(x.parent)
                    x = self.root
        x.red = False
        return

    def __getitem__(self, key):
        node = self.find_node(key)
        if node is None:
            raise KeyError("Unknown key: %r" % (key,))
        return node.value
    
    def __setitem__(self, key, value):
        node = self.find_node(key)
        if node is None:
            node = RedBlackTreeNode(key, value)
            self.__rb_insert(node)
        else:
            node.value = value
        return

    def __contains__(self, key):
        return self.find_node(key) is not None

    def __delitem__(self, key):
        node = self.find_node(key)
        if node is None:
            raise KeyError("Unknown key: %r" % (key,))
        self.__rb_delete(node)
    
    def iterkeys(self):
        return iter(self.keys())

    def itervalues(self):
        return iter(self.values())

    def iteritems(self):
        return iter(self.items())

    def keys(self):
        result = []
        def callback(result, node):
            result.append(node.key)

        if self.root is not None:
            self.root.depth_first_search(partial(callback, result))

        return result

    def values(self):
        result = []
        def callback(result, node):
            result.append(node.value)

        if self.root is not None:
            self.root.depth_first_search(partial(callback, result))

        return result

    def items(self):
        result = []
        def callback(result, node):
            result.append((node.key, node.value))
        
        if self.root is not None:
            self.root.depth_first_search(partial(callback, result))

        return result

class RedBlackTreeNode(object):
    def __init__(self, key, value):
        super(RedBlackTreeNode, self).__init__()
        self.red = True
        self.parent = None
        self.left = None
        self.right = None
        self.key = key
        self.value = value
        return

    def depth_first_search(self):
        if self.left is not None:
            self.left.dfs()
        yield self
        if self.right is not None:
            self.right.dfs()

        return

    def debug(self):
        if self.left is not None:
            left = self.left.debug().split("\n")
            left_size = max([len(l) for l in left])
        else:
            left = ["nil"]
            left_size = 3
        
        if self.right is not None:
            right = self.right.debug().split("\n")
            right_size = max([len(l) for l in right])
        else:
            right = ["nil"]
            right_size = 3

        column_size = max([left_size, right_size])

        top = str(self.key)
        if self.red:
            top += " [r]"
        else:
            top += " [b]"
        
        top_size = len(top)
        size = max([3 + left_size + right_size, top_size])

        result = top.center(size, "-")
        result += "\n" + " " * left_size + "/ \\" + " " * right_size

        for i in xrange(max([len(left), len(right)])):
            result += "\n"
            if i < len(left):
                result += left[i].rjust(left_size)
            else:
                result += " " * left_size
            
            result += "   "
            if i < len(right):
                result += right[i].ljust(right_size)
            else:
                result += " " * right_size
            
        return result

    @property
    def black_height(self):
        if self.left is None:
            left_height = 1
        else:
            left_height = self.left.black_height
            if not self.left.red:
                left_height += 1

        if self.right is None:
            right_height = 1
        else:
            right_height = self.right.black_height
            if not self.right.red:
                right_height += 1

        if left_height != right_height:
            raise ValueError("left and right black heights are unequal: "
                             "%d vs %d" % (left_height, right_height))

        return left_height

    def check(self):
        left = self.left
        right = self.right

        if left is not None:
            assert left.parent is self, (
                "parent inconsistency on %d" % id(left))
            left.check()
        if right is not None:
            assert right.parent is self, (
                "parent inconsistency on %d" % id(right))
            right.check()

        self.black_height

        if self.red:
            assert ((left is None or not left.red) and
                    (right is None or not right.red)), (
                "red node %d does not have two child black nodes" % id(self))
            assert self.parent is not None, (
                "red node %d does not have a parent" % id(self))

        return

    @property
    def successor(self):
        succ = self.right
        
        if succ is None:
            return None

        while succ.left is not None:
            succ = succ.left

        return succ

    @property
    def predecessor(self):
        pred = self.left

        if pred is None:
            return None

        while pred.right is not None:
            pred = pred.right
        
        return pred