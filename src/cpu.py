class CPU(object):
	
	def __init__(self,memory,instruction,InstructionSet):
		self.memory = memory
		self.InstructionSet = InstructionSet
		self.rRegister =[]
		self.fRegister =[]
		self.registerCount=32
		self.instruction = instruction
		# create the registers and initialise the value to perform operation
		for x in range(1,33):
			rRegister.append({'R'+str(i):0})
			fRegister.append({'F'+str(i):0})

		#create the four stages in the application and increase the count of each of these pipeline stages
		#initialise all the four stage into zero, the value in all the stage signifies the amount of cycle taken

	def start(instr,config,data):
	
	# this is the function that will save the necessary information into the output file	
	def profile(self,instruction):
		info= self.execute()
		# the executed instruction must return the address of the nexet instruction

	def bin2dec(self,value):
		return int(value,2)

	def dec2bin(self,value,length=False):
		result ='{0:b}'.format(value)
		if length!=False and len(result) < len:
			extra = length -len(result)
			result=('0' * extra)+result
		return result
		
	
											