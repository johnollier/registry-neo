import sys
import time
import hashlib
import redis
import pdb

def sha_hash(s):
    return hashlib.sha256(s.encode("utf-8")).hexdigest()

def combine_hash_prod(hash_left, hash_right):
    if not hash_left:
        raise RuntimeError("left hash must be present")
    elif hash_right:
        return sha_hash(hash_left + hash_right)
    else:
        return hash_left

def combine_hash_simple(hash_left, hash_right):
    if not hash_left:
        raise RuntimeError("left hash must be present")
    elif hash_right:
        return hash_left + hash_right
    else:
        return hash_left

class Node:
    def __init__(self, point, hash_value):
        self.point = point
        self.hash_value = hash_value

    def __eq__(self, other):
        return (self.point == other.point) and (self.hash_value ==
                other.hash_value)

    def __str__(self):
        return 'node ' + str(self.point) + ' ' + str(self.hash_value)

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def even(self):
        return self.x % 2 == 0

    def __str__(self):
        return 'point({0},{1})'.format(self.x, self.y)

    def __eq__(self, other):
        return (self.x == other.x) and (self.y == other.y)

    def __hash__(self):
        return hash((self.x, self.y))

    def sibling(self):
        """ the point with the same parent as this point """
        if self.even():
            return Point(self.x + 1, self.y)
        else:
            return Point(self.x - 1, self.y)


class MerkleTree:

    def __init__(self, hash_store):
        self.hash_store = hash_store
        if self.hash_store.exists("max-y"):
            self.max_y = self.hash_store.get("max-y")
        else:
            self.max_y = 0
            self.hash_store.set("max-y",0)

    def update_tree(self, entry_number, entry):
        entry_hash = sha_hash(entry)
        self.update_max_y( entry_number )
        path = self.path_to_root( Point(entry_number, 0) )
        siblings = [p.sibling() for p in path]
        sibling_nodes = self.read_hashes(siblings)
        updated_nodes = self.update_nodes(entry_hash, path, sibling_nodes)
        self.store_hashes(point_updated_hashes, redis)

    def update_max_y(self, entry_number ):
        if self.max_y == 0 or entry_number >= (2 << (self.max_y - 1)):
            self.max_y = self.hash_store.incr("max-y")

    def update_nodes(self, entry_hash, path, sibling_nodes):
        """ update the nodes which will be affected by the addition of the new
        entry    """
        updated_nodes = [Node(path[0], entry_hash)]
        #pdb.set_trace()
        for i in range(1, len(path)):
            previous_sibling_node = sibling_nodes[i - 1]
            previous_node = updated_nodes[i - 1]
            if path[i - 1].even():
                updated_hash = combine_hash_simple(previous_node.hash_value, previous_sibling_node.hash_value)
            else:
                updated_hash = combine_hash_simple(previous_sibling_node.hash_value, previous_node.hash_value)
            updated_nodes.append(Node(path[i], updated_hash))
        return updated_nodes

    def read_hashes(self, points):
        """ get the list of Nodes corresponding to points"""
        return [Node(p, self.hash_store.get(point_key(p)) ) for p in points]

    def store_hashes(self, nodes):
        for node in nodes:
            key = point_key( node.point )
            print('key: {0}, value: {1}'.format(key, str(node.point)))
            self.hash_store.set(key, node.hash_value)

    # Tuple<Point>
    def path_to_root(self, point):
        if point.y == self.max_y:
            return point,
        else:
            return (point ,) + self.path_to_root(Point( point.x >> 1, point.y + 1))

    def point_key(point):
        return str(point.y) + "-" + str(point.x)
