from collections import defaultdict
import heapq
import sys


class Node:

    def __init__(self, *args, **kwargs):
        self.data = kwargs.get('data') or None
        self.left = kwargs.get('left') or None
        self.right = kwargs.get('right') or None

    def get_data(self):
        return self.data


class FreqNode(Node):

    def __init__(self, freq, *args, **kwargs):
        super(FreqNode, self).__init__(*args, **kwargs)
        self.freq = freq

    def frequency(self):
        return self.freq

    def __repr__(self):
        return f'{self.freq} + /{self.left}/ and /{self.right}/'

    def __lt__(self, other):
        return self.frequency() < other.frequency()

    def __gt__(self, other):
        return self.frequency() > other.frequency()


class PriorityQueue():

    def __init__(self):
        self._pq = []

    def size(self):
        return len(self._pq)

    def is_empty(self):
        return len(self._pq) == 0

    def push(self, item):
        return heapq.heappush(self._pq, item)

    def pop(self):
        try:
            return heapq.heappop(self._pq)
        except IndexError:
            return None


class HuffmanTree:

    def __init__(self, freq_map):
        self._freq_map = freq_map
        self._pq = PriorityQueue()
        self._root = None
        self._code_map = {}

    def _insert_into_pq(self):
        for val, count in self._freq_map.items():
            node = FreqNode(freq=count, data=val)
            self._pq.push(node)

    def create(self):
        self._insert_into_pq()

        if self._pq.is_empty():
            self._root = None
        if self._pq.size() == 1:
            item_1 = self._pq.pop()
            self._root = FreqNode(freq=item_1.frequency(), left=item_1)

        while (not self._pq.is_empty()):
            item_1 = self._pq.pop()
            if item_1 is None:
                break
            item_2 = self._pq.pop()
            if item_2 is None:
                self._root = item_1
                break

            new_priority = item_1.frequency() + item_2.frequency()
            item = FreqNode(
                freq=new_priority,
                left=item_1,
                right=item_2
            )
            self._pq.push(item)

    def generate_codes(self, tree=None, prefix=''):
        if tree is None:
            tree = self._root

        left = tree.left
        right = tree.right

        if not (left or right):
            self._code_map[tree.get_data()] = prefix

        if left:
            self.generate_codes(tree=left, prefix=prefix + '0')
        if right:
            self.generate_codes(tree=right, prefix=prefix + '1')

        return self._code_map

    def find_value(self, code):
        root = self._root
        decoded_str = ''
        for b in code:
            if not (root.left or root.right):
                decoded_str += root.get_data()
                root = self._root
            if b == '0':
                root = root.left
            else:
                root = root.right

        if not (root.left or root.right):
            decoded_str += root.get_data()

        return decoded_str


class HuffmanEncoder(object):

    def __init__(self, data):
        self._code_map = {}
        self._freq_map = defaultdict(lambda: 0)
        self._data = data
        self._tree = None

    def get_data(self):
        return self._data

    def get_frequency_map(self):
        return self._freq_map

    def get_code_map(self):
        return self._code_map

    def get_tree(self):
        return self._tree

    def _generate_freq_map(self):
        for val in self.get_data():
            self._freq_map[val.lower()] += 1

    def _generate_code_map(self):
        self._code_map = self._tree.generate_codes()

    def _init_tree(self):
        self._tree = HuffmanTree(freq_map=self.get_frequency_map())
        self._tree.create()

    def _get_encoded_string(self):
        code_map = self.get_code_map()
        return ''.join(code_map[char.lower()] for char in self.get_data())

    def encode(self):
        self._generate_freq_map()
        self._init_tree()
        self._generate_code_map()
        return self._get_encoded_string()


class HuffmanDecoder(object):

    def __init__(self, tree, code):
        self._tree = tree
        self._code = code

    def decode(self):
        return self._tree.find_value(code=self._code)


def huffman_encoding(data):
    compressor = HuffmanEncoder(data=data)
    return compressor.encode(), compressor.get_tree()


def huffman_decoding(code, tree):
    return HuffmanDecoder(tree=tree, code=code).decode()


if __name__ == "__main__":
    codes = {}

    a_great_sentence = "The bird is the word"

    print("The size of the data is: {}\n".format(sys.getsizeof(a_great_sentence)))  # The size of the data is: 69
    print(
        "The content of the data is: {}\n".format(a_great_sentence))  # The content of the data is: The bird is the word

    encoded_data, tree = huffman_encoding(a_great_sentence)

    print("The size of the encoded data is: {}\n".format(
        sys.getsizeof(int(encoded_data, base=2))))  # The size of the encoded data is: 36
    print("The content of the encoded data is: {}\n".format(
        encoded_data))  # The content of the encoded data is: 00111111100010000111011011000111100001010011111110001101010111101100

    decoded_data = huffman_decoding(encoded_data, tree)

    print("The size of the decoded data is: {}\n".format(
        sys.getsizeof(decoded_data)))  # The size of the decoded data is: 69
    print("The content of the encoded data is: {}\n".format(
        decoded_data))  # The content of the encoded data is: the bird is the word

    # Test case 1
    print('Test Case 2')
    a_great_sentence = "My name is varun bansal"

    print("The size of the data is: {}\n".format(sys.getsizeof(a_great_sentence)))
    print("The content of the data is: {}\n".format(a_great_sentence))

    encoded_data, tree = huffman_encoding(a_great_sentence)

    print("The size of the encoded data is: {}\n".format(sys.getsizeof(int(encoded_data, base=2))))
    print("The content of the encoded data is: {}\n".format(encoded_data))

    decoded_data = huffman_decoding(encoded_data, tree)

    print("The size of the decoded data is: {}\n".format(sys.getsizeof(decoded_data)))
    print("The content of the encoded data is: {}\n".format(decoded_data))

    # Test case 3
    print('Test Case 3')
    a_great_sentence = "cccccc"

    print("The size of the data is: {}\n".format(sys.getsizeof(a_great_sentence)))
    print("The content of the data is: {}\n".format(a_great_sentence))

    encoded_data, tree = huffman_encoding(a_great_sentence)

    print("The size of the encoded data is: {}\n".format(sys.getsizeof(int(encoded_data, base=2))))
    print("The content of the encoded data is: {}\n".format(encoded_data))

    decoded_data = huffman_decoding(encoded_data, tree)

    print("The size of the decoded data is: {}\n".format(sys.getsizeof(decoded_data)))
    print("The content of the decoded data is: {}\n".format(decoded_data))
