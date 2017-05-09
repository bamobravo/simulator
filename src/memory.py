import time,sys
class Memory(object):
	"""docstring for Cache"""
	def __init__(self,initialData,blocks,blockSize):
		self.data = initialData #the block size of the memory
		self.iCache=Cache('instruction',blocks,blockSize)
		self.dCache = Cache('data',4,4)#this is the cache location that help find the hit

	#fetch this data from the memory and return the number of cycle to perform this
	#if this time is more than one the other value will need to stall
	def fetch(self,fetchType,startAddress,size):#the size will be in block
		block = =1
		if fetchType=='instruction':		
			if  (block=self.iCache.isHit(address))!= -1:
				return address,size #the address is th eindex 
			else:
				return address, size +(self.iCache.blockSize*3)#penalty for cache miss

		elif fetchType=='data':
			if (block=self.dCache.isHit(address))!=-1:
				self.dCache.updateCache(block)
				return dCache.fetch(block,address,size) ,size
			least = iCache.getLeastRecentlyUsed()
			memoryData = self.data[startAddress:startAddress+size]
			iCache.writeToCache(least,startAddress,memoryData)
		return data[startAddress:startAddress+size] size + (self.dCache.blockSize*3)#penalty for cache miss
	


class Cache(object):
	"""docstring for instructionCache"""
	def __init__(self,cacheType,blocks, blockSize):
		self.blocks = []
		for x in range(0,blocks):
			self.blocks.append({'startAddress':None,'time':None,'data':None}) 
		self.blockSize= blockSize
		self.cacheType = cacheType
		self.hitCount=0
		self.requestCount = 0

	def writeToCache(self,index,address,data):
		block =blocks[index]
		block['startAddress']=address
		block['time']=time.time()
		block['data']=data

	def getLeastRecentlyUsed(self):
		min = sys.maxint
		position = -1
		for index,value in enumerate(self.blocks):
			if value['time'] < min:
				position =index
				min = value['time']
		return position

	def isHit(self,fetchType,address,size):
		# use the information about the strategy to perform this operatio and to get work done here
		block = self.findBlock(address,size)
		self.requestCount+=1
		if block!=-1:
			self.hitCount+=1
			self.blocks[block]['time']= time.time()
			return True
		return False

	def findBlock(self,fetchType,address,size):
		for index,block in enumerate(self.blocks):
			if block['startAddress']==None:
				continue
			if self.fetchType =='instruction':
				blockindex = address//self.blockSize
				if blockindex > self.blocks:
					raise Exception('invalid memory location')
				if block['startAddress']==blockindex:
					return index
			else:
				if block['startAddress'] <=address and address <= block['startAddress'] + size:
					return index
		return -1

	def updateCache(self,bl):
		block = self.blocks[0]['time']= time.time()

	def fetch(self,block,address,size):
		data = self.blocks[block]['data']
		return data[address:address+size]
