import csv
import os
from config import *

from ghidra.app.script import GhidraScript
from ghidra.util.task import ConsoleTaskMonitor
from ghidra.app.decompiler import DecompileOptions, DecompInterface
from ghidra.program.model.pcode import PcodeOp
from ghidra.app.util.exporter import Exporter
from com.google.security.binexport import BinExportExporter
from java.io import File


function_list = []
program_name = currentProgram.getName()
path = currentProgram.getExecutablePath()
listing = currentProgram.getListing()
func_manager = currentProgram.getFunctionManager()
internal_fcn_objs = func_manager.getFunctions(True)


addr_set = currentProgram.getMemory()
f = File(BINDIFF_EXPORT_PATH + currentProgram.getExecutableMD5() + '.BinExport')
exporter = BinExportExporter() #Binary BinExport (v2) for BinDiff
exporter.export(f, currentProgram, addr_set, monitor)


for fun_obj in internal_fcn_objs:
    fun_name = fun_obj.getName()
    min_addr = fun_obj.getBody().getMinAddress().getOffset()
    function_list.append([path, fun_name, min_addr])


with open(os.path.join(GHIDRA_FUNCTION_DATA_PATH, SAMPLE_FUNCTION_ADDRESS_CSV), 'a') as f:
    writer = csv.writer(f)
    writer.writerows(function_list)
