# this class does the loading of all the functioall unit of the computer organisation
# function to load the cpu
import sys,parser,argparse,memory,cpu,functionalunit



prs = argparse.ArgumentParser(description='MIPS Sub-Instruction set simulator..')
prs.add_argument('instruction',help='the path to the instruction to be loaded')
prs.add_argument('config',help='the configuration file for the simulator')
prs.add_argument('memory',help='the initial memory value')
prs.add_argument('output',help='the file to save the result to')
argum = prs.parse_args()
instr = argum.instruction
config = argum.config
data = argum.memory
out = argum.output
myParser = parser.functionalParser(instr,config,data)
icacheBlocks,icacheBlockSize = myParser.icacheInfo()
memoryData =myParser.loadInitialMemoryData()
memory =memory.Memory(memoryData,icacheBlocks,icacheBlockSize);
instructions = myParser.loadInstructions();
instructionSet = myParser.getInstructionSet();
adder = functionalunit.FunctionalUnit('adder',myParser.adderSize,myParser.adderCycle)
multiplier = functionalunit.FunctionalUnit('multiplier',myParser.multiplierSize,myParser.multiplierCycle)
divider = functionalunit.FunctionalUnit('divider',myParser.dividerSize,myParser.dividerCycle)
processor = cpu.CPU(memory,instructions,instructionSet,adder,multiplier,divider,myParser.labels,out)
processor.start()