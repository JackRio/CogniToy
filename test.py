"""Build in python function https://docs.python.org/3/library/functions.html"""


# 1
# def findFactors():
# 	'''
# Divisible by 7 and not multiple of 5
# 	'''
# 	l = []
# 	for i in range(2000,3201):
# 		if (i%7 == 0) and (i%5 != 0):
# 			l.append(str(i))
# 	print(','.join(l))
# print(findFactors.__doc__)
# findFactors()

# 2
"""
Print Output in tuple and list form
"""
# values = input()
# l = values.split(',')
# t = tuple(l)
# print(l)
# print(t)

# 3
'''
Printing matrix form
'''
# value = input("Enter row and column")
# values = [int(x) for x in value.split(',')]
# r = values[0]
# c = values[1]

# matrix = [[0 for col in range(r)]for row in range(r)]

# for row in range(r ):
# 	for col in range(c):
# 		print(row,col)
# 		matrix[row][col] = row * col

# print(matrix)


# 4
"""
String sorting
"""
# items = [x for x in input().split(',')]
# items.sort()
# print(','.join(items))

# 5
"""
Captilizing lines
"""
# inputs = [x for x in input().split(',')]
# for c in inputs:
# 	print(''.join(c.upper()))

# lines = []
# while True:
# 	s = input()
# 	if s:
# 		lines.append(s.upper())
# 	else:
# 		break
# for sentence in lines:
# 	print(sentence)

# 6
"""
Printing words after sorting and removing repeating words
"""
# inputs = [x for x in input().split(' ')]
# print(' '.join(sorted(list(set(inputs)))))

# 7
"""
Binary number arithmetic
"""
# values = [x for x in input().split(',')]
# item = []
# for x in values:
# 	intp = int(x,2)
# 	if not intp%5:
# 		item.append(x)

# print(','.join(item))


# 8
'''
Printing numbers which have all digit even
'''
# even = []
# for x in range(1000,3001):
# 	i = str(x)
# 	if (int(i[0])%2 == 0 and int(i[1])%2 == 0 and int(i[2])%2 == 0 and int(i[3])%2 == 0):
# 		even.append(i)
# print(','.join(even))

# 9
# import re

# def passwordCheck():
# 	'''
# 	Password checking code
# 	'''
# 	passw = []
# 	inputs = [x for x in input().split(',')]
# 	for password in inputs:
# 		if len(password) < 6 or len(password) > 12:
# 			continue
# 		else:
# 			pass
# 		if not re.search('[a-z]',password):
# 			continue
# 		elif not re.search("[0-9]",password):
# 			continue
# 		elif not re.search('[A-Z]',password):
# 			continue
# 		elif not re.search('[#$@]',password):
# 			continue
# 		elif re.search('\\s',password):
# 			continue
# 		else:
# 			pass
# 		passw.append(password)
# 	print(','.join(passw))

# print(passwordCheck.__doc__)
# passwordCheck()

# 10
# from operator import itemgetter, attrgetter
# def sortMultipleCondition():
# 	'''
# 	Sorting based on 3 different keys from the input
# 	The priority is that name > age > score.
# 	Sorting based on above criteria
# 	'''
# 	l = []
# 	while True:
# 	    s = input()
# 	    if not s:
# 	        break
# 	    l.append(tuple(s.split(",")))

# 	l = list(sorted(l, key=itemgetter(0,1,2)))
# 	for x in l:
# 		print(x)

# print(sortMultipleCondition.__doc__)
# sortMultipleCondition()

# 11
# def putNumbers(n):
#     i = 0
#     while i<n:
#         j=i
#         i=i+1
#         if j%7==0:
#             yield j

# for i in putNumbers(100):
#     print(i)

# 12
# def countfrequency():
# 	"""
# 	Count frequency of words in the sentence and sort them alphanumerically
# 	"""
# 	freq = {}
# 	inputs = [x for x in input().split(' ')]
# 	for words in inputs:
# 		freq[words] = freq.get(words,0) + 1

# 	words = list(freq.keys())
# 	words.sort()

# 	for w in words:
# 		print(w,':',freq[w])
# print(countfrequency.__doc__)
# countfrequency()


# 13
# def chinesePuzzle(numHeads,numlegs):
# 	"""
# 	We count 35 heads and 94 legs among the chickens and rabbits in a farm.
# 	How many rabbits and how many chickens do we have?
# 	"""
# 	ns = 'No Solution!'
# 	for i in range(numHeads + 1):
# 		j = numHeads - i
# 		if 2*i + 4*j == numLegs:
# 			yield i,j
# 	return ns,ns

# numHeads = 35
# numLegs = 94
# chickens = []
# rabbits = []
# print(chinesePuzzle.__doc__)
# for x,y in chinesePuzzle(numHeads, numLegs):
# 	chickens.append(x)
# 	rabbits.append(y)
# print(list(zip(chickens, rabbits)))


# 14
# Iterate steps by 2
# inputs = input()
# print(inputs[::2])
# print(inputs[::-1])

# 13
# def countItems():
# 	"""
# 	Count characters in the input and print it occurence
# 	"""
# 	count = {}
# 	inputs = input()
# 	for s in inputs:
# 		count[s] = count.get(s,0) + 1
# 	print('\n'.join(['%s,%s' % (k,v) for k,v in count.items()]))

# print(countItems.__doc__)
# countItems()

# 14
# class Person(object):
# 	def getGender(self):
# 		return 'Unknown'

# class Male(Person):
# 	def getGender(self):
# 		return 'Male'

# class Female(Person):
# 	def getGender(self):
# 		return 'Female'

# aMale = Male()
# aFemale = Female()
# print(aMale.getGender())
# print(aFemale.getGender())

# 15
# def removeDuplicate( li ):
# 	"""
# 	Remove duplicate
# 	"""
#     newli=[]
#     seen = set()
#     for item in li:
#         if item not in seen:
#             seen.add( item )
#             newli.append(item)

#     return newli

# li=[12,24,35,24,88,120,155,88,120,155]
# print(removeDuplicate(li))

# 16
"""
Initializing matrix and printing it
"""
# arr 1= [[[0 for col in range(8)]for col in range(5)]for row in range(3)]
# for row in arr:
# 	print("\n".join(map(str,row)))

# 17
"""Sentence Formation"""
# subjects=["I", "You"]
# verbs=["Play", "Love"]
# objects=["Hockey","Football"]

# for s in subjects:
# 	for v in verbs:
# 		for o in objects:
# 			print(s ,v ,o)

# 18
"""Lambda function using map"""
# print(list(map(lambda x:1+1,range(100))))

# 19
"""Compressing and decompressing a string"""
# import zlib
# s = 'hello world!hello world!hello world!hello world!'
# t = zlib.compress(bytearray(s,'utf8'))
# print (t)
# print(zlib.decompress(t))


# 20
# import random
# nos = random.random()*100
# if nos < 5:
# 	print(nos + (5 - nos))
# elif nos > 95:
# 	print(nos - (nos - 95))
# else:
# 	print(nos)






"""All the sorting algorithm in python"""

# 1

# def bubbleSort(li):
# 	"""Bubble sort """
# 	for iter_num in range(len(li)-1,0,-1):
# 		for idx in range(iter_num):
# 			if li[idx] > li[idx+1]:
# 				temp = li[idx]
# 				li[idx] = li[idx+1]
# 				li[idx+1] = temp

# print(bubbleSort.__doc__)
# li = [52,85,4,7,96,25,35,84,58]
# bubbleSort(li)
# print(li)


# 2

# def mergeSort(li):
# 	"""
# 	Merge Sort
# 	"""
# 	if len(li) <= 1:
# 		return li

# 	middle = (len(li)//2)
# 	left_list = li[:middle]
# 	right_list = li[middle:]
#

# 	left_list = mergeSort(left_list)
#
# 	right_list = mergeSort(right_list)
#
# 	return list(merge(left_list,right_list))

# def merge(left_half,right_half):
# 	res = []
# 	while len(left_half) != 0 and len(right_half) != 0:
# 		if left_half[0] < right_half[0]:
# 			res.append(left_half[0])
# 			left_half.remove(left_half[0])
# 		else:
# 			res.append(right_half[0])
# 			right_half.remove(right_half[0])
# 	if len(left_half) == 0:
# 		res = res + right_half
# 	else:
# 		res = res + left_half
# 	return res


# print(mergeSort.__doc__)
# li = [85,52,4,7]
# print(li)
# print(mergeSort(li))

# 3

# def insertionSort(li):
"""
Insertion Sort:
Insertion sort involves finding the right place for a given element in a sorted list.
So in beginning we compare the first two elements and sort them by comparing them. 
Then we pick the third element and find its proper position among the previous two sorted elements. 
This way we gradually go on adding more elements to the already sorted list by putting them in their proper position.

"""
# 	for i in range(1,len(li)):
# 		j = i-1
# 		next_elem = li[i]

# 		while (li[j] > next_elem) and (j >= 0):
# 			li[j+1] = li[j]
# 			j = j-1
# 			li[j+1] = next_elem


# print(insertionSort.__doc__)
# li = [85,52,4,7]
# print(li)
# print(insertionSort(li))

# 4

# def quickSort(li,first,last):
# 	"""
# 	Quick Sort same as merge sort but uses less memory
# 	"""
# 	if first < last:
# 		splitpoint = partition(li,first,last)

# 		quickSort(li, first, splitpoint - 1)
# 		quickSort(li, splitpoint + 1, last)

# def partition(li,first,last):
# 	pivot = li[first]
# 	leftmark = first + 1
# 	rightmark = last

# 	done = False
# 	while not done:

# 		while leftmark <= rightmark and li[leftmark] <= pivot:
# 			leftmark = leftmark + 1

# 		while li[rightmark] >= pivot and rightmark >= leftmark:
# 			rightmark = rightmark - 1

# 		if rightmark < leftmark:
# 			done = True
# 		else:
# 			li[leftmark] = li[rightmark] + li[leftmark]
# 			li[rightmark] = li[leftmark] - li[rightmark]
# 			li[leftmark] = li[leftmark] - li[rightmark]

# 	temp = li[first]
# 	li[first] = li[rightmark]
# 	li[rightmark] = temp

# 	return rightmark

# li = [52,42,58,9,67,14,15,35,28,98,74,48,52]
# print(quickSort.__doc__)
# quickSort(li, 0, len(li) - 1)
# print(li)


# def heapify(arr, n, i):
# 	largest = i
# 	l = 2 * i + 1
# 	r = 2 * i + 2
# 	if l < n and arr[i] < arr[l]:
# 		largest = l

# if r < n and arr[largest] < arr[r]:
# 		largest = r

# 	if largest != i:
# 		arr[i],arr[largest] = arr[largest],arr[i]
# 		heapify(arr, n, largest)
# def heapSort(arr):
# 	'''
# 	Heap sort
# 	'''
# 	n = len(arr)

# 	for i in range(n, -1, -1):
# 		heapify(arr, n, i)

# 	for i in range(n-1, 0, -1):
# 		arr[i], arr[0] = arr[0], arr[i]
# 		heapify(arr, i, 0)

# arr = [ 12, 11, 13, 5, 6, 7]
# print(heapSort.__doc__)
# heapSort(arr)
# print ('\n'.join(str(a) for a in arr))


# ********** Searching algorithm in python ***************
