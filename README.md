Huffman File Compressor

A compact file compression and decompression tool written in Python that implements the Huffman coding algorithm. Huffman coding is a loss‑less compression method that assigns shorter binary codes to frequently occurring symbols and longer codes to rare ones, thereby reducing overall file size without losing any data. This project demonstrates how to build and traverse Huffman trees, perform bit‑level I/O and encode/decode arbitrary files, including text, audio and images. It is based on an assignment from the University of Toronto’s CSC148 course, with starter code provided for educational use.

What this project does

The compressor reads an input file as a sequence of bytes, computes a frequency dictionary mapping each byte to the number of times it appears, and then builds a Huffman tree by repeatedly combining the two least‑frequent symbols into a new internal node. Once the tree is constructed, a recursive traversal assigns a unique prefix code to each symbol; leaf nodes store the actual bytes, while internal nodes carry no symbol and point to subtrees. The original file is then encoded into a stream of bits according to this code table, padded to a multiple of eight bits and written out as bytes.

The compressed file begins with a small header. First, the number of internal nodes (plus one) is stored as a single byte using the num_nodes_to_bytes() method of the HuffmanTree class. Next, the structure of the tree itself is serialized using a post‑order traversal: each internal node is recorded as two pairs of bytes indicating whether its children are leaves or pointers to earlier nodes. Finally, a 32‑bit little‑endian integer stores the length of the original file, followed by the encoded payload. During decompression, the program reconstructs the Huffman tree from this header, then decodes the bit stream back into the original sequence of bytes. An optional improve_tree function rearranges the labels on leaves to reduce the average code length without changing the tree shape.

Implementation highlights
Core algorithms: The program defines functions such as build_frequency_dict(), build_huffman_tree(), get_codes() and compress_bytes() to perform the fundamental steps of Huffman coding. It uses recursion to number internal nodes in post‑order and to generate codes for each symbol.

Data structures: A simple HuffmanTree class represents nodes with symbol, left, right and number attributes. Only leaves store symbols; interior nodes point to children and carry numbering for serialization.

Bit‑level utilities: Helper functions convert between integers and bit strings (get_bit(), byte_to_bits(), bits_to_byte()), translate byte arrays into 32‑bit integers (bytes_to_int()), and parse the serialized tree into ReadNode objects that record whether each child is a symbol or an internal node. These functions enable compact representation of the Huffman tree and encoded data.

Compression and decompression: compress_file() reads the entire file, builds the tree, computes codes, prints the average bits per symbol, and writes the header and compressed data. decompress_file() performs the inverse: it reads the node count, reconstructs the tree from the post‑order list of ReadNode objects, reads the original length and then decodes the remaining bytes back to the original content.

Testing: A suite of unit and property‑based tests using pytest and Hypothesis verifies that the frequency dictionary counts bytes correctly, the Huffman tree is built properly, codes are optimal regardless of dictionary order, and compressing then decompressing returns the original data. The tests also check that the serialized tree has the correct size and that average code lengths are within expected bounds.

How to run
Clone the repository and navigate to the starter folder:

git clone https://github.com/KunalMehta4/huffman-file-compressor.git

cd huffman-file-compressor/csc148/assignments/a2/starter

Compress a file: run python compress.py, choose c when prompted, and provide the path to the file you want to compress. The program will create a new file with a .huf extension and print the average bits per symbol.

Decompress a file: run python compress.py again, choose d, and supply the .huf file. The program will reconstruct the original file with an added .orig extension.

Run tests: in the same directory, execute pytest to run the unit and property‑based tests and confirm that your implementation passes all provided cases.

Educational value

This project offers hands‑on experience with:

Greedy algorithms and data compression: Huffman coding uses a greedy strategy to build an optimal prefix code based on symbol frequencies, ensuring that no code is a prefix of another. Implementing this algorithm reinforces understanding of greedy choices and optimal substructure.

Binary trees and recursion: Building, traversing and numbering a Huffman tree requires recursive functions for post‑order numbering and code generation.

Bitwise operations: The program works directly with bits, converting between bytes and bit strings for efficient storage and transmission.

File I/O and serialization: Writing and reading binary files, including constructing a compact header and interpreting it on decompression, demonstrates practical skills in binary serialization.

Testing and verification: Property‑based tests using Hypothesis check that compression is loss‑less and that various invariants hold, fostering confidence in algorithm correctness.

By completing this assignment, developers gain a deep understanding of data compression techniques and the nuances of working with binary data and recursive data structures.
