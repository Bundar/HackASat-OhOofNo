from pwn import *
import numpy as np
from PIL import Image
def calcSum(i,j):
	return int(img_arr[i-1][j-1]) + int(img_arr[i-1][j]) + int(img_arr[i-1][j+1]) +\
	int(img_arr[i][j-1]) + int(img_arr[i][j]) + int(img_arr[i][j+1]) +\
	int(img_arr[i+1][j-1]) +int(img_arr[i+1][j]) + int(img_arr[i+1][j+1])

def printSurroundings(i,j):
	print("(i,j): (" + str(i) + ", " + str(j)+") SUM: " + str(calcSum(i,j)) )
	surroundings = img_arr[i-1][j-1] + " | " + img_arr[i-1][j] + " | " + img_arr[i-1][j+1] +\
	"\n--- | --- | ---\n " +\
	img_arr[i][j-1] + " | " + img_arr[i][j] + " | " + img_arr[i][j+1] +\
	"\n--- | --- | --- \n" +\
	img_arr[i+1][j-1] + " | " + img_arr[i+1][j] + " | " + img_arr[i+1][j+1] + "\n"

	print(surroundings)

def checkStar(i, j):
	printSurroundings(i,j)
	# printSurroundings(int(starCoord.split(',')[0]),int(starCoord.split(',')[1]))
	# for each contiguous 255 calc surrounding sum and find max as center.
	if not ( 0 <= i < len(img_arr) and 0 <= j < len(img_arr[0])) and not visited[i][j]:
		return (0,"")
	visited[i][j] = 1

	best_ij = str(i) + "," + str(j)
	sum_ = calcSum(i,j)
	try:
		if not visited[i][j+1] and img_arr[i][j+1] == '255':
			e = checkStar(i, j+1)
			if e[0] > sum_:
				best_ij = e[1]
				sum_ = e[0]
		if not visited[i+1][j+1] and img_arr[i+1][j+1] == '255':
			se = checkStar(i+1, j+1)
			if se[0] > sum_:
				best_ij = se[1]
				sum_ = se[0]
		if not visited[i+1][j] and img_arr[i+1][j] == '255':
			s = checkStar(i+1, j)
			if s[0] > sum_:
				best_ij = s[1]
				sum_ = s[0]
		if not visited[i+1][j-1] and img_arr[i+1][j-1] == '255':
			sw = checkStar(i+1, j-1)
			if sw[0] > sum_:
				best_ij = sw[1]
				sum_ = sw[0]
	except:
		print("Somtin went rong")

	return (sum_, best_ij)


## Start Connection
r = remote('stars.satellitesabove.me', 5013)
log.info(r.recvuntil("\n").decode())

## Send Ticket
r.sendline("bravo37542zulu:GLwCA6GcV1bMI5FmiPWrNh8x6BqcrIoExeu5cu_Tq5bXrX1ItUtJMpBcBb0mOtbp-A")
iter_ = 0
while(True):
	log.info("Iteration: " + str(iter_))
	## Get input immage data
	img_string = r.recvuntil("\n\n").decode()

	# log.info(img_string)
	lines = img_string.split('\n')
	lines.pop()
	lines.pop()

	img_arr = [0]*len(lines)
	visited = [0]*len(lines)

	for i, line in enumerate(lines):
		img_arr[i] = line.split(',')
		visited[i] = [0]*len(img_arr[i])

	array = np.zeros([len(img_arr)+1, len(img_arr[0])+1, 3], dtype=np.uint8)

	log.info(r.recvuntil("\n").decode())
	log.info(r.recvuntil("\n").decode())
	for i, line in enumerate(lines):
		for j, val in enumerate(line.split(',')):
			array[i][j] = [int(val), int(val), int(val)]
			if visited[i][j] == 1:
				continue
			if val == '255':
				starCoord = checkStar(i,j)[1]
				log.info("Star Coord: " + starCoord)
				r.sendline(starCoord)
			else:
				visited[i][j] = 1

	img = Image.fromarray(array)
	img.save('starMapIter'+str(iter_)+'.png')
	iter_ += 1
	r.sendline('\n')
	log.info(r.recvline().decode())


r.interactive()



