import os
import heapq

class Huffman:
    def __init__(self, path):
        self.path = path
        self.heap =[]
        self.codes = {}
        self.reverse_codes = {}

    class HeapNode:
        def __init__(self, char , freq):
            self.char = char
            self.freq = freq
            self.left = None
            self.right = None

        def __lt__(self , other):
            return self.freq < other.freq
        
        #This function gives a boolean output 
        #it runs when two instances are compared with '<' symbol
        
        def __eq__(self , other):

            if other == None:
                return False
            if(not isinstance(other, HeapNode)):
                return False
            
            return self.freq == other.freq
        
        #line 2 checks wheather given other is an instance of heapnode or not, simply it
        #checks wheather "other" is "HeapNode" or not


    def make_frequency_dict(self, text):

        #calc frequency and return

        frequency = {}

        for char in text:
            if not char in frequency:
                frequency[char] = 0
            else: 
                frequency[char] +=1

        return frequency

    def make_heap(self,frequency):

        #make priority queue

        #heap = A heap has the property that the element with the highest (or lowest) priority can be accessed in constant tim

        for key in frequency:
            node = self.HeapNode(key, frequency[key])
            heapq.heappush(self.heap , node)


    def merge_codes(self):

        #build huffman tree . Save root in heap
        
        while(len(self.heap)>1):

            node1 = heapq.heappop(self.heap)
            node2 = heapq.heappop(self.heap)

            #heare we are poping from heap so node1 will be node with least freq
            #node2 will be node with 2nd least freq

            merged = self.HeapNode(None, node1.freq + node2.freq)

            merged.left = node1
            merged.right = node2

            heapq.heappush(self.heap ,merged)

    
    def make_codes_helper(self, node , current_code):

        # This is a recursive function which assigns 0 to left hand edge of node
        # and 1 to  right hand edge of node

        if node == None:
            return
        
        if( node.char != None):
            self.codes[node.char] = current_code
            self.reverse_codes[current_code] = node.char

        self.make_codes_helper( node.left , current_code+"0")
        self.make_codes_helper( node.right , current_code+"1")


    def make_codes(self):

        #make codes for characters and save

        root = heapq.heappop(self.heap)
        current_code = ""
        self.make_codes_helper(root , current_code )

    def get_encoded_text(self, text):

        #replace characters with code and return
        
        encoded_text = ""
        for character in text:
            encoded_text += self.codes[character]
        
        return encoded_text

    def pad_encoded_text(self, encoded_text):

        #pad encoded text and return

        extra_padding = 8 - len(encoded_text) % 8

        for i in range(extra_padding):
            encoded_text += "0"

        #adds extra 0's to encoded text so that total number of bits
        #is multiple of 8

        padded_info = "{0:08b}".format(extra_padding)

        # storing the number of extra bits added in a string padded_info
        # in the form binary and converting it into 8 bits

        # if 3 extra bits are stored it converts into binary as 11 and adds
        # 6 o's at start make it 00000011 and store padded info 

        encoded_text = encoded_text + padded_info

        return encoded_text

    def get_byte_array(self, padded_encoded_text):

        #convert bits into byte array and return it

        b = bytearray()

        for i in range(0, len(padded_encoded_text), 8):
            byte = padded_encoded_text[i:i+8]

            b.append(int(byte,2))

            # here byte is a string of  8 bits and converts that 8 bit binary number into integer 
            # and adds into bytearray b

        return b

    def compress(self):
        filename , file_extension = os.path.splitext(self.path)
    
    #os.path.splitext() function seperates path string into two diff strings( i.e., path , path format)
    #os.path.splitext('/computer/c/file.txt') is seperated as '/computer/c/file' + '.txt'

        output_path = filename + ".bin"

        with open(self.path , 'r') as file , open(output_path , 'wb') as output:

            text = file.read()
            text = text.rstrip()

            frequency = self.make_frequency_dict(text)

            self.make_heap(frequency)

            self.merge_codes()

            self.make_codes()

            encoded_text = self.get_encoded_text(text)
            padded_encoded_text = self.pad_encoded_text(encoded_text)

            b = self.get_byte_array(padded_encoded_text)

            output.write(bytes(b))

        print("Compressed")
        return output_path
    

    def remove_padding(self , bitstring):

        #removes padding and gives encoded text back
        
        padded_info = bitstring[:8]

        #padded_information is stored in fr=irst 8 bits of  bitstring

        extra_padding = int(padded_info,2)

        #convert the padded info which is in binary form into integer gives innteger
        #value of how many extra padded bits are there at end

        bitstring = bitstring[8:]

        #remove the first 8 padded info bits
        encoded_text = bitstring[: -1*extra_padding]

        #remove the extra no of bits from end

        return encoded_text
    
    def decode_text(self , encoded_text):

        #gives decoded text

        current_code = ""
        decoded_text = ""

        for bit in encoded_text:
            current_code += bit
            if(current_code in self.reverse_codes):
                character = self.reverse_codes[current_code]
                decoded_text += character
                current_code =""
        
        return decoded_text

    def decompress(self, input_path):

        filename , file_extension = os.path.splitext(self.path)

        output_path = filename + "_decompressed" + ".txt"

        with open(input_path , 'rb' )  as file, open(output_path , 'w') as output:

            bit_string = ""
            byte = file.read(1)

            # this takes first byte from bytearray

            while(len(byte)>0):

                byte = ord(byte)    #gives ascii of integer

                bits = bin(byte)[2:].rjust(8 , "0")

                # converts the integer into binary and adjusting its length to 8 by 
                # inserting 0's at start

                #[2:] is used because while converting into binary it gives code as Ob001..
                # to remove first two letters 0b we used [2:]

                bit_string += bits
                byte = file.read(1)
 
                #reads another byte from bytearray and continues till len(byte) >0

            encoded_text = self.remove_padding(bit_string)
            decoded_text = self.decode_text(encoded_text)

            output.write(decoded_text)

        print("Decompressed")
        return output_path

h = Huffman("C:\Aditya's Files\Projects\HuffmanCoding Algorithm\py impl\sample.txt")
h.compress()
h.decompress("C:\Aditya's Files\Projects\HuffmanCoding Algorithm\py impl\sample.bin")

