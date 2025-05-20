import tkinter as tk
from tkinter import filedialog
import matplotlib.pyplot as plt
import heapq
from tkinter import ttk
from pathlib import Path
import os
import time

class HuffmanCoding:
    def __init__(self, path):
        self.path = path
        # self.data_path = "Data\\decoded_text.txt"
        self.codes = {}
        self.root = None
        self.content = ""

    class HeapNodeFormation:
        def __init__(self, frequency, characters):
            self.characters = characters
            self.frequency = frequency
            self.left = None
            self.right = None

        def __lt__(self, other):
            return self.frequency < other.frequency

        def __eq__(self, other):
            return self.frequency == other.frequency

        def __add__(self, other):
            return HuffmanCoding.HeapNodeFormation ( self.frequency + other.frequency, None )

    def get_frequencies(self, chars):
        char_frequencies = {}
        for char in chars:
            if char in char_frequencies:
                char_frequencies[char] += 1
            else:
                char_frequencies[char] = 1
        return char_frequencies

    def get_min_heap(self, chars):
        char_frequencies = self.get_frequencies ( chars )
        # list of tupples with increasing order of frequencies and characters
        priority_queue = [HuffmanCoding.HeapNodeFormation ( freq, char ) for char, freq in char_frequencies.items ()]
        # The priority queue is stored in the heap
        heapq.heapify ( priority_queue )
        return priority_queue

    # Returns a dictionary with the character and its frequency in the string
    def build_huffman_tree(self, chars):
        priority_queue = self.get_min_heap ( chars )
        while len ( priority_queue ) > 1:
            left_node = heapq.heappop ( priority_queue )
            right_node = heapq.heappop ( priority_queue )

            tree_node = left_node + right_node
            tree_node.left = left_node
            tree_node.right = right_node

            heapq.heappush ( priority_queue, tree_node )
            self.root = priority_queue[0]
        return priority_queue[0]

    def binary_codes_logic(self, root_node, code):
        if root_node is not None:
            self.codes[root_node.characters] = code

        if root_node.left is not None:
            self.binary_codes_logic ( root_node.left, code + "0" )
        if root_node.right is not None:
            self.binary_codes_logic ( root_node.right, code + "1" )

    def encode_data(self, words):
        encoded_data = ""
        for character in words:
            encoded_data += self.codes[character]

        return encoded_data

    def decode_data(self, encoded):
        decoded_data = ""
        node = self.root
        for bit in encoded:
            if bit == "0" and node is not None:
                node = node.left
            if bit == "1" and node is not None:
                node = node.right

            if node.characters is not None:
                decoded_data += node.characters
                node = self.root

        return decoded_data

    def file_reader(self):
        chunk_size = 1024
        path = Path(self.path)

        if path.is_file():
            try:
                with open(path, 'r', encoding='utf-8') as file:
                    while True:
                        chunk = file.read ( chunk_size )
                        if not chunk:
                            break
                        self.content += chunk
            except Exception as e:
                print(f"Error reading the file {path}: {e}")

        return self.content

class HuffmanApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Huffman Coding Compression")

        # Set the fixed size for the GUI window
        self.root.geometry("600x400")  # Adjust the width and height as needed

        # Frame for the first line of buttons
        frame1 = tk.Frame(root)
        frame1.pack(side="top", anchor="w", padx=10, pady=10)

        # Input Text
        self.text_input_label = tk.Label(frame1, text="Select File:", font=("Helvetica", 12), anchor="w")
        self.text_input_label.pack(side="left")

        self.file_path = None

        # Browse Button
        self.browse_button = tk.Button(frame1, text="Browse...", command=self.browse_file, font=("Helvetica", 10))
        self.browse_button.pack(side="left", padx=10)

        # Display label for file status
        self.file_status_label = tk.Label(frame1, text="File not selected", font=("Helvetica", 10), fg="red")
        self.file_status_label.pack(side="left", padx=10)
        frame2 = tk.Frame(root)
        frame2.pack(side="top", anchor="w", padx=10, pady=10)

        # Upload Button
        self.upload_button = tk.Button(frame2, text="Upload", command=self.upload_file, font=("Helvetica", 10),
                                       bg="#4CAF50",  # Green background color
                                       fg="white")    # White text color
        self.upload_button.pack(side="left", padx=10)

        # Frame for the second line of buttons
        frame2 = tk.Frame(root)
        frame2.pack(side="top", anchor="w", padx=10, pady=10)

        # Frame for the third line of buttons
        frame3 = tk.Frame(root)
        frame3.pack(side="top", anchor="w", padx=10, pady=10)

        # Performance Graph Button
        performance_button = ttk.Button(frame3, text="View Performance Graph", command=self.show_performance_graph, style="TButton", padding=5)
        performance_button.pack(side="left", padx=10)

        # Frame for the fourth line of widgets
        frame4 = tk.Frame(root)
        frame4.pack(side="top", anchor="w", padx=10, pady=10)

        # Output
        self.result_label = tk.Label(frame4, text="", font=("Helvetica", 10), wraplength=300, anchor="w", fg="red")
        self.result_label.pack(side="left", padx=10)

        self.huffman_coding = object

        # Configure Style
        style = ttk.Style()
        style.configure("TButton", font=("Helvetica", 10))

    def browse_file(self):
        self.file_path = filedialog.askopenfilenames()
        if self.file_path:
            self.file_status_label.config(text="File selected", fg="green")
        else:
            self.file_status_label.config(text="File not selected", fg="red")

    def upload_file(self):
        if self.file_path:
            self.result_label.config(text="File uploaded successfully", fg="black")
        else:
            self.result_label.config(text="Please select a file before uploading", fg="red")

    def calculate_compression_ratio(self, original_size, compressed_size):
        compression_ratio = original_size / compressed_size
        return compression_ratio

    def compress(self, object, num):
        if self.file_path:
            words = object.file_reader ()
            tree = object.build_huffman_tree ( words )
            object.binary_codes_logic ( tree, "" )
            encoded = object.encode_data ( words )
            if encoded:
                original_size = len ( words ) * 8  # Assuming 8 bits per character
                compressed_size = len ( encoded )

                with open ( f"Data//Encoded//encoded_output{num}.txt", 'w' ) as file:
                    file.write ( encoded )

                self.result_label.config ( text=f"Decompressed data saved in 'Data/decompressed_output.txt' location",
                                           fg="black" )
                return original_size, compressed_size, encoded
        return 0, 0, ""

    def decompress(self, encoded_data,num):
        if encoded_data:
            decompressed_data = self.huffman_coding.decode_data(encoded_data)

            # Save decompressed data to a file
            with open(f"Data//Decoded//decompressed_output{num}.txt", 'w') as file:
                file.write(decompressed_data)

            self.result_label.config(text=f"Decompressed data saved in 'Data/decompressed_output.txt' location", fg="black")
        else:
            self.result_label.config(text="Please upload a file first", fg="red")

    def measure_time(self, file_name, num):
        self.huffman_coding = HuffmanCoding ( file_name )
        compress_start_time = time.time ()
        original_size, compressed_size, encoded_data = self.compress ( self.huffman_coding, num )
        compress_time = time.time () - compress_start_time

        decompress_start_time = time.time ()
        # Scheduling decompression to run after a short delay
        self.root.after ( 10, lambda data=encoded_data: self.decompress ( data, num ) )
        decompress_time = time.time () - decompress_start_time

        compression_ratio = self.calculate_compression_ratio ( original_size, compressed_size )
        print ( f"Compression Ratio: {compression_ratio}" )
        return compress_time, decompress_time

    def show_performance_graph(self):
        file_size = []
        compression_times = []
        decompression_times = []
        if self.file_path:
            for i in range(len(self.file_path)):
                file_name = self.file_path[i]
                if file_name:
                    with open (file_name, 'r' ) as file:
                        input_data = file.read ()
                        file_size.append ( len ( input_data ) )
                        compress_time, decompress_time = self.measure_time (file_name, i)
                        compression_times.append ( compress_time )
                        decompression_times.append ( decompress_time )

        else:
            self.result_label.config ( text="Please upload a file first", fg="red" )

        # Plot the performance graph
        plt.plot(file_size, compression_times, label='Compression Time')
        plt.plot(file_size, decompression_times, label='Decompression Time')
        plt.xlabel('Data Size')
        plt.ylabel('Time (s)')
        plt.title('Huffman Compression and Decompression Performance')
        plt.legend()
        plt.show()



if __name__ == "__main__":
    root = tk.Tk()
    app = HuffmanApp(root)
    root.mainloop()
