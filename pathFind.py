import tkinter as tk
import time
import sys
import math


class Tools:  # class for tools used by pathfinders and mazeGen
	# function for drawing individual cells of the calculation in progress
	def drawCalculation(canvas, mazeSizeCell, row, col, grid):
		if grid == "On":
			x1 = (row * mazeSizeCell) + (0.5 * mazeSizeCell) + 2
			x2 = x1 + mazeSizeCell - 1
			y1 = (col * mazeSizeCell) + (0.5 * mazeSizeCell) + 2
			y2 = y1 + mazeSizeCell - 1
			if row != 1 or col != 1:
				canvas.create_rectangle(x1, y1, x2, y2, fill="#ffca45", width=0)
		else:
			x1 = (row * mazeSizeCell) + (0.5 * mazeSizeCell) + 1
			x2 = x1 + mazeSizeCell
			y1 = (col * mazeSizeCell) + (0.5 * mazeSizeCell) + 1
			y2 = y1 + mazeSizeCell
			if row != 1 or col != 1:
				canvas.create_rectangle(x1, y1, x2, y2, fill="#ffca45", width=0)
		canvas.update()

	# function for drawing individual cells of the solution
	#	first checks if Grid is an option, as it modifies the visualisation
	def drawSolutionCell(canvas, mazeSizeCell, row, col, grid):
		if grid == "On":
			x1 = (row * mazeSizeCell) + (0.5 * mazeSizeCell) + 2
			x2 = x1 + mazeSizeCell - 1
			y1 = (col * mazeSizeCell) + (0.5 * mazeSizeCell) + 2
			y2 = y1 + mazeSizeCell - 1
			canvas.create_rectangle(x1, y1, x2, y2, fill="#58b33d", width=0)
		else:
			x1 = (row * mazeSizeCell) + (0.5 * mazeSizeCell) + 1
			x2 = x1 + mazeSizeCell
			y1 = (col * mazeSizeCell) + (0.5 * mazeSizeCell) + 1
			y2 = y1 + mazeSizeCell
			canvas.create_rectangle(x1, y1, x2, y2, fill="#58b33d", width=0)
		canvas.update()

	# function for creating the solution visualisation by recursively calling drawSolutionCell
	#	uses time.sleep to slow down the visualisation based on the user's chosen speed
	def drawSolutionWhole(canvas, mazeSizeCell, solvedPath, grid, speed):
		for i in range(len(solvedPath) - 1):
			time.sleep(speed / 4)
			Tools.drawSolutionCell(canvas, mazeSizeCell, solvedPath[i][0], solvedPath[i][1], grid)
			time.sleep(speed / 4)
			if solvedPath[i][0] == solvedPath[i + 1][0]:
				j = (int(solvedPath[i][1]) + int(solvedPath[i + 1][1])) / 2
				Tools.drawSolutionCell(canvas, mazeSizeCell, solvedPath[i][0], j, grid)
			elif solvedPath[i][1] == solvedPath[i + 1][1]:
				j = (int(solvedPath[i][0]) + int(solvedPath[i + 1][0])) / 2
				Tools.drawSolutionCell(canvas, mazeSizeCell, j, solvedPath[i][1], grid)
			canvas.update()
		Tools.drawSolutionCell(canvas, mazeSizeCell, 1, 1, grid)

	# function for counting up neighbours of every given cell in a maze to store in a dictionary
	def neighbourCount(maze):
		neighbours = {}  # dictionary storing cells as key and neighbour directions as associated values
		for i in range(len(maze) - 1):
			if i % 2 == 1:
				for j in range(len(maze) - 1):
					if j % 2 == 1:
						if maze[i][j] == "c":
							neighbours[(i, j)] = []
							if maze[i + 1][j] == "c":
								neighbours[(i, j)].append("E")
							if maze[i][j + 1] == "c":
								neighbours[(i, j)].append("S")
							if maze[i - 1][j] == "c":
								neighbours[(i, j)].append("W")
							if maze[i][j - 1] == "c":
								neighbours[(i, j)].append("N")
		return neighbours

#class to store the function used by Breadth-First Search
class BreadthFirst:
	# function for solving mazes with breadth first search
	def pfBF(canvas, mazeSizeCell, maze, grid, speed):
		visited = [(1, 1)]  # list to store all visted cells
		queue = [(1, 1)]  # list to store cells yet to run through the algorithm
		pathways = {} # dictionary storing every cell's origin during exploration
		solvedPath = []	# list storing every cell in the solved path
		neighbours = Tools.neighbourCount(maze)
		goal = ((len(maze) - 2), (len(maze) - 2)) # sets goal equal to the last cell of the maze
		outputTimeElapsedSeconds = time.time() # records start time
		
		# will run until every explorable cell has been seen
		#	 each loop removes one cell from the queue and explores every neighbour
		while len(queue) > 0:
			time.sleep(speed) # time.sleep used to slow down visualisation
			current = queue.pop(0)
			if current == ((len(maze) - 2), (len(maze) - 2)):
				break # used to break out of the while loop if the goal has been found
			for d in "ESWN":
				if d in neighbours[current]:
					if d == "E":
						nextCell = (current[0] + 2, current[1])
						nextPath = (current[0] + 1, current[1])
					elif d == "S":
						nextCell = (current[0], current[1] + 2)
						nextPath = (current[0], current[1] + 1)
					elif d == "W":
						nextCell = (current[0] - 2, current[1])
						nextPath = (current[0] - 1, current[1])
					elif d == "N":
						nextCell = (current[0], current[1] - 2)
						nextPath = (current[0], current[1] - 1)

					# draws explored cells for each given loop
					Tools.drawCalculation(canvas, mazeSizeCell, nextPath[0], nextPath[1], grid)
					Tools.drawCalculation(canvas, mazeSizeCell, nextCell[0], nextCell[1], grid)

					if nextCell not in visited:
						visited.append(nextCell)
						queue.append(nextCell)
						pathways[nextCell] = current
		while goal != (1, 1):
			solvedPath.append(goal)
			goal = pathways[goal]
		solvedPath.append((1, 1))

		outputTimeElapsedSeconds = time.time() - outputTimeElapsedSeconds
		Tools.drawSolutionWhole(canvas, mazeSizeCell, solvedPath, grid, speed)

		outputSearchedPercent = (len(visited) - 1) / ( ( ((len(maze) - 1) / 2) * ((len(maze) - 1) / 2) ) - 1 )
		outputSolvedLength = len(solvedPath) - 1

		return outputTimeElapsedSeconds, outputSearchedPercent, outputSolvedLength

#class to store all 3 functions used by depth first search
class DepthFirst:
	# function for completing the majority of the depth-first search with the same bias as the maze
	def pfSame(
		goal,
		current,
		neighbours,
		canvas,
		mazeSizeCell,
		maze,
		grid,
		speed,
		solvedPath,
		visited,
	):
		breakOut = False
		if "E" in neighbours[current] and breakOut != True:
			nextCell = (current[0] + 2, current[1])
			nextPath = (current[0] + 1, current[1])
			neighbours[current].remove("E")
			time.sleep(speed)
			Tools.drawCalculation(canvas, mazeSizeCell, nextPath[0], nextPath[1], grid)
			Tools.drawCalculation(canvas, mazeSizeCell, nextCell[0], nextCell[1], grid)
			if nextCell != goal and nextCell not in visited:
				neighbours[nextCell].remove("W")
				visited[nextCell] = ""
				goal, breakOut, visited = DepthFirst.pfSame(
					goal,
					nextCell,
					neighbours,
					canvas,
					mazeSizeCell,
					maze,
					grid,
					speed,
					solvedPath,
					visited,
				)
			if nextCell == goal:
				solvedPath.append(goal)
				goal = current
				return goal, True, visited
		if "S" in neighbours[current] and breakOut != True:
			nextCell = (current[0], current[1] + 2)
			nextPath = (current[0], current[1] + 1)
			neighbours[current].remove("S")
			time.sleep(speed)
			Tools.drawCalculation(canvas, mazeSizeCell, nextPath[0], nextPath[1], grid)
			Tools.drawCalculation(canvas, mazeSizeCell, nextCell[0], nextCell[1], grid)
			if nextCell != goal and nextCell not in visited:
				neighbours[nextCell].remove("N")
				visited[nextCell] = ""
				goal, breakOut, visited = DepthFirst.pfSame(
					goal,
					nextCell,
					neighbours,
					canvas,
					mazeSizeCell,
					maze,
					grid,
					speed,
					solvedPath,
					visited,
				)
			if nextCell == goal:
				solvedPath.append(goal)
				goal = current
				return goal, True, visited
		if "W" in neighbours[current] and breakOut != True:
			nextCell = (current[0] - 2, current[1])
			nextPath = (current[0] - 1, current[1])
			neighbours[current].remove("W")
			time.sleep(speed)
			Tools.drawCalculation(canvas, mazeSizeCell, nextPath[0], nextPath[1], grid)
			Tools.drawCalculation(canvas, mazeSizeCell, nextCell[0], nextCell[1], grid)
			if nextCell != goal and nextCell not in visited:
				neighbours[nextCell].remove("E")
				visited[nextCell] = ""
				goal, breakOut, visited = DepthFirst.pfSame(
					goal,
					nextCell,
					neighbours,
					canvas,
					mazeSizeCell,
					maze,
					grid,
					speed,
					solvedPath,
					visited,
				)
			if nextCell == goal:
				solvedPath.append(goal)
				goal = current
				return goal, True, visited
		if "N" in neighbours[current] and breakOut != True:
			nextCell = (current[0], current[1] - 2)
			nextPath = (current[0], current[1] - 1)
			neighbours[current].remove("N")
			time.sleep(speed)
			Tools.drawCalculation(canvas, mazeSizeCell, nextPath[0], nextPath[1], grid)
			Tools.drawCalculation(canvas, mazeSizeCell, nextCell[0], nextCell[1], grid)
			if nextCell != goal and nextCell not in visited:
				neighbours[nextCell].remove("S")
				visited[nextCell] = ""
				goal, breakOut, visited = DepthFirst.pfSame(
					goal,
					nextCell,
					neighbours,
					canvas,
					mazeSizeCell,
					maze,
					grid,
					speed,
					solvedPath,
					visited,
				)
			if nextCell == goal:
				solvedPath.append(goal)
				goal = current
				return goal, True, visited
		return goal, False, visited

	# function used to perform depth first search with an opposed bias
	def pfOpposed(
		goal,
		current,
		neighbours,
		canvas,
		mazeSizeCell,
		maze,
		grid,
		speed,
		solvedPath,
		visited,
	):
		breakOut = False
		if "N" in neighbours[current] and breakOut != True:
			nextCell = (current[0], current[1] - 2)
			nextPath = (current[0], current[1] - 1)
			neighbours[current].remove("N")
			time.sleep(speed)
			Tools.drawCalculation(canvas, mazeSizeCell, nextPath[0], nextPath[1], grid)
			Tools.drawCalculation(canvas, mazeSizeCell, nextCell[0], nextCell[1], grid)
			if nextCell != goal and nextCell not in visited:
				neighbours[nextCell].remove("S")
				visited[nextCell] = ""
				goal, breakOut, visited = DepthFirst.pfOpposed(
					goal,
					nextCell,
					neighbours,
					canvas,
					mazeSizeCell,
					maze,
					grid,
					speed,
					solvedPath,
					visited,
				)
			if nextCell == goal:
				solvedPath.append(goal)
				goal = current
				return goal, True, visited
		if "W" in neighbours[current] and breakOut != True:
			nextCell = (current[0] - 2, current[1])
			nextPath = (current[0] - 1, current[1])
			neighbours[current].remove("W")
			time.sleep(speed)
			Tools.drawCalculation(canvas, mazeSizeCell, nextPath[0], nextPath[1], grid)
			Tools.drawCalculation(canvas, mazeSizeCell, nextCell[0], nextCell[1], grid)
			if nextCell != goal and nextCell not in visited:
				neighbours[nextCell].remove("E")
				visited[nextCell] = ""
				goal, breakOut, visited = DepthFirst.pfOpposed(
					goal,
					nextCell,
					neighbours,
					canvas,
					mazeSizeCell,
					maze,
					grid,
					speed,
					solvedPath,
					visited,
				)
			if nextCell == goal:
				solvedPath.append(goal)
				goal = current
				return goal, True, visited
		if "S" in neighbours[current] and breakOut != True:
			nextCell = (current[0], current[1] + 2)
			nextPath = (current[0], current[1] + 1)
			neighbours[current].remove("S")
			time.sleep(speed)
			Tools.drawCalculation(canvas, mazeSizeCell, nextPath[0], nextPath[1], grid)
			Tools.drawCalculation(canvas, mazeSizeCell, nextCell[0], nextCell[1], grid)
			if nextCell != goal and nextCell not in visited:
				neighbours[nextCell].remove("N")
				visited[nextCell] = ""
				goal, breakOut, visited = DepthFirst.pfOpposed(
					goal,
					nextCell,
					neighbours,
					canvas,
					mazeSizeCell,
					maze,
					grid,
					speed,
					solvedPath,
					visited,
				)
			if nextCell == goal:
				solvedPath.append(goal)
				goal = current
				return goal, True, visited
		if "E" in neighbours[current] and breakOut != True:
			nextCell = (current[0] + 2, current[1])
			nextPath = (current[0] + 1, current[1])
			neighbours[current].remove("E")
			time.sleep(speed)
			Tools.drawCalculation(canvas, mazeSizeCell, nextPath[0], nextPath[1], grid)
			Tools.drawCalculation(canvas, mazeSizeCell, nextCell[0], nextCell[1], grid)
			if nextCell != goal and nextCell not in visited:
				neighbours[nextCell].remove("W")
				visited[nextCell] = ""
				goal, breakOut, visited = DepthFirst.pfOpposed(
					goal,
					nextCell,
					neighbours,
					canvas,
					mazeSizeCell,
					maze,
					grid,
					speed,
					solvedPath,
					visited,
				)
			if nextCell == goal:
				solvedPath.append(goal)
				goal = current
				return goal, True, visited
		return goal, False, visited

	# function called by main class. Initialises variables used by both versions of depth first
	#	 and then passes that information to the corresponding algorithm. 
	# 	 Is also responsible for visualisation
	def pfDF(canvas, mazeSizeCell, maze, grid, speed, bias):
		visited = {(1, 1): ""}
		solvedPath = []
		neighbours = Tools.neighbourCount(maze)
		current = (1, 1)
		goal = ((len(maze) - 2), (len(maze) - 2))
		outputTimeElapsedSeconds = time.time()

		sys.setrecursionlimit(6500)	# required to prevent overflow of recursion limit
		
		if bias == True:
			DepthFirst.pfSame(
				goal,
				current,
				neighbours,
				canvas,
				mazeSizeCell,
				maze,
				grid,
				speed,
				solvedPath,
				visited,
			)
		else:
			DepthFirst.pfOpposed(
				goal,
				current,
				neighbours,
				canvas,
				mazeSizeCell,
				maze,
				grid,
				speed,
				solvedPath,
				visited,
			)

		solvedPath.append((1, 1))

		outputTimeElapsedSeconds = time.time() - outputTimeElapsedSeconds
		Tools.drawSolutionWhole(canvas, mazeSizeCell, solvedPath, grid, speed)
		
		outputSearchedPercent = (len(visited) - 1) / ( ( ((len(maze) - 1) / 2) * ((len(maze) - 1) / 2) ) - 1 )
		outputSolvedLength = len(solvedPath) - 1

		return outputTimeElapsedSeconds, outputSearchedPercent, outputSolvedLength

#class to store the 2 functions used by A* algorithm
class AStarAlgorithm:
	# function to calculate the heuristic for any given cell
	def pfHeuristic(current, goal, heuristicChoice):
		if heuristicChoice == 0: 	# Djikstra's
			heuristic = 0
		elif heuristicChoice == 1:	# Euclidean
			heuristic = math.sqrt( ((abs(goal[0] - current[0]) /2 ) ** 2) + ((abs(goal[1] - current[1]) / 2 ) ** 2) )
		elif heuristicChoice == 2: 	# Manhattan
			heuristic = (abs(goal[0] - current[0]) / 2 + abs(goal[1] - current[1]) / 2 )
		else:						# Dysfunction
			heuristic = (abs(goal[0] + current[0]) / 2 + abs(goal[1] + current[1]) / 2 )
		return heuristic
	
	# function for performing the bulk of the a* algorithm
	def pfAStar(canvas, mazeSizeCell, maze, grid, speed, heuristicChoice):
		
		# initialisation of standard 
		solvedPath = []
		neighbours = Tools.neighbourCount(maze)
		current = (1, 1)
		goal = ((len(maze) - 2), (len(maze) - 2))
		heuristic = AStarAlgorithm.pfHeuristic(current, goal, heuristicChoice)

		# dict to store cells as key, followed by their actual value, their heuristic value, their origin cell
		#	 and if they have been visited already
		visited = {(1,1) : [0, heuristic, (0,0), 1]}	
		outputTimeElapsedSeconds = time.time()
		

		while current != goal:
				
			visitedLowest = [2048]
			time.sleep(speed) # time.sleep used to slow down visualisation
			if current == goal:
				break # used to break out of the while loop if the goal has been found
			currentActualValue = 0
			currentSource = current
			while visited[currentSource][2] != (0,0):
				currentActualValue += 1
				currentSource = visited[currentSource][2]
			for d in "ESWN": #for loop that scouts values for neighbouring cells
				if d in neighbours[current]:
					if d == "E":
						nextCell = (current[0] + 2, current[1])
					elif d == "S":
						nextCell = (current[0], current[1] + 2)
					elif d == "W":
						nextCell = (current[0] - 2, current[1])
					elif d == "N":
						nextCell = (current[0], current[1] - 2)
					
					if nextCell not in visited: 
						# if cell has not been visited before, adds information to the dict
						nextCellHeuristic = AStarAlgorithm.pfHeuristic(nextCell, goal, heuristicChoice)
						visited[nextCell] = [currentActualValue + 1, nextCellHeuristic, current, 0]
					elif nextCell in visited and visited[nextCell][0] > currentActualValue:
						# if cell has been visited before, checks to see if a new lowest value is found
						visited[nextCell][0] = currentActualValue + 1
			
			# calculates the lowest value cell which hasn't been explored
			for coordinate, value in visited.items():
				coordinateTotalValue = value[0] + value[1]
				coordinateHeuristicValue = AStarAlgorithm.pfHeuristic(coordinate, goal, heuristicChoice)
				if visited[coordinate][3] == 0:
					if visitedLowest[0] > coordinateTotalValue:
						visitedLowest = [coordinateTotalValue, coordinateHeuristicValue, coordinate]
					elif visitedLowest[1] > coordinateHeuristicValue:
						visitedLowest = [coordinateTotalValue, coordinateHeuristicValue, coordinate]
			
			current = visitedLowest[2]
			visited[current][3] = 1
			
			if current[0] + 2 == visited[current][2][0]:
				nextCell = (current[0] + 2, current[1])
				nextPath = (current[0] + 1, current[1])
			elif current[1] + 2 == visited[current][2][1]:
				nextCell = (current[0], current[1] + 2)
				nextPath = (current[0], current[1] + 1)
			elif current[0] - 2 == visited[current][2][0]:
				nextCell = (current[0] - 2, current[1])
				nextPath = (current[0] - 1, current[1])
			elif current[1] - 2 == visited[current][2][1]:
				nextCell = (current[0], current[1] - 2)
				nextPath = (current[0], current[1] - 1)
			Tools.drawCalculation(
				canvas, mazeSizeCell, nextPath[0], nextPath[1], grid
			)
			Tools.drawCalculation(
				canvas, mazeSizeCell, current[0], current[1], grid
			)

		# while loop for calculating the solution
		while goal != (1, 1):
			solvedPath.append(goal)
			goal = visited[goal][2]
		solvedPath.append((1, 1))

		# records final time when solution is found before drawing
		outputTimeElapsedSeconds = time.time() - outputTimeElapsedSeconds
		Tools.drawSolutionWhole(canvas, mazeSizeCell, solvedPath, grid, speed)
		
		outputSearchedPercent = (len(visited) - 1) / ( ( ((len(maze) - 1) / 2) * ((len(maze) - 1) / 2) ) - 1 )
		outputSolvedLength = len(solvedPath) - 1

		return outputTimeElapsedSeconds, outputSearchedPercent, outputSolvedLength
