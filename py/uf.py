import random
from datetime import datetime

class UF(object):
	def __init__(self, count):
		"""
			Initializes ids. Todo: Use array instead and benchmark
		"""
		self.union_ids = [i for i in xrange(count)]

	def find(self, one, two):
		return self.union_ids[one] == self.union_ids[two]


	def union(self, one, two):

		common_id = self.union_ids[one]
		two_id = self.union_ids[two]
		if common_id == two_id:
			return
		for i, union_id in enumerate(self.union_ids):
			if union_id == two_id:
				self.union_ids[i] = common_id

		
	def __repr__(self):
		return "{}: {}".format(self.__class__, self.union_ids)			
	
class UFTree(UF):

	def find(self, one, two):
		return self.root(one) == self.root(two)

	def root(self, pos, need_depth=False):
		up_count = 1
		up = self.union_ids[pos]
		while up != self.union_ids[up]:
			up_count += 1
			up = self.union_ids[up]

		if not need_depth:
			return up
		else:
			return (up, up_count)

	def union(self, one, two):
		root_one, root_two = self.root(one), self.root(two)
		self.union_ids[root_two] = root_one

	def depth_info(self):
		length = len(self.union_ids)
		depths = [None for i in xrange(length)]
		for i in xrange(length):
			root, depth = self.root(i, need_depth=True)
			depths[i] = depth

		return depths

		
class WeightedTree(UFTree):
	def __init__(self, count):
		UFTree.__init__(self, count)
		self.root_sizes = [1 for i in xrange(count)]

	def union(self, one, two):
		root_one, root_two = self.root(one), self.root(two)
		if root_one == root_two:
			return
		if self.root_sizes[root_one] >= self.root_sizes[root_two]:
			self.union_ids[root_two] = root_one
			self.root_sizes[root_one] += self.root_sizes[root_two]
		else:
			self.union_ids[root_one] = root_two
			self.root_sizes[root_two] += self.root_sizes[root_one]


class UFHash(object):

	def __init__(self, count):
		self.union_ids = [None] * count
		for i in xrange(count):
			self.union_ids[i] = i

		self.member_groups = {}
		for i in xrange(count):
			self.member_groups[i] = {i: i}


	def find(self, one, two):
		return self.union_ids[one] == self.union_ids[two]

	def union(self, one, two):
		common_id = self.union_ids[one]
		two_id = self.union_ids[two]
		if common_id == two_id:
			return
		#import ipdb;ipdb.set_trace()
		for member in self.member_groups[two_id]:
			self.member_groups[common_id][member] = member
			self.union_ids[member] = common_id

		del self.member_groups[two_id]

	def __repr__(self):
		return "UFHash: {}".format(self.member_groups)

def test(obj, count):
		print "Started test", count
		start = datetime.now()
		upto = count/2;
		for i in xrange(upto):
			one = random.randint(0, count-1)
			two = random.randint(0, count -1)
			#print "Percentage completed: {}".format(i*100.0/upto)
			obj.union(one, two)
			result = obj.find(one, two)
			assert(result)
		end = datetime.now()
		print "Done"
		return (end - start).total_seconds()

def run():

	"""
		Initializing objects because it takes more time for larger numbers
	"""
	counts = [int(pow(10, i)) for i in xrange(1, 4)]																																																																																																																																																																																																																														
	results = {}
	for count in counts:
		uf_tree = UFTree(count)
		uf_hash = UFHash(count)
		uf_weighted_tree = WeightedTree(count)
		results[count] = {}
		print "Started ", count
		tree_result = test(uf_tree, count)
		hash_result = test(uf_hash, count)
		weighted_result = test(uf_weighted_tree, count)
		print "Done ", count
		results[count]['hash'] = hash_result
		results[count]['tree'] = tree_result
		results[count]['weighted_tree'] = weighted_result

	return results
	






