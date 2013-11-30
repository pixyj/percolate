import math
import random
import uf


"""	.	
. . . . .
. . . . .
. . . . .
. . . . .
. . . . . 
    .
    
"""

class Percolation(object):
	def __init__(self, size=50):
		self.size = size
		self.total = size * size + 2
		self.uf_tree = uf.WeightedTree(self.total)
		self.block_status = {}
		for i in xrange(self.total):
			self.block_status[i] = False

		self.block_status[0] = self.block_status[self.total-1] = True


	def unblock(self, position):
		if self.block_status[position]:
			return False

		for i in self.get_neighbours(position):
			if self.block_status[i]:
				self.uf_tree.union(position, i)

		self.block_status[position] = True		
		return True

	def is_connected(self, one, two):
		return self.uf_tree.find(one, two)

	def is_percolated(self):
		return self.uf_tree.find(0, self.total - 1)

	def run_random_simulation(self):
		unblocked_count = 0
		random_order = [i for i in xrange(1, self.total - 1)]
		random.shuffle(random_order)
		for i in random_order:
			self.unblock(i)
			unblocked_count += 1
			if self.is_percolated():
				break

		return unblocked_count * 1.0 / (self.total - 2)



	def _get_virtual_top_neighbours(self):
		return range(1, self.size + 1)

	def _get_virtual_bottom_neighbours(self):
		return range(self.total -1 - self.size, self.total - 1)
		
	def get_neighbours(self, position):
		assert(position >=0 and position < self.total)
		if position == 0:
			return self._get_virtual_top_neighbours()
		if position == self.total - 1:
			return self._get_virtual_bottom_neighbours()

		neighbours = []
		neighbours.extend(self._get_left_neighbours(position))
		neighbours.extend(self._get_right_neighbours(position))
		neighbours.extend(self._get_top_neighbours(position))
		neighbours.extend(self._get_bottom_neigbours(position))
		return neighbours


	def _get_row(self, position):
		if position % self.size == 0:
			return position / self.size - 1

		return position / self.size

	def _get_column(self, position):
		
		if position % self.size == 0:
			return self.size - 1

		return (position % self.size) - 1

	def _get_left_neighbours(self, position):
		if self._get_column(position) == 0:
			return []

		positions = []
		same_row_left = position - 1
		positions.append(same_row_left)
		return positions
		"""
		if self._get_row(position) > 0:
			above_row_left = position - self.size - 1
			positions.append(above_row_left)

		if self._get_row(position) < self.size - 1:
			below_row_left = position + self.size - 1
			positions.append(below_row_left)

		return positions
		"""

	def _get_right_neighbours(self, position):
		if self._get_column(position) == self.size - 1:
			return []

		positions = []
		same_row = position + 1
		positions.append(same_row)
		return positions

		"""
		if self._get_row(position) > 0:
			above_row = position - self.size + 1
			positions.append(above_row)

		if self._get_row(position) < self.size - 1:
			below_row = position + self.size + 1
			positions.append(below_row)

		return positions
		"""

	def _get_top_neighbours(self, position):
		if self._get_row(position) == 0:
			return [0]

		return [position - self.size]


	def _get_bottom_neigbours(self, position):
		if self._get_row(position) == self.size - 1:
			return [self.total - 1]

		return [position + self.size]



def run_simulations(size, times):
	unblocked_ratios = []
	for i in xrange(int(times)):
		p = Percolation(size)
		ratio = p.run_random_simulation()
		unblocked_ratios.append(ratio)
		print "Percentage completed:", i*100.0/times

	return unblocked_ratios


def plot(unblocked_ratios):
	buckets = [0 for i in xrange(100)]
	for i in unblocked_ratios:
		i = int(math.floor(i*100))
		buckets[i] += 1
	return buckets


def run(size=10, times=1000):
	ratios = run_simulations(size, times)
	print "Done simulation"
	buckets = plot(ratios)
	results = ""
	for i, count in enumerate(buckets):
		results += "{},{}\n".format(i, count)

	with open("percolate_{}_{}.csv".format(size, times), "w") as f:
		f.write(results)



if __name__ =="__main__":
	run()