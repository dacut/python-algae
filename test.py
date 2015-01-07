from math import e, pi
import os, sys
import unittest

sys.path = [os.getcwd()] + sys.path

from algae.collections import RedBlackTree
from algae.rbtree import RedBlackTreeNode

class TestRedBlackTree(unittest.TestCase):
    def test_ascending_insert(self):
        x = RedBlackTree()
        keys = []
        values = []
        items = []
        
        root_keys = ([1] * 2 + [2] * 5 + [4] * 10 + [8] * 20 + [16] * 40 +
                     [32] * 80 + [64] * 160)

        for key, root_key in zip(xrange(1, 318), root_keys):
            value = -key
            x[key] = value
            keys.append(key)
            values.append(value)
            items.append((key, value))

            self.assertEqual(x.keys(), keys)
            self.assertEqual(x.values(), values)
            self.assertEqual(x.items(), items)
            self.assertEqual(x.root.key, root_key)

    def test_descending_insert(self):
        x = RedBlackTree()
        keys = []
        values = []
        items = []
        
        root_keys = ([317] * 2 + [316] * 5 + [314] * 10 + [310] * 20 +
                     [302] * 40 + [286] * 80 + [254] * 160)

        for key, root_key in zip(xrange(317, 0, -1), root_keys):
            value = -key
            x[key] = value
            keys = [key] + keys
            values = [value] + values
            items = [(key, value)] + items

            self.assertEqual(x.keys(), keys)
            self.assertEqual(x.values(), values)
            self.assertEqual(x.items(), items)
            self.assertEqual(x.root.key, root_key)

    def test_even_insert(self):
        x = RedBlackTree()
        keys = [0]
        values = [0]
        items = [(0, 0)]

        x[0] = 0
        for key in xrange(1, 200):
            x[key] = key
            x[-key] = -key
            
            keys = [-key] + keys + [key]
            values = [-key] + values + [key]
            items = [(-key, -key)] + items + [(key, key)]

            self.assertEqual(x.keys(), keys)
            self.assertEqual(x.values(), values)
            self.assertEqual(x.items(), items)
            self.assertEqual(x.root.key, 0)
            
        # Replace some of the keys.
        for key in xrange(1, 200):
            x[key] = key + 1
            self.assertEqual(x[key], key + 1)

            self.assertTrue(key in x)
            self.assertFalse(key + 1000 in x)

    def test_mixed_insert_delete(self):
        # This is list of the numbers 0-255 randomized but in a reproducible
        # fashion.
        numbers = range(256)
        numbers.sort(key=lambda x: (
            str(pi ** x).replace(".", "")[x % 5:x % 5 + 4]))
        x = RedBlackTree()
        for i in numbers:
            x[i] = i

        for i in xrange(256):
            self.assertEqual(x[i], i)

        # Delete in a different random order
        numbers.sort(key=lambda x: (
            str(e ** x).replace(".", "")[x % 5:x % 5 + 4]))
        for i in numbers:
            self.assertTrue(i in x)
            del x[i]
            self.assertFalse(i in x)

        return

    def test_min_max_del(self):
        x = RedBlackTree()

        self.assertIsNone(x.min())
        self.assertIsNone(x.max())

        for value in xrange(0, 32, 2):
            x[value] = value

        try:
            ignored = x[1]
            self.fail("Expected KeyError")
        except KeyError:
            pass

        self.assertEqual(x.min(), (0, 0))
        self.assertEqual(x.max(), (30, 30))
        self.assertEqual(x.min(15), (14, 14))
        self.assertEqual(x.max(15), (16, 16))
        self.assertEqual(x.min(16), (16, 16))
        self.assertEqual(x.max(16), (16, 16))
        self.assertIsNone(x.min(-20))
        self.assertIsNone(x.max(40))

        del x[18]
        self.assertEqual(x.min(17), (16, 16))
        self.assertEqual(x.max(17), (20, 20))

        self.assertEqual(x.root.key, 6)
        del x[6]
        self.assertEqual(x.min(6), (4, 4))
        self.assertEqual(x.max(6), (8, 8))
        return

    def test_unbalanced_del(self):
        x = RedBlackTree()
        for value in xrange(16):
            x[value] = value
            x.root.check()
            
        del x[0]
        x.root.check()

        del x[2]
        x.root.check()
        
        del x[1]
        x.root.check()

        # Need this to create a non-empty left branch on node 8 to test
        # the branch "y.left is not None" in __rb_delete.
        x[7.5] = 7.5
        del x[8]
        del x[7.5]
        
        # Remove the rest of the nodes
        for val in [7, 6, 5, 4, 3, 12, 10, 9, 13, 11, 15, 14]:
            del x[val]
            if x.root is not None:
                x.root.check()

        # Make sure removing a node that doesn't exist fails.
        try:
            del x[0]
            self.fail("Expected KeyError")
        except KeyError:
            pass

        return

    def test_debug(self):
        x = RedBlackTree()
        x[1] = 1
        self.assertEqual(x.root.debug(), 
                         "\n".join([r"--1 [b]--",
                                    r"   / \   ",
                                    r"nil   nil",]))

        x[0] = 0
        self.assertEqual(x.root.debug(),
                         "\n".join([r"-----1 [b]-----",
                                    r"         / \   ",
                                    r"--0 [r]--   nil",
                                    r"   / \         ",
                                    r"nil   nil      "]))

        x[2] = 2
        self.assertEqual(x.root.debug(),
                         "\n".join([r"--------1 [b]--------",
                                    r"         / \         ",
                                    r"--0 [r]--   --2 [r]--",
                                    r"   / \         / \   ",
                                    r"nil   nil   nil   nil"]))

        del x[0]
        self.assertEqual(x.root.debug(),
                         "\n".join([r"-----1 [b]-----",
                                    r"   / \         ",
                                    r"nil   --2 [r]--",
                                    r"         / \   ",
                                    r"      nil   nil"]))
        

    def test_initialization(self):
        x = RedBlackTree({1: 2, 5: 6})
        self.assertEqual(x[1], 2)
        self.assertEqual(x[5], 6)

        x = RedBlackTree(((1, 2), (5, 6)))
        self.assertEqual(x[1], 2)
        self.assertEqual(x[5], 6)

    def test_update_items(self):
        class Dictish(object):
            def items(self):
                for x in ((0, 0), (1, 1), (2, 2)):
                    yield x
        
        d = Dictish()
        x = RedBlackTree()
        x.update(d)
        self.assertTrue(0 in x)
        self.assertEqual(x[0], 0)
        self.assertTrue(1 in x)
        self.assertEqual(x[1], 1)
        self.assertTrue(2 in x)
        self.assertEqual(x[2], 2)

        self.assertEqual(repr(x), "{0: 0, 1: 1, 2: 2}")

    def test_black_height(self):
        root = RedBlackTreeNode(5, 5)
        left = RedBlackTreeNode(0, 0)
        right = RedBlackTreeNode(10, 10)
        root.red = left.red = right.red = False
        root.left = left
        root.right = right
        left.parent = right.parent = root

        self.assertEqual(root.black_height, 2)
        left.red = right.red = True
        self.assertEqual(root.black_height, 1)
        right.red = False
        try:
            root.black_height
            self.fail("Expected AssertionError")
        except AssertionError:
            pass

        self.assertEquals(repr(root),
                          "RedBlackTreeNode(key=5, value=5, red=False)")
        return

    def test_adjacents(self):
        root = RedBlackTreeNode(5, 5)
        self.assertIsNone(root.predecessor)
        self.assertIsNone(root.successor)
        
        root.left = RedBlackTreeNode(2, 2)
        root.right = RedBlackTreeNode(8, 8)
        self.assertIs(root.predecessor, root.left)
        self.assertIs(root.successor, root.right)
        
        root.left.right = RedBlackTreeNode(3, 3)
        root.right.left = RedBlackTreeNode(7, 7)
        self.assertIs(root.predecessor, root.left.right)
        self.assertIs(root.successor, root.right.left)

        root.left.right.right = RedBlackTreeNode(4, 4)
        root.right.left.left = RedBlackTreeNode(6, 6)
        self.assertIs(root.predecessor, root.left.right.right)
        self.assertIs(root.successor, root.right.left.left)
        return

if __name__ == "__main__":
    unittest.main()
