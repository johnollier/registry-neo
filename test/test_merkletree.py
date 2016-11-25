import unittest
from registry.merkletree import *

class MockRedis:
    def __init__(self, store):
        self.store = store

    def exists(self, key):
        return key in self.store

    def incr(self, key):
        self.store[key] = self.store[key] + 1
        return self.store[key]

    def get(self, key):
        return self.store[key]
    
    def set(self, key, val):
        self.store[key] = val


class MerkleTreeTestCase(unittest.TestCase):
    def test_eq(self):
        n1 = Point(1, 2)
        n2 = Point(2, 1)
        n3 = Point(2, 1)
        self.assertFalse(n1 == n2)
        self.assertTrue(n2 == n3)

    def test_even(self):
        n1 = Point(1, 2)
        n2 = Point(2, 3)
        n3 = Point(0, 1)
        self.assertFalse(n1.even())
        self.assertTrue(n2.even())
        self.assertTrue(n3.even())

    def test_siblings(self):
        path = [Point(2, 0), Point(1, 1), Point(0, 2)]
        expected = [Point(3, 0), Point(0, 1), Point(1, 2)]
        siblings = [ p.sibling() for p in path]
        self.assertEqual(3, len(siblings))
        for i in range(3):
            self.assertEqual(expected[i], siblings[i])
            self.assertEqual(expected[i], siblings[i])

    def test_path_to_root0(self):
        store = {"max-y":0}
        tree = MerkleTree( MockRedis(store) )
        points = tree.path_to_root(Point(0, 0))
        self.assertEqual(1, len(points))
        self.assertEqual(Point(0,0), points[0])

    def test_path_to_root1(self):
        store = {"max-y":1}
        tree = MerkleTree( MockRedis( store ))
        points = tree.path_to_root(Point(1, 0))
        self.assertEqual(2, len(points))
        self.assertEqual(Point(1,0), points[0])
        self.assertEqual(Point(0,1), points[1])

    def test_path_to_root2(self):
        store = {"max-y":2}
        tree = MerkleTree( MockRedis( store ))
        points = tree.path_to_root(Point(2, 0))
        self.assertEqual(3, len(points))
        self.assertEqual(Point(2,0), points[0])
        self.assertEqual(Point(1,1), points[1])
        self.assertEqual(Point(0,2), points[2])

    def test_path_to_root3(self):
        store = {"max-y":2}
        tree = MerkleTree( MockRedis( store ))
        points = tree.path_to_root(Point(0, 0))
        self.assertEqual(3, len(points))
        self.assertEqual(Point(0,0), points[0])
        self.assertEqual(Point(0,1), points[1])
        self.assertEqual(Point(0,2), points[2])

    def combine_hash_simple(hash_left, hash_right):
        """ simple combine hash function to make combining easier to see"""
        if not hash_left:
            raise RuntimeError("left hash must be present")
        elif hash_right:
            return hash_left + hash_right
        else:
            return hash_left

    def test_should_not_increase_max_y(self):
        store = {"max-y":3}
        tree = MerkleTree( MockRedis( store ))
        tree.update_max_y( 5 )
        self.assertEqual(3, tree.max_y)

    def test_should_not_increase_max_y_upper_limit(self):
        store = {"max-y":3}
        tree = MerkleTree( MockRedis( store ))
        tree.update_max_y( 7 )
        self.assertEqual(3, tree.max_y)

    def test_should_increase_max_y(self):
        store = {"max-y":3}
        tree = MerkleTree( MockRedis( store ))
        tree.update_max_y( 8 )
        self.assertEqual(4, tree.max_y)

    def test_should_increase_max_y_after_first(self):
        store = {"max-y":0}
        tree = MerkleTree( MockRedis( store ))
        tree.update_max_y( 0 )
        self.assertEqual(1, tree.max_y)
    
    def test_should_set_max_y_if_store_empty(self):
        store = {}
        tree = MerkleTree( MockRedis( store ))
        self.assertEqual(0, tree.max_y)

    def test_update_hashes(self):
        store = {"max-y":2}
        tree = MerkleTree( MockRedis( store ))
        points = (Point(3, 0), Point(1, 1), Point(0, 2))
        entry_hash = 'd'
        sibling_nodes = [Node(Point(2,0),'c'), Node(Point(0,1),'ab'), Node(Point(1,2),'')]
        expected = [Node(Point(3, 0), 'd'), Node(Point(1, 1), 'cd'), Node(Point(0, 2), 'abcd')]
        updated_nodes = tree.update_nodes(entry_hash, points, sibling_nodes)
        self.assertEqual(3, len(updated_nodes))
        for i in range(3):
            self.assertListEqual(expected, updated_nodes)


if __name__ == '__main__':
    unittest.main()
