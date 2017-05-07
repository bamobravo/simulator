# contains functionalities for parsing the instruction and the configuration file
class functionalParser(object):
	"""docstring for functionalParser"""
	def __init__(self,instructionFile,configFile,data):
		self.instructionFile = instructionFile
		self.configFile = configFile
		self.dataFile = data

	def parseInstruction(self):
		# this function parses instruction in the file and report in case or error
		content = loadFile(self.configFile)
		result=[]
		instr = content.split('\n');
		for index,ins in enumerate(instr):
			col.trim()
			col = ins.split(' ')
			# search for the needed to be sure the command is one of the instruction
			if not isValidInstruction(col):
				# return an error displaying the line number that is an invalid instruction
				raise Exception('syntax error on line '+(index+1))
			# the instruction is valid until this place so load build the instruction object and add it to the list
			tempInstruction = Instruction(tuple(col))

	def icacheInfo(self):
		try:
			return self.icacheBlock,self.icacheSize
		except Exception as e:
			self.loadFunctionalFileInfo()
			return self.icacheBlock,self.icacheSize
		

	def loadFunctionalFileInfo(self):
		content = self.loadFile(self.configFile);
		items = content.strip().split("\n")
		for item in items:
			startpos = item.index(':')
			startpos+=1
			if item.find("adder")!= -1:
				temp = item[startpos:].strip().split(',')
				self.adderCycle = int(temp[0])
				self.adderSize = int(temp[1])
			elif item.find("Multiplier")!= -1:
				temp = item[startpos:].strip().split(',')
				self.MultiplierCycle = int(temp[0])
				self.MultiplierSize = int(temp[1])
			elif item.find("divider") != -1:
				temp = item[startpos:].strip().split(',')
				self.dividerCycle = int(temp[0])
				self.dividerSize = int(temp[1])
			elif item.find("I-Cache")!= -1:
				temp = item[startpos:].strip().split(',')
				self.icacheBlock = int(temp[0])
				self.icacheSize = int(temp[1])

	def isValidInstruction(self,inst):
		# need a  list of all the valid istruction and the number of operands
		instruction = self.findInstruction(inst)
		if instruction==None:
			return False
		return (instruction['operand'] +1)==len(inst) 
		
		# loads the configuration needed for the cpu,this function return the starting memory state for the cpu also		
	def getCPUParam(self,filename):
		'return a tuple that contains the information needed by the cpu object'
		content = self.loadFile(filename)
		config = content.split('\n')
		for index,con in enumerate(config):
			result = con.split(' ')
			return tuple(result)

	def loadFile(self,filename):
		file = open(filename,'r')
		content = file.read()
		file.close()
		return content

	def getInstructionSet(self,filename=''):
		if self.instructionSet == None:
			self.instructionSet = self.buildInstructionSet(filename)
		return self.instructionSet

	def findInstruction(self,instructionName):
		for inst in self.instructionSet:
			if inst['name']==instructionName:
				return inst
		return None

	def buildInstructionSet(filename):
		#create a list of dictionaries containing the instruction set and the properties
		dict = [{'name':'HLT','execute':0,'completionStage':'Issue','operand':0}]
		dict.append({'name':'J','execute':0,'completionStage':'Issue'})
		dict.append({'name':'BEQ','execute':0,'completionStage':'Read'})
		dict.append({'name':'BNE','execute':0,'completionStage':'Read'})
		dict.append({'name':'DADD','execute':1,'completionStage':'Execute'})
		dict.append({'name':'DADDI','execute':1,'completionStage':'Execute'})
		dict.append({'name':'DSUB','execute':1,'completionStage':'Execute'})
		dict.append({'name':'DSUBI','execute':1,'completionStage':'Execute'})
		dict.append({'name':'AND','execute':1,'completionStage':'Execute'})
		dict.append({'name':'ANDI','execute':1,'completionStage':'Execute'})
		dict.append({'name':'OR','execute':1,'completionStage':'Execute'})
		dict.append({'name':'ORI','execute':1,'completionStage':'Execute'})
		dict.append({'name':'LI','execute':1,'completionStage':'Execute'})
		dict.append({'name':'LUI','execute':1,'completionStage':'Execute'})
		dict.append({'name':'LW','execute':1,'completionStage':'Execute','isData':True})
		dict.append({'name':'SW','execute':1,'completionStage':'Execute','isData':True})
		dict.append({'name':'LD','execute':2,'completionStage':'Execute','isData':True})
		dict.append({'name':'SD','execute':2,'completionStage':'Execute','isData':True})
		add,sub,mul,div= loadConfigFromFile(filename);
		dict.append({'name':'ADDD','execute':add,'completionStage':'Execute'})
		dict.append({'name':'SUBD','execute':sub,'completionStage':'Execute'})
		dict.append({'name':'MUL','execute':mul,'completionStage':'Execute','isData':True})
		dict.append({'name':'DIV','execute':div,'completionStage':'Execute'})
		return dict

		#function to load the memory information in a way that it can be easily accessed
		def loadInitialMemoryData(self):
			#load all the memory information into a straight array
			content = self.loadFile(data)
			content = content.replace("\n",'')
			return content