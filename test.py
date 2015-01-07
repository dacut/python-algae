import os, sys
import unittest

sys.path = [os.getcwd()] + sys.path

from algae.collections import RedBlackTree

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

    def test_min_max_del(self):
        x = RedBlackTree()
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

    def test_debug(self):
        x = RedBlackTree()
        x[1] = 1
        self.assertEqual(x.root.debug(), 
                         "\n".join([r"--1 [b]--",
                                    r"   / \   ",
                                    r"nil   nil",]))

    def test_initialization(self):
        x = RedBlackTree({1: 2, 5: 6})
        self.assertEqual(x[1], 2)
        self.assertEqual(x[5], 6)

        x = RedBlackTree(((1, 2), (5, 6)))
        self.assertEqual(x[1], 2)
        self.assertEqual(x[5], 6)

if __name__ == "__main__":
    unittest.main()
