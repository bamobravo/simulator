class CPU(object):
	
	def __init__(self,memory,cache):
		self.memory = memory
		self.InstructionSet = self.buildInstuctionSet()
		#create the four stages in the application and increase the count of each of these pipeline stages
		#initialise all the four stage into zero, the value in all the stage signifies the amount of cycle taken

	def buildInstructionSet(filename):
		#create a list of dictionaries
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

		
	def profile(self,instruction):
		info= self.execute()
		# the executed instruction must return the address of the nexet instruction
	
	def execute(self,instruction):
		# get the command and the operand
		command = instruction[0]
		
	
											