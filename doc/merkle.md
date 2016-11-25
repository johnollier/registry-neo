### Validating using Trees

If we have a sequence of data entries, then Merkle Trees allow us to validate a single entry both in terms of its value and its position in the sequence.

A Merkle Tree is a binary tree structure where hashes of entries are combined repeatedly to reach a single Root Hash for the whole sequence.

In this implementation, the hash values of n individual entries are placed on the bottom row of a perfect binary tree. We can view the tree as a coordinate system where the 'x' coordinate runs along the rows and the 'y' coordinate runs from 0 on the bottom row to k, where n is between 2<sup>k-1</sup> and 2<sup>k</sup>.

The diagram shows a tree containing 6 entries. The nodes with a dotted line exist in the coordinate system, but are empty.

![root-hash-diagram](https://github.com/johnollier/registry-neo/blob/master/doc/root-hash-diag.png)

For example the sixth node has coordinates (5,0) and its parent has coordinates (2,1). We get from a node to its parent by dividing the x coordinate by 2 and discarding any remainder; and adding 1 to the y coordinate. In this way we can find a sequence of nodes leading to the root node which will always have coordinates (0,k). The path to the root for the sixth node is shown in green.

The hash value in a non leaf node is the hash of the combination of the hashes of its child nodes. If the right child node is empty, then it's just the hash of the left child node.

If we calculate the hash of that node, then we need the hash values for the nodes coloured yellow in order to calculate the root hash.

### Updating the Tree

If we add an entry to the sequence, then as well as adding the hash of the entry to the tree, some previously empty positions in the tree will be populated and some non empty nodes will have to be updated.

If a seventh node is added to the example tree, then the nodes coloured red in figure 2 are the ones to be updated/added. It can be seen that they are nodes on the path from the new node to the root. The values in the sibling nodes coloured yellow are need to calculate the new hashes.
