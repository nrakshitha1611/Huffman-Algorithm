# Huffman Coding in Python

A simple Python implementation of the Huffman Coding algorithm for file compression and decompression.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Usage](#usage)
- [Customization](#customization)

## Overview

This script (`Huffman.py`) implements the Huffman Coding algorithm to compress text files into a binary format and decompress them back to their original form. It follows these steps:

1. Read the input text file and build a frequency dictionary.
2. Construct a Huffman tree based on character frequencies.
3. Generate binary codes for each character.
4. Encode the text into a padded bit string and write it to a `.bin` file.
5. Read the binary file, remove padding, and decode the bit string to reconstruct the original text.

## Features

- Frequency dictionary generation
- Huffman tree construction with priority queue (`heapq`)
- Code generation and reverse lookup
- Bit-level encoding, padding, and byte array conversion
- File compression (`.bin`) and decompression back to text

## Prerequisites

- Python 3.x  
- No external libraries required; uses only built-in modules (`os`, `heapq`).

## Usage

1. **Clone the repository**
    ```bash
    git clone https://github.com/nrakshitha1611/Huffman-Algorithm.git
    cd Huffman-Algorithm
    ```

2. **Configure file paths**  
   At the bottom of `Huffman.py`, update the `input_path` and (optional) `output_path`:
    ```python
    if __name__ == "__main__":
        input_path = "path/to/your/input.txt"
        h = Huffman(input_path)
        compressed_path = h.compress()
        h.decompress(compressed_path)
    ```

3. **Run the script**
    ```bash
    python Huffman.py
    ```
    This will produce:
    - `input.bin` &rarr; compressed binary file  
    - `input_decompressed.txt` &rarr; decompressed text output

## Customization

To accept command-line arguments instead of hard-coded paths, you can add at the bottom of `Huffman.py`:
```python
import sys

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python Huffman.py <input_file>")
        sys.exit(1)
    input_path = sys.argv[1]
    h = Huffman(input_path)
    compressed_path = h.compress()
    h.decompress(compressed_path)
