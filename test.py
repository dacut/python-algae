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
