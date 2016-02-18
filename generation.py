import Queue
import math
import numpy
import scipy
import random
import copy
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import minimum_spanning_tree
import matplotlib.pyplot as plt
import matplotlib.patches as patches

class Colour:
	def __init__(self, colour, xColour, total, lastTouched):
		self.colour = colour
		self.xColour = xColour
		self.total = total
		self.lastTouched = lastTouched

def createRandom():
	colour = ""

	#some colours aren't 6 long, keep getting a number
	while len(colour) != 7:
		"CHOOSE NEW"
		colour = "#%06x" % random.randint(0, 0xFFFFFF)

	return colour

def getParent():
	parent1 = FAMILY[random.randint(0,len(FAMILY)-1)]
	parent2 = FAMILY[random.randint(0,len(FAMILY)-1)]

	if (parent1.total < parent2.total):
		return parent1
	else:
		return parent2

#create two children, choose the strongest one
def crossover(p1,p2):
	c11 = p1.colour[1:4]
	c12 = p1.colour[4:7]

	c21 = p2.colour[1:4]
	c22 = p2.colour[4:7]

	c11Sum = int(c11, 16)
	c12Sum = int(c12, 16)

	if (c11Sum < c12Sum):
		c1 = c11
	else:
		c1 = c12

	c21Sum = int(c21, 16)
	c22Sum = int(c22, 16)

	if (c21Sum < c22Sum):
		c2 = c21
	else:
		c2 = c22

	return "#" + c1 + c2
	

def mutate(c):
	num = random.randint(1,6)
	hexNum = hex(random.randint(0, 15))
	c1 = c[0:num]
	c2 = c[num+1:]
	c = c1 + hexNum[2:] + c2
	return c

def reducePopulation():
	lowestArray = []
	lowest = 1000

	for colour in FAMILY:
		if colour.lastTouched < lowest:
			lowest = colour.lastTouched
			lowestArray = []
			lowestArray.append(colour)
		elif colour.lastTouched == lowest:
			lowestArray.append(colour)

	parent1 = lowestArray[random.randint(0,len(lowestArray)-1)]
	parent2 = lowestArray[random.randint(0,len(lowestArray)-1)]

	if (parent1.total < parent2.total):
		FAMILY.remove(parent2)
	else:
		FAMILY.remove(parent1)

		

def main():

	global FAMILY
	FAMILY = []
	step = 0

	for i in range (1,21):
		c = createRandom()
		xc = c[1:]
		xc = "0x" + xc
		newColour = Colour(c, xc, int(xc, 16), 0)
		FAMILY.append(newColour)


	fig1 = plt.figure()
	ax1 = fig1.add_subplot(111, aspect="equal")
	plt.axis([0,10,0,10])
	
	#set up parents
	for i,c in enumerate(FAMILY):
		ax1.add_patch(patches.Rectangle((i/float(10),0),0.1,0.1,facecolor=c.colour))

	for j in range (1,101):
		#choose parents:
		step += 1
		parent1 = getParent()
		parent2 = getParent()

		parent1.lastTouched = step
		parent2.lastTouched = step

		childColour = crossover(parent1, parent2)

		# 20% chance of mutation
		if random.random() <= 0.2:
			childColour = mutate(childColour)

		xChildColour = childColour[1:]
		xChildColour = "0x" + xChildColour
		newChildColour = Colour(childColour, xChildColour, int(xChildColour, 16), step)
		FAMILY.append(newChildColour)

		reducePopulation()

		for i,c in enumerate(FAMILY):
			ax1.add_patch(patches.Rectangle((i/float(10),j/float(10)),0.1,0.1,facecolor=c.colour))
	
	plt.show()

main()





















