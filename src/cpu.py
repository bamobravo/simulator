class CPU(object):
	
	def __init__(self,memory,instruction,InstructionSet,adderUnit,mulUnit,divUnit,labels,outFile):
		self.memory = memory
		self.InstructionSet = InstructionSet
		self.pc =0
		self.ip=0
		self.outputFile=outFile
		self.rRegister ={}
		self.fRegister ={}
		self.registerCount=32
		self.instruction = instruction
		self.hasHalt=False
		self.profileInformation=[]
		self.adder = adderUnit
		self.multiplier = mulUnit
		self.divider = divUnit
		self.labels= labels
		# create and initialise all the register and the corresponding register value
		# use a stack for the completion time issue
		for i in range(1,33):
			self.rRegister['R'+str(i)]=0
			self.fRegister['F'+str(i)]=0

	def start(self):
		'execute the instruction and returns the cpu profile information'
		context = self.createContext()
		previousValues=self.createEmptyValues()
		previousInstruction = None
		while not self.hasHalt:
			stall =0 # the value for monitoring stalling
			currentValues=self.createEmptyValues()
			currentInstruction,fetchCycle = self.fetchInstruction(previousInstruction,previousValues,currentValues)#retun the instruction and the time taken
			currentValues['fetch']=fetchCycle
			if currentInstruction.command=='HLT':
				temp = self.combineProfileData(currentInstruction,fetchCycle,'','','','','','','')
				self.profileInformation.append(temp)
				break
			#create a context for each of the execution and pass the context to all the pipeline stage function
			struct,issueCycle,hasHalt = self.issueInstruction(currentInstruction,previousInstruction,previousValues,currentValues) # the step depend on each other
			currentValues['issue']=issueCycle
			readCycle = self.read(currentInstruction,previousInstruction,previousValues,currentValues)
			currentValues['read']=readCycle
			execCycle,raw,waw,struct = self.execute(currentInstruction,previousInstruction,previousValues,currentValues,struct)
			currentValues['execute']=execCycle
			writeCycle =self.write(currentInstruction,previousInstruction,previousValues,currentValues)
			currentValues['write']=writeCycle
			previousValues= currentValues
			previousInstruction=currentInstruction
			temp = self.combineProfileData(currentInstruction,fetchCycle,issueCycle,readCycle,execCycle,writeCycle,waw,raw,struct)
			self.profileInformation.append(temp)

		self.profile()

	def createEmptyValues(self):
		"function to initialize the new profile value for the next set of "
		previousValues={}
		previousValues['fetch']=None
		previousValues['issue']=None
		previousValues['read']=None
		previousValues['execute']=None
		previousValues['write']=None
		return previousValues

	def createContext(self):
		"this function create the context each execution unit, the context contain register information"
		result={}
		result['memory']=self.memory
		result['fRegister']= self.fRegister
		result['rRegister']= self.rRegister
		result['functional']= {'adder':self.adder,'multiplier':self.multiplier,'divider':self.divider}
		return result

	def fetchInstruction(self,previousInstruction,previous,current):
		'the function simulation the fetch instruction pipiline stage, the function returns the instruction'
		# halt = False

		index,cycleCount=self.memory.fetch('instruction',self.pc,1)
		self.ip = self.pc
		self.pc+=1
		extra = (0 if previous['fetch']==None else previous['fetch'])
		result = cycleCount+extra
		if previousInstruction!=None and previous['fetch']+1 < previous['issue'] and result < previous['issue']:
			result = previous['issue']
		return self.instruction[index],result

	def issueInstruction(self,instruction,previousInstruction,previous, current):
		halt = False
		if instruction.command=='HLT':
			return '','',''
			halt = True
		if previousInstruction!=None and instruction.command==previousInstruction.command:
			if previous['write'] + 1 < current['fetch']:
				return 'N',current['fetch']+1,halt
			return 'Y',previous['write'] + 1,halt
		else:
			return 'N',current['fetch']+1,halt

	def read(self,instruction,previousInstruction,previous,current):
		if instruction.command=='HLT':
			return ''
		if instruction.command=='LI':
			return current['issue'] + 1;
		return current['issue'] + 1
		
	def execute(self,instruction,previousInstruction,previous,current,struct ='N'):
		if instruction.command=='HLT':
			return '','','',''
		instructionInfo = self.getInstructionInformation(instruction.command)
		if instructionInfo==None:
			raise Exception("unsupported operation")
		if instruction.command=='LI':
			self.rRegister[instruction.operands[0]]=int(instruction.operands[1])
			return current['read'] +1,'N','N',struct
		if instruction.command=='L.D':
			temp = instruction.operands[1].split('(')
			num = temp[0]
			reg = int(self.rRegister[temp[1][0:len(temp[1])-1]])
			address = int(num) + reg
			data,cycle =self.memory.fetch('data',address,2)#load double word from memory
			self.fRegister[instruction.operands[0]]=self.bin2dec(data)
			return current['read'] +cycle,'N','N',struct
		# treat each instruction category differently
		#you have to include information about the structural unit in the calculation
		if instructionInfo['type'] =='Arithmetic' or instructionInfo['type'] =='Logical':
			#check for likely data hazard
			extra = 0;
			# also check for structural hazard
			fUnit = self.getFunctionalUnit(instruction)
			hazard,raw,war = self.isDataHazard(previousInstruction,instruction)
			structOccured,minValue  = fUnit.isHazard(previous['read'])
			struct = 'Y' if structOccured else 'N'
			if structOccured:
				pass
			dataExectTime = 0
			if hazard:
				pass
				# dataExectTime = 
				# need to stall when data hazard occurs increase the value of extra based on some condition
				# remember there are different functional unit 
			context = self.createContext()
			cycle= instruction.execute(context)
			print cycle
			usedTime = current['read']+dataExectTime+cycle
			return usedTime,raw,war,struct
		elif instructionInfo['type']=='Control':
			usedTime = previous['read'] + 1
			if instruction.command=='J':
				self.pc = self.labels[instruction.operands[0]]
			elif instruction.command=='BNE':
				if self.rRegister[instruction.operands[0]]!=self.rRegister[instruction.operands[1]]:
					self.pc = self.labels[instruction.operands[2]] 
			elif instruction.command=='BEQ':
				if self.rRegister[instruction.operands[0]]==self.rRegister[instruction.operands[1]]:
					self.pc = self.labels[instruction.operands[2]] 
			return usedTime,'N','N','N'

	def getFunctionalUnit(self,instruction):
		instructionType = instruction.command
		if instructionType.find('ADD')!=-1 or instructionType.find('SUB')!= -1:
			return self.adder
		elif instructionType.find('MUL')!= -1:
			return self.multiplier
		elif instructionType.find('DIV')!= -1:
			return self.divider
		else:
			return None

	def isDataHazard(self,previous,current):
		#check if the previous instruction contains operand in the next instruction
		# also determine if it is WAR OR RAW
		raw='N'
		war ='N'
		result = False
		for i,cur in enumerate(current.operands):
			try:
				index = previous.operands.index(cur)
				if index!=-1:
					result = True
					if i==0 and index!=0:
						raw='Y'# the current instruction tries to use loaction of the first instruction
					if index==0 and i!=0:
						war='Y'
			except Exception as e:
				continue
			
		return result,raw,war

	def write(self,instruction,previousInstruction,previous,current):
		# if instruction.command=='LI':
		# 	return current['execute'] +1
		if instruction.command=='HLT':
			return ''
		return current['execute']+1

	def combineProfileData(self,instruction,fetch,issue,read,execute,write,waw,raw,struct):
		'create account profiling information for display as a form of dictionary'
		result = {}
		result['instruction']=self.stringifyInstruction(instruction)
		result['fetch']=fetch
		result['issue']=issue
		result['read']=read
		result['execute']=execute
		result['write']=write
		result['waw']=waw
		result['raw']=raw
		result['struct']=struct
		return result
	#the function to turn an instruction into a string for display purpose
	def stringifyInstruction(self,instruction):
		'build a string that can be used for output for the instruction'
		result='' if instruction.label==None else instruction.label+': '
		result+=instruction.command
		if len(instruction.operands) > 0:
			temp = ','.join(instruction.operands)
			result+=' '+temp
		return result
	def getInstructionInformation(self,command):
		for instruction in self.InstructionSet:
			if instruction['name'] ==command:
				return instruction
		return None

	def bin2dec(self,value):
		return int(value,2)

	def dec2bin(self,value,length=False):
		result ='{0:b}'.format(value)
		if length!=False and len(result) < len:
			extra = length -len(result)
			result=('0' * extra)+result
		return result

	def profile(self):
		"output the information into a file"
		data = self.getOutputInformation()
		print data
		file = open(self.outputFile,'w')
		file.write(data)
		file.close()

	def getOutputInformation(self):
		"format the profiling information from the cpu execution"
		content ="Instruction	Fetch 	Issue 	Read 	Exec 	Write 	RAW 	WAW 	Struct\n"
		for item in self.profileInformation:
			content+="{!s} 	{!s} 	{!s} 	{!s} 	{!s} 	{!s} 	{!s} 	{!s} 	{!s}\n".format(item['instruction'],item['fetch'],item['issue'],item['read'],item['execute'],item['write'], item['raw'],item['waw'],item['struct'])
		# add additional information about the memory information
		content+="\n"
		content+="Total number of access request for instruction cache: "+str(self.memory.iCache.requestCount)
		content+="Number of instruction cache hit: "+str(self.memory.iCache.hitCount)
		content+="Total number of access request for data cache: "+str(self.memory.dCache.requestCount)
		content+="Total number of access request for instruction cache: "+str(self.memory.dCache.hitCount)
		return content
		
	
											