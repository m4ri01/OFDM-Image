import heapq
import random
from collections import defaultdict, Counter
from bitarray import bitarray

class HuffmanNode:
    def __init__(self, symbol=None, freq=0, left=None, right=None):
        self.symbol = symbol
        self.freq = freq
        self.left = left
        self.right = right

    # Define comparison operators for the priority queue
    def __lt__(self, other):
        return self.freq < other.freq

def build_huffman_tree(frequency):
    heap = [HuffmanNode(symbol=sym, freq=freq) for sym, freq in frequency.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        merged = HuffmanNode(freq=left.freq + right.freq, left=left, right=right)
        heapq.heappush(heap, merged)

    return heap[0]

def generate_huffman_codes(node, prefix='', codebook=None):
    if codebook is None:
        codebook = {}
    if node.symbol is not None:
        codebook[node.symbol] = prefix
    else:
        generate_huffman_codes(node.left, prefix + '0', codebook)
        generate_huffman_codes(node.right, prefix + '1', codebook)
    return codebook

def encode(data, codebook):
    encoded_data = bitarray()
    for chunk in data:
        encoded_data.extend(codebook[chunk])
    return encoded_data


def decode(encoded_data, tree):
    decoded_data = []
    node = tree
    for bit in encoded_data:
        node = node.left if bit == 0 else node.right
        if node.symbol is not None:
            decoded_data.append(node.symbol)
            node = tree
    return decoded_data

def main(encoder_data, binary_data):
    # Frequency analysis
    frequency = Counter(binary_data)
    huffman_tree = build_huffman_tree(frequency)
    decoded_data = decode(encoder_data, huffman_tree)
    decoded_data = ''.join(str(bit) for bit in decoded_data)
    return decoded_data

def decode_huffman_image(encoder_data, binary_data):
    data1 = ''.join(str(bit) for bit in encoder_data)
    data2 = ''.join(str(bit) for bit in binary_data)
    data1 = bitarray(data1)

    remainder = len(data2) % 8
    if remainder != 0:
        data2 += '0' * (8 - remainder)

    bin_values = []
    temp_value = []
    for idx, r in enumerate(data2):
        temp_value.append(r)
        if (idx + 1) % 8 == 0:
            str_temp = "".join(temp_value)
            bin_values.append(str_temp)
            temp_value = []
    bin_values = bin_values[1:]

    decoded_data = main(data1,bin_values)
    decoded_data = [int(bit) for bit in decoded_data]
    return decoded_data
