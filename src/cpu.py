class CPU(object):
	
	def __init__(self,memory,instruction,InstructionSet,adderUnit,mulUnit,divUnit):
		self.memory = memory
		self.InstructionSet = InstructionSet
		self.pc =0
		self.ip=0
		self.rRegister =[]
		self.fRegister =[]
		self.registerCount=32
		self.instruction = instruction
		self.hasHalt=False
		self.profileInformation=[]
		self.adder = functionalUnit.FunctionalUnit(adderUnit)
		self.Multiplier = functionalUnit.FunctionalUnit(mulUnit)
		self.division = functionalUnit.FunctionalUnit(divUnit) 
		# create the registers and initialise the value to perform operation
		for x in range(1,33):
			rRegister.append({'R'+str(i):0})
			fRegister.append({'F'+str(i):0})

		#create the four stages in the application and increase the count of each of these pipeline stages
		#initialise all the four stage into zero, the value in all the stage signifies the amount of cycle taken

	def start(self):
		fetchCycle=0
		issueCycle=0
		readCycle=0
		execCycle =0
		writeCycle =0
		while not self.hasHalt:
			currentInstruction,fetchCycle = self.fetchInstruction(fetchCycle)#retun the instruction and the time taken
			issueCycle = self.issueInstruction(currentInstruction,issueCycle)
			readCycle = self.read(currentInstruction.readCycle)
			execCycle = self.execute(currentInstruction,executeCycle)
			writeCycle =self.executeWrite(currentInstruction,writeCycle)
			


	def fetchInstruction(self):
		self.memory.fetch('instruction',self.pc,1)
	# this is the function that will save the necessary information into the output file	
	def profile(self,instruction):
		data = self.getOutputInformation()
		file = open(self.outputFile,'w')
		file.write(data)
		file.close()
		
	def getOutputInformation(self):
		content ='Instruction	Fetch 	Issue 	Read 	Exec 	Write 	RAW 	WAW 	Struct'
		for item in self.profileInformation:
			content+="{!s} 	{!s} 	{!s} 	{!s} 	{!s} 	{!s} 	{!s} 	{!s} 	{!s}\n".format(item.instruction,item.fetch,item.issue,item.read,item.execute,item.write, item.raw,item.waw,item.struct)
		# add additional information about the memory information
		content+="\n"
		content+="Total number of access request for instruction cache: "+self.memory.iCache.requestCount
		content+="Number of instruction cache hit: "+self.memory.iCache.hitCount
		content+="Total number of access request for data cache: "+self.memory.dCache.requestCount
		content+="Total number of access request for instruction cache: "+self.memory.dCache.hitCount
		return content

	def bin2dec(self,value):
		return int(value,2)

	def dec2bin(self,value,length=False):
		result ='{0:b}'.format(value)
		if length!=False and len(result) < len:
			extra = length -len(result)
			result=('0' * extra)+result
		return result
		
	
											