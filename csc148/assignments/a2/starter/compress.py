"""
Assignment 2 starter code
CSC148
Instructors: Bogdan Simion, Rutwa Engineer, Marc De Benedetti, Romina Piunno
"""
from __future__ import annotations

import time

from huffman import HuffmanTree
from utils import *


# ====================
# Functions for compression
# ====================


def build_frequency_dict(text: bytes) -> dict[int, int]:
    """ Return a dictionary which maps each of the bytes in <text> to its
    frequency.

    >>> d = build_frequency_dict(bytes([65, 66, 67, 66]))
    >>> d == {65: 1, 66: 2, 67: 1}
    True
    """
    data = {}

    for num in text:
        if num in data:
            data[num] += 1
        else:
            data[num] = 1

    return data


def build_huffman_tree(freq_dict: dict[int, int]) -> HuffmanTree:
    """ Return the Huffman tree corresponding to the frequency dictionary
    <freq_dict>.

    Precondition: freq_dict is not empty.

    >>> freq = {2: 6, 3: 4}
    >>> t = build_huffman_tree(freq)
    >>> result = HuffmanTree(None, HuffmanTree(3), HuffmanTree(2))
    >>> t == result
    True
    >>> freq = {2: 6, 3: 4, 7: 5}
    >>> t = build_huffman_tree(freq)
    >>> result = HuffmanTree(None, HuffmanTree(2), \
                             HuffmanTree(None, HuffmanTree(3), HuffmanTree(7)))
    >>> t == result
    True
    >>> import random
    >>> symbol = random.randint(0,255)
    >>> freq = {symbol: 6}
    >>> t = build_huffman_tree(freq)
    >>> any_valid_byte_other_than_symbol = (symbol + 1) % 256
    >>> dummy_tree = HuffmanTree(any_valid_byte_other_than_symbol)
    >>> result = HuffmanTree(None, HuffmanTree(symbol), dummy_tree)
    >>> t.left == result.left or t.right == result.left
    True
    """
    data = []
    for sign, num in freq_dict.items():
        data.append((num, HuffmanTree(sign)))

    if 1 == len(data):
        og_sign = list(freq_dict.keys())[0]
        temp_shy = (og_sign + 1) % 256
        return HuffmanTree(
            None,
            HuffmanTree(og_sign),
            HuffmanTree(temp_shy)
        )

    while 1 < len(data):

        for x in range(len(data)):
            for y in range(x + 1, len(data)):
                if data[y][0] < data[x][0]:
                    data[x], data[y] = data[y], data[x]

        (first_num, first_tree), (second_num, tree_b) = data[:2]
        final_tree = HuffmanTree(None, first_tree, tree_b)
        final_num = first_num + second_num

        data = data[2:] + [(final_num, final_tree)]

    return data[0][1]


def helper_traversal(node: HuffmanTree, bins: str, nums: dict[int, str]) -> None:
    """
    Using recursion this function iterates through the huffman tree and builds
    binary codes for each symbol. This function does not return anything and is
    later used in get_codes to build a dictionary full of these binary codes.
    """

    if node.is_leaf():
        nums[node.symbol] = bins
    else:
        if node.left:
            helper_traversal(node.left, bins + "0", nums)
        if node.right:
            helper_traversal(node.right, bins + "1", nums)


def get_codes(tree: HuffmanTree) -> dict[int, str]:
    """ Return a dictionary which maps symbols from the Huffman tree <tree>
    to codes.

    >>> tree = HuffmanTree(None, HuffmanTree(3), HuffmanTree(2))
    >>> d = get_codes(tree)
    >>> d == {3: "0", 2: "1"}
    True
    """
    nums = {}
    helper_traversal(tree, "", nums)
    return nums


def mapper(node: HuffmanTree, counter: list[int]) -> None:
    """
    Using recursion, this helper function gives a number to each internal node
    in the Huffman tree. It starts from the leaves and works its way up,
    increasing the counter.

    """

    if not node.is_leaf():

        if node.left:
            mapper(node.left, counter)
        if node.right:
            mapper(node.right, counter)

        node.number = counter[0]
        counter[0] += 1


def number_nodes(tree: HuffmanTree) -> None:
    """ Number internal nodes in <tree> according to postorder traversal. The
    numbering starts at 0.

    >>> left = HuffmanTree(None, HuffmanTree(3), HuffmanTree(2))
    >>> right = HuffmanTree(None, HuffmanTree(9), HuffmanTree(10))
    >>> tree = HuffmanTree(None, left, right)
    >>> number_nodes(tree)
    >>> tree.left.number
    0
    >>> tree.right.number
    1
    >>> tree.number
    2
    """
    counter = [0]
    mapper(tree, counter)


def avg_length(tree: HuffmanTree, freq_dict: dict[int, int]) -> float:
    """ Return the average number of bits required per symbol, to compress the
    text made of the symbols and frequencies in <freq_dict>, using the Huffman
    tree <tree>.

    The average number of bits = the weighted sum of the length of each symbol
    (where the weights are given by the symbol's frequencies), divided by the
    total of all symbol frequencies.

    >>> freq = {3: 2, 2: 7, 9: 1}
    >>> left = HuffmanTree(None, HuffmanTree(3), HuffmanTree(2))
    >>> right = HuffmanTree(9)
    >>> tree = HuffmanTree(None, left, right)
    >>> avg_length(tree, freq)  # (2*2 + 7*2 + 1*1) / (2 + 7 + 1)
    1.9
    """
    acc_nums = 0
    acc_signs = 0
    data = get_codes(tree)

    for signs, nums in freq_dict.items():
        acc_signs += nums
        total = len(data[signs])
        acc_nums += nums * total

    return acc_nums / acc_signs


def compress_bytes(text: bytes, codes: dict[int, str]) -> bytes:
    """ Return the compressed form of <text>, using the mapping from <codes>
    for each symbol.

    >>> d = {0: "0", 1: "10", 2: "11"}
    >>> text = bytes([1, 2, 1, 0])
    >>> result = compress_bytes(text, d)
    >>> result == bytes([184])
    True
    >>> [byte_to_bits(byte) for byte in result]
    ['10111000']
    >>> text = bytes([1, 2, 1, 0, 2])
    >>> result = compress_bytes(text, d)
    >>> [byte_to_bits(byte) for byte in result]
    ['10111001', '10000000']
    """

    acc = []
    for x in text:
        new = codes[x]
        acc.append(new)

    acc_string = ''
    for y in acc:
        acc_string += y

    total = len(acc_string)
    leftover = total % 8

    if leftover != 0:
        filler = 8 - leftover
    else:
        filler = 0

    acc_string += filler * '0'
    acc1 = []

    for i in range(0, len(acc_string), 8):
        nums = acc_string[i:i + 8]
        wholes = bits_to_byte(nums)
        acc1.append(wholes)

    return bytes(acc1)


def postorder_traversal(node: HuffmanTree, output: bytearray) -> None:
    """
    Goes through the Huffman tree from the bottom up. Adds info about each
    branch to the output after visiting its children.
    """
    if node.is_leaf():
        return

    for x in (node.left, node.right):
        if x:
            postorder_traversal(x, output)

    acc = []
    for child in (node.left, node.right):
        if child.is_leaf():
            acc.append((0, child.symbol))
        else:
            acc.append((1, child.number))

    for byte, num in acc:
        output.append(byte)
        output.append(num)


def tree_to_bytes(tree: HuffmanTree) -> bytes:
    """ Return a bytes representation of the Huffman tree <tree>.
    The representation should be based on the postorder traversal of the tree's
    internal nodes, starting from 0.

    Precondition: <tree> has its nodes numbered.

    >>> tree = HuffmanTree(None, HuffmanTree(3, None, None), \
    HuffmanTree(2, None, None))
    >>> number_nodes(tree)
    >>> list(tree_to_bytes(tree))
    [0, 3, 0, 2]
    >>> left = HuffmanTree(None, HuffmanTree(3, None, None), \
    HuffmanTree(2, None, None))
    >>> right = HuffmanTree(5)
    >>> tree = HuffmanTree(None, left, right)
    >>> number_nodes(tree)
    >>> list(tree_to_bytes(tree))
    [0, 3, 0, 2, 1, 0, 0, 5]
    >>> tree = build_huffman_tree(build_frequency_dict(b"helloworld"))
    >>> number_nodes(tree)
    >>> list(tree_to_bytes(tree))\
            #doctest: +NORMALIZE_WHITESPACE
    [0, 104, 0, 101, 0, 119, 0, 114, 1, 0, 1, 1, 0, 100, 0, 111, 0, 108,\
    1, 3, 1, 2, 1, 4]
    """
    result = bytearray()
    postorder_traversal(tree, result)
    return bytes(result)


def compress_file(in_file: str, out_file: str) -> None:
    """ Compress contents of the file <in_file> and store results in <out_file>.
    Both <in_file> and <out_file> are string objects representing the names of
    the input and output files.

    Precondition: The contents of the file <in_file> are not empty.
    """
    with open(in_file, "rb") as f1:
        text = f1.read()
    freq = build_frequency_dict(text)
    tree = build_huffman_tree(freq)
    codes = get_codes(tree)
    number_nodes(tree)
    print("Bits per symbol:", avg_length(tree, freq))
    result = (tree.num_nodes_to_bytes() + tree_to_bytes(tree)
              + int32_to_bytes(len(text)))
    result += compress_bytes(text, codes)
    with open(out_file, "wb") as f2:
        f2.write(result)


# ====================
# Functions for decompression
def subtrees(node_lst, types, data):
    """
    Builds part of a Huffman tree. If the type is 0, it makes a simple tree.
    Otherwise, it builds a more complex tree using the node list and data.
    """
    if types == 0:
        return HuffmanTree(data)
    else:
        return generate_tree_general(node_lst, data)


def generate_tree_general(node_lst: list[ReadNode],
                          root_index: int) -> HuffmanTree:
    """ Return the Huffman tree corresponding to node_lst[root_index].
    The function assumes nothing about the order of the tree nodes in the list.

    >>> lst = [ReadNode(0, 5, 0, 7), ReadNode(0, 10, 0, 12), \
    ReadNode(1, 1, 1, 0)]
    >>> generate_tree_general(lst, 2)
    HuffmanTree(None, HuffmanTree(None, HuffmanTree(10, None, None), \
HuffmanTree(12, None, None)), \
HuffmanTree(None, HuffmanTree(5, None, None), HuffmanTree(7, None, None)))
    """
    current_node = node_lst[root_index]

    left_tree = subtrees(node_lst, current_node.l_type, current_node.l_data)
    right_tree = subtrees(node_lst, current_node.r_type, current_node.r_data)

    return HuffmanTree(None, left_tree, right_tree)


def tree_creation(types, data, acc):
    if types == 0:
        return HuffmanTree(data)
    else:
        return acc.pop()


def pushing(node, acc):
    """
    This function builds a Huffman tree by combining a node's left and
    right data into a new tree, and then adds that new tree to a list
    called acc.
    """
    right_tree = tree_creation(node.r_type, node.r_data, acc)
    left_tree = tree_creation(node.l_type, node.l_data, acc)
    combined_tree = HuffmanTree(None, left_tree, right_tree)
    acc.append(combined_tree)


def generate_tree_postorder(node_lst: list[ReadNode],
                            root_index: int) -> HuffmanTree:
    """ Return the Huffman tree corresponding to node_lst[root_index].
    The function assumes that the list represents a tree in postorder.

    >>> lst = [ReadNode(0, 5, 0, 7), ReadNode(0, 10, 0, 12), \
    ReadNode(1, 0, 1, 0)]
    >>> generate_tree_postorder(lst, 2)
    HuffmanTree(None, HuffmanTree(None, HuffmanTree(5, None, None), \
HuffmanTree(7, None, None)), \
HuffmanTree(None, HuffmanTree(10, None, None), HuffmanTree(12, None, None)))
    """
    stack = []

    for curr in range(0, root_index + 1):
        curr_node = node_lst[curr]
        pushing(curr_node, stack)

    return stack[-1]


def symbol_search(tree, data):

    curr_node = tree

    for nums in data:

        if curr_node.is_leaf():
            return current_node.symbol

        if nums == '0':
            current_node = current_node.left

        else:
            current_node = current_node.right

    return None


def symbol_traversal(tree, nums, starter):
    """
    This function follows a path through a binary tree based on a list of
    0s and 1s, and returns the symbol of the leaf node it ends up at, along
    with the position it stopped at.
    """
    curr_node = tree
    index = starter

    while not curr_node.is_leaf() and index < len(nums):
        curr_num = nums[index]

        if curr_num == '0':
            curr_node = curr_node.left
        else:
            curr_node = curr_node.right

        index += 1

    return curr_node.symbol, index


def decompress_bytes(tree: HuffmanTree, text: bytes, size: int) -> bytes:
    """ Use Huffman tree <tree> to decompress <size> bytes from <text>.

    >>> tree = build_huffman_tree(build_frequency_dict(b'helloworld'))
    >>> number_nodes(tree)
    >>> decompress_bytes(tree, \
             compress_bytes(b'helloworld', get_codes(tree)), len(b'helloworld'))
    b'helloworld'
    """
    acc = bytearray()
    counter = 0

    data = []
    for x in text:
        convert = byte_to_bits(x)
        for y in convert:
            data.append(y)

    index = 0

    while index < len(data) and counter < size:
        symbol, index = symbol_traversal(tree, data, index)
        acc.append(symbol)
        counter += 1

    return bytes(acc)


def decompress_file(in_file: str, out_file: str) -> None:
    """ Decompress contents of <in_file> and store results in <out_file>.
    Both <in_file> and <out_file> are string objects representing the names of
    the input and output files.

    Precondition: The contents of the file <in_file> are not empty.
    """
    with open(in_file, "rb") as f:
        num_nodes = f.read(1)[0]
        buf = f.read(num_nodes * 4)
        node_lst = bytes_to_nodes(buf)
        # use generate_tree_general or generate_tree_postorder here
        tree = generate_tree_general(node_lst, num_nodes - 1)
        size = bytes_to_int(f.read(4))
        with open(out_file, "wb") as g:
            text = f.read()
            g.write(decompress_bytes(tree, text, size))


# ====================
# Other functions
def in_order_traversal(node, data):
    """
    This function performs an in-order traversal on a binary tree, but it only
    collects the leaf nodes
    """
    if node is None:
        return
    if node.is_leaf():
        data.append(node)
    else:
        in_order_traversal(node.left, data)
        in_order_traversal(node.right, data)


def improve_tree(tree: HuffmanTree, freq_dict: dict[int, int]) -> None:
    """ Improve the tree <tree> as much as possible, without changing its shape,
    by swapping nodes. The improvements are with respect to the dictionary of
    symbol frequencies <freq_dict>.

    >>> left = HuffmanTree(None, HuffmanTree(99, None, None), \
    HuffmanTree(100, None, None))
    >>> right = HuffmanTree(None, HuffmanTree(101, None, None), \
    HuffmanTree(None, HuffmanTree(97, None, None), HuffmanTree(98, None, None)))
    >>> tree = HuffmanTree(None, left, right)
    >>> freq = {97: 26, 98: 23, 99: 20, 100: 16, 101: 15}
    >>> avg_length(tree, freq)
    2.49
    >>> improve_tree(tree, freq)
    >>> avg_length(tree, freq)
    2.31
    """
    acc = []
    in_order_traversal(tree, acc)

    lst = list(freq_dict.keys())

    for num in range(len(lst) - 1):
        if freq_dict[lst[num + 1]] > freq_dict[lst[num]]:
            lst[num], = lst[num + 1]
            lst[num + 1] = lst[num]

    for char in range(min(len(acc), len(lst))):
        acc[char].symbol = lst[char]


if __name__ == "__main__":
    import doctest

    doctest.testmod()

    import python_ta

    python_ta.check_all(config={
        'allowed-io': ['compress_file', 'decompress_file'],
        'allowed-import-modules': [
            'python_ta', 'doctest', 'typing', '__future__',
            'time', 'utils', 'huffman', 'random'
        ],
        'disable': ['W0401']
    })

    mode = input(
        "Press c to compress, d to decompress, or other key to exit: ")
    if mode == "c":
        fname = input("File to compress: ")
        start = time.time()
        compress_file(fname, fname + ".huf")
        print(f"Compressed {fname} in {time.time() - start} seconds.")
    elif mode == "d":
        fname = input("File to decompress: ")
        start = time.time()
        decompress_file(fname, fname + ".orig")
        print(f"Decompressed {fname} in {time.time() - start} seconds.")
