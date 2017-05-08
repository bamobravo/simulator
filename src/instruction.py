# the class to emulate an instruction 
# it will contain the instruction along side with the operand and also the 
class Instruction(object):
	"""docstring for Instruction"""
	def __init__(self, command,operands):
		self.command = command
		self.operands = operands
	
	# context will contain the memory object, the register status
	def execute(self,context):
		pass