# this class does the loading of all the functioall unit of the computer organisation
# function to load the cpu
import sys,parser,argparse,memory,cpu
prs = argparse.ArgumentParser(description='MIPS Sub-Instruction set simulator..')
prs.add_argument('instruction',help='the path to the instruction to be loaded')
prs.add_argument('config',help='the configuration file for the simulator')
prs.add_argument('memory',help='the initial memory value')
argum = prs.parse_args()
instr = argum.instruction
config = argum.config
data = argum.memory
myParser = parser.functionalParser(instr,config,data)
icacheBlocks,icacheBlockSize = myParser.icacheInfo()
memoryData =myParser.loadInitialMemoryData()
memory =structure.Memory(memoryData,icacheBlocks,icacheBlockSize);
instructions = myParser.loadInstructions();
instructionSet = myParser.getInstructionSet();
processor = cpu.CPU(memory,instructions,instructionSet,myParser.adderSize,multiplierSize,dividerSize)
		
class Instruction(object):
	"""docstring for Instruction"""
	def __init__(self,command, first,second,third,location):
		self.command = command
		self.first = first
		self.second = second
		self.third = third
		self.location= location #location is the memory location of the instruction at hand
	
	def execute(self,state):
		"""this function checks executes the instruction the current instruction"""