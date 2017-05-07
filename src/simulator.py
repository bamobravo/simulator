# this class does the loading of all the functioall unit of the computer organisation
# function to load the cpu
import sys,parser,argparse,structure
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


def loadCPUUnit(filename):
	# pass the filename into a dictionary object and then pass the object into 
	#into a class constructor to create the dobject
	parse = functionalParser(filename)
	cpuParam = parse.getCpuParam()#includes the cache information too
	cpu = getCPU(cpuParam)
	return cpu

def getCPU():
	#load information about the function unit and load the class that can be called on the cpu
	pass

class CPU(object):
	"""this class contains the all the information needed to be used by the cpu that will help in 
	performing the necessary simulation"""
	# add code pointer that points to the next instruction to be executed
	def __init__(self,address):
		self.ip = address
		self.cp =0 #set this to an arbitrary value

	def setNextInstruction(self,address):
		self.cp = address
		
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