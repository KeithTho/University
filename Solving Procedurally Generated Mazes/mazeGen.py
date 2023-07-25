import random
from pathFind import Tools


class BinaryTree:
	# function for generating mazes with binary tree algorithm
	def mgBT(maze):
		for i in range(len(maze) - 1):
			if i % 2 == 1:
				for j in range(len(maze) - 1):
					if j % 2 == 1:
						# coinflip to decide whether to clear wall north or east
						if random.randint(0, 1) == 1:
							if i == (len(maze) - 2) and j == (
								len(maze) - 2
							):  # final square doesn't clear a wall
								maze[i][j] = "c"
							elif 0 < j < (len(maze) - 2):
								maze[i][j] = "c"
								maze[i][j + 1] = "c"
							else:  # prevents maze from breaking the outer wall
								maze[i][j] = "c"
								maze[i + 1][j] = "c"

						else:
							if i == (len(maze) - 2) and j == (
								len(maze) - 2
							):  # final square doesn't clear a wall
								maze[i][j] = "c"
							elif 0 < i < (len(maze) - 2):
								maze[i][j] = "c"
								maze[i + 1][j] = "c"
							else:  # prevents maze from breaking the outer wall
								maze[i][j] = "c"
								maze[i][j + 1] = "c"
		return maze


class BinaryTreeModified:
	# function for generating modified binary tree mazes
	#	 first calls BinaryTree.mgBT to generate a maze, and then edits the maze
	#	 by searching for dead ends and adding new pathways to unconnected passages
	#	 this creates an imperfect maze with many passageways
	def mgBTM(maze):
		maze = BinaryTree.mgBT(maze)
		neighbours = Tools.neighbourCount(maze)
		
		for i, value in neighbours.items():
			# first searches for cells with only one neighbour i.e. dead ends
			if len(value) == 1:
				# first if statement used to ensure top left corner doesn't create a passageway outside the maze
				if i[0] == 1 and i[1] == 1:
					if value[0] == "E":
						neighbours[(i)].append("S")
						maze[i[0]][i[1] + 1] = "c"
					else:
						neighbours[(i)].append("E")
						maze[i[0] + 1][i[1]] = "c"

				# prevents northern wall from creating northern passageways
				elif i[0] == 1:
					if value[0] == "E":
						if random.randint(0, 1) == 1 and i[1] != len(maze) - 2:
							neighbours[(i)].append("S")
							maze[i[0]][i[1] + 1] = "c"
						elif i[1] != 1:
							neighbours[(i)].append("W")
							maze[i[0]][i[1] - 1] = "c"
					else:
						if random.randint(0, 1) == 1 and i[1] != len(maze) - 2:
							neighbours[(i)].append("E")
							maze[i[0] + 1][i[1]] = "c"
						elif i[1] != 1:
							neighbours[(i)].append("W")
							maze[i[0]][i[1] - 1] = "c"

				# prevents western wall from creating western passageways
				elif i[1] == 1:
					if value[0] == "E":
						if random.randint(0, 1) == 1 and i[0] != len(maze) - 2:
							neighbours[(i)].append("S")
							maze[i[0]][i[1] + 1] = "c"
						elif i[0] != 1:
							neighbours[(i)].append("N")
							maze[i[0] - 1][i[1]] = "c"
					else:
						if random.randint(0, 1) == 1 and i[0] != len(maze) - 2:
							neighbours[(i)].append("E")
							maze[i[0] + 1][i[1]] = "c"
						elif i[0] != 1:
							neighbours[(i)].append("N")
							maze[i[0] - 1][i[1]] = "c"

				# any cells that are not along the northern or western wall
				else:
					if value[0] == "E":
						randomCheck = random.randint(0, 2)
						if randomCheck == 0 and i[1] != len(maze) - 2:
							neighbours[(i)].append("S")
							maze[i[0]][i[1] + 1] = "c"
						elif randomCheck == 1:
							neighbours[(i)].append("W")
							maze[i[0]][i[1] - 1] = "c"
						else:
							neighbours[(i)].append("N")
							maze[i[0] - 1][i[1]] = "c"
					elif value[0] == "W":
						randomCheck = random.randint(0, 2)
						if randomCheck == 0 and i[1] != len(maze) - 2:
							neighbours[(i)].append("S")
							maze[i[0]][i[1] + 1] = "c"
						elif randomCheck == 1:
							neighbours[(i)].append("E")
							maze[i[0] + 1][i[1]] = "c"
						else:
							neighbours[(i)].append("N")
							maze[i[0] - 1][i[1]] = "c"
					elif value[0] == "N":
						randomCheck = random.randint(0, 2)
						if randomCheck == 0 and i[1] != len(maze) - 2:
							neighbours[(i)].append("S")
							maze[i[0]][i[1] + 1] = "c"
						elif randomCheck == 1:
							neighbours[(i)].append("E")
							maze[i[0] + 1][i[1]] = "c"
						else:
							neighbours[(i)].append("W")
							maze[i[0]][i[1] - 1] = "c"
					else:
						randomCheck = random.randint(0, 2)
						if randomCheck == 0 and i[1] != len(maze) - 2:
							neighbours[(i)].append("N")
							maze[i[0] - 1][i[1]] = "c"
						elif randomCheck == 1:
							neighbours[(i)].append("E")
							maze[i[0] + 1][i[1]] = "c"
						else:
							neighbours[(i)].append("W")
							maze[i[0]][i[1] - 1] = "c"

		return maze


class AldousBroder:
	# function for generating mazs with the Aldous-Broder algorithm
	def mgAB(maze):
		visited = {(1, 1): ""}
		x = 1 
		y = 1
		# while loop runs until every cell has been visited once
		while len(visited) < ((len(maze) - 1) / 2) * ((len(maze) - 1) / 2):
			maze[x][y] = "c"
			randomCheck = random.randint(0, 3)
			# next cell is chosen at random by randomCheck
			#	 with a second condition to prevent breaking outside the boundary
			if x != (len(maze) - 2) and randomCheck == 0:
				# nested within each if statement is the possibility of adding new cells
				#	 to the visited dictionary, if it has not been seen
				if ((x + 2, y)) not in visited:
					maze[x + 1][y] = "c"
					maze[x + 2][y] = "c"
					visited[x + 2, y] = ""
				# else the algorithm simply moves to that cell and repeats the cycle
				x += 2

			elif y != (len(maze) - 2) and randomCheck == 1:
				if ((x, y + 2)) not in visited:
					maze[x][y + 1] = "c"
					maze[x][y + 2] = "c"
					visited[x, y + 2] = ""
				y += 2

			elif x != 1 and randomCheck == 2:
				if ((x - 2, y)) not in visited:
					maze[x - 1][y] = "c"
					maze[x - 2][y] = "c"
					visited[x - 2, y] = ""
				x += -2

			elif y != 1 and randomCheck == 3:
				if ((x, y - 2)) not in visited:
					maze[x][y - 1] = "c"
					maze[x][y - 2] = "c"
					visited[x, y - 2] = ""
				y += -2
		return maze
