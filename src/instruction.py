# the class to emulate an instruction 
# it will contain the instruction along side with the operand and also the 
class Instruction(object):
	"""docstring for Instruction"""
	def __init__(self, command,operands,label):
		self.command = command
		self.operands = operands
		self.label =label
	
	# context will contain the memory object, the register status, the instruction 
	def execute(self,context):
		register = context['rRegister'] if self.command.find('.D')==-1 else context['fRegister']
		firstOperand = self.operands[0]
		secondOperand = self.operands[1]
		thirdOperand = self.operands[2]
		#save the completion time for all the unit in a functional unit
		if self.command =='ADD.D':
			register[firstOperand]=register[secondOperand] + register[thirdOperand]
			return context['functional']['adder'].cycle
		if self.command =='SUB.D':
			register[firstOperand]=register[secondOperand] - register[thirdOperand]
			return context['functional']['adder'].cycle
		if self.command =='DIV.D':
			register[firstOperand]=register[secondOperand] / register[thirdOperand]
			return context['functional']['divider'].cycle

		if self.command=='MUL.D':
			register[firstOperand]=register[secondOperand] * register[thirdOperand]
			return context['functional']['multiplier'].cycle

		if self.command =='DADDI':
			register[firstOperand]=register[secondOperand] + int(thirdOperand)
			return context['functional']['adder'].cycle/2

		if self.command =='DADD':
			register[firstOperand]=register[secondOperand] + register[thirdOperand]
			return context['functional']['adder'].cycle/2

		if self.command =='DSUB':
			register[firstOperand]=register[secondOperand] - register[thirdOperand]
			return context['functional']['adder'].cycle/2

		if self.command =='DSUBI':
			register[firstOperand]=register[secondOperand] + thirdOperand
			return context['functional']['adder'].cycle/2

		if self.command =='AND':
			register[firstOperand]=register[secondOperand] and register[thirdOperand]
			return 1

		if self.command =='OR':
			register[firstOperand]=register[secondOperand] or register[thirdOperand]
			return 1

		
		
