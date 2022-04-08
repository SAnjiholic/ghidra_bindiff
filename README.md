# ghidra bindiff

bindiff using ghidra decompiler

needs:
- python3
- Ghidra
- Ghidra binexport plugin

how to use?:
 1. install Ghidra and Ghidra plugin(binexport)
    > [ghidra](https://ghidra-sre.org/)
    > [ghidra plugin(binexport)](https://github.com/google/binexport)
 2. Enter the path to ghidra headless in your config file.
 3. python run.py binary1_path, binary2_path