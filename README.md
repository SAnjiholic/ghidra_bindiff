# ghidra bindiff

bindiff using ghidra decompiler

needs:
- python3
- bindiff
- Ghidra
- Ghidra binexport plugin

how to use?:
 1. install bindiff, Ghidra and Ghidra plugin(binexport)
    > [bindiff](https://www.zynamics.com/bindiff.html)
    > [ghidra](https://ghidra-sre.org/)
    > [ghidra plugin(binexport)](https://github.com/google/binexport)
 2. Enter the path to ghidra headless and bindiff in your config file.
 3. python run.py binary1_path, binary2_path