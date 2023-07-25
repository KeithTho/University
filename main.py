import tkinter as tk
import mazeGen as mg
import pathFind as pf
import time

# variables used for the dimensions in the maze
mazeSizeCell = 80  # length of cells in pixels
mazeSizeWhole = 9  # number of rows/columns
maze = [["w" for i in range(mazeSizeWhole)] for i in range(mazeSizeWhole)] # list of lists to store maze cell information

# variables used in data outputs for pathfinding evaluation
outputTimeElapsedSeconds = 0 # tracks the time elapsed since pathfinding began
outputSearchedPercent = "0%" # tracks the percent of maze cells searched
outputSolvedLength = 0 # counts the number of cells used in the solved path

# variables used in option menus and radio buttons
optionMaze = ["Binary Tree", "Binary Tree Modified", "Aldous-Broder"]
optionPath = ["Breadth-First Search", "Depth-First Search", "Depth-First Search Opposed", 
	     		 "Djikstra's Algorithm", "A* Euclidean", "A* Manhattan", "A* Dysfunctional"]
optionSize = ["Small", "Medium", "Large"]
optionGrid = ["Off", "On"]
optionSpeed = ["Fastest", "Fast", "Slow"]


#######################
#######################
###		Functions	###
#######################
#######################

# function for creating the visualisation of the entire maze
def mazeDrawWhole(maze):
	canvas.delete("all")  # avoid memory leak
	for i, row in enumerate(maze):
		for j, col in enumerate(row):
			if i == 1 and j == 1:  # print starting cell
				colour = "#7a68d4"
			elif i == mazeSizeWhole - 2 and j == mazeSizeWhole - 2:  # print final cell as red
				colour = "#a31a00"
			elif str(col) == "c":  # print clearings as white
				colour = "white"
			elif str(col) == "w":  # print walls as black
				colour = "#22323d"
			mazeDrawCell(i, j, colour)


# function for drawing individual cells within the maze
def mazeDrawCell(row, col, colour):
	# cells are drawn 2px larger on both length and width if there is no grid
	if choiceGrid.get() == "Off":
		if row == 0 and col == 0:
			canvas.create_rectangle(11, 11, 30, 30, fill="#22323d", outline="#22323d")
		else:
			x1 = (row * mazeSizeCell) + (0.5 * mazeSizeCell) + 1
			x2 = x1 + mazeSizeCell
			y1 = (col * mazeSizeCell) + (0.5 * mazeSizeCell) + 1
			y2 = y1 + mazeSizeCell
			canvas.create_rectangle(x1, y1, x2, y2, fill=colour, width=0)
	else:
		if row == 0 and col == 0:
			canvas.create_rectangle(11, 11, 30, 30, fill="#22323d", outline="#22323d")
		else:
			x1 = 1 + (row * mazeSizeCell) + (0.5 * mazeSizeCell)
			x2 = x1 + mazeSizeCell
			y1 = 1 + (col * mazeSizeCell) + (0.5 * mazeSizeCell)
			y2 = y1 + mazeSizeCell
			canvas.create_rectangle(x1, y1, x2, y2, fill=colour, outline="#22323d")


# function that calls maze generation algorithms, called by mazeGenButton
def mazeGen():
	global maze
	global mazeSizeCell
	global mazeSizeWhole

	# establishes size before calling maze generation algorithm
	if choiceSize.get() == "Small":
		mazeSizeWhole = 9
		mazeSizeCell = 80
	elif choiceSize.get() == "Medium":
		mazeSizeWhole = 39
		mazeSizeCell = 20
	else:
		mazeSizeWhole = 159
		mazeSizeCell = 5
	maze = [["w" for i in range(mazeSizeWhole)] for i in range(mazeSizeWhole)]

	# calls corresponding maze generation algorithm, followed by visualisation
	if choiceMaze.get() == "Binary Tree":
		maze = mg.BinaryTree.mgBT(maze)
	elif choiceMaze.get() == "Binary Tree Modified":
		maze = mg.BinaryTreeModified.mgBTM(maze)
	else:
		maze = mg.AldousBroder.mgAB(maze)
	mazeDrawWhole(maze)
	

# function for reseting the pathfinding visualisation while maintaining the same maze design
def mazeReset():
	canvas.delete("all")  # avoid memory leak
	mazeDrawWhole(maze)
	
	outputVariableSearchedPercent.set("0%")	
	outputVariableSolvedLength.set(0)	
	outputVariableTimeElapsedSeconds.set(0)
	
# function for calling the pathfinding functions based on user choice
def pathFind():
	global outputSearchedPercent
	global outputSolvedLength
	global outputTimeElapsedSeconds

	outputTimeElapsedSeconds = time.time()

	# establishes speed before calling pathfinding algorithm
	if choiceSpeed.get() == "Fast":
		speedPass = 2 / ((mazeSizeWhole + 1) * (mazeSizeWhole + 1))
	elif choiceSpeed.get() == "Slow":
		speedPass = 2 / (mazeSizeWhole + 1)
	else:
		speedPass = 0

	# chained elif statements to call corresponding pathfinding algorithm
	if choicePath.get() == "Breadth-First Search":
		outputTimeElapsedSeconds, outputSearchedPercent, outputSolvedLength = pf.BreadthFirst.pfBF(canvas, mazeSizeCell, maze, choiceGrid.get(), speedPass)
	elif choicePath.get() == "Depth-First Search":
		outputTimeElapsedSeconds, outputSearchedPercent, outputSolvedLength = pf.DepthFirst.pfDF(canvas, mazeSizeCell, maze, choiceGrid.get(), speedPass, True)
	elif choicePath.get() == "Depth-First Search Opposed":
		outputTimeElapsedSeconds, outputSearchedPercent, outputSolvedLength = pf.DepthFirst.pfDF(canvas, mazeSizeCell, maze, choiceGrid.get(), speedPass, False)
	elif choicePath.get() ==  "Djikstra's Algorithm":
		outputTimeElapsedSeconds, outputSearchedPercent, outputSolvedLength = pf.AStarAlgorithm.pfAStar(canvas, mazeSizeCell, maze, choiceGrid.get(), speedPass, 0)
	elif choicePath.get() ==  "A* Euclidean":
		outputTimeElapsedSeconds, outputSearchedPercent, outputSolvedLength = pf.AStarAlgorithm.pfAStar(canvas, mazeSizeCell, maze, choiceGrid.get(), speedPass, 1)
	elif choicePath.get() ==  "A* Manhattan":
		outputTimeElapsedSeconds, outputSearchedPercent, outputSolvedLength = pf.AStarAlgorithm.pfAStar(canvas, mazeSizeCell, maze, choiceGrid.get(), speedPass, 2)
	elif choicePath.get() ==  "A* Dysfunctional":
		outputTimeElapsedSeconds, outputSearchedPercent, outputSolvedLength = pf.AStarAlgorithm.pfAStar(canvas, mazeSizeCell, maze, choiceGrid.get(), speedPass, 3)

	# modifying string to display correctly in GUI
	outputSearchedPercent = str(outputSearchedPercent * 100 )[0:4] + "%"
	outputTimeElapsedSeconds = str(outputTimeElapsedSeconds)[0:4]

	# setting variable strings for GUI display
	outputVariableSearchedPercent.set(outputSearchedPercent)	
	outputVariableSolvedLength.set(outputSolvedLength)	
	outputVariableTimeElapsedSeconds.set(outputTimeElapsedSeconds)



#######################
#######################
###		GUI LOOP	###
#######################
#######################

###################################
## Initialisation and Decoration ##
###################################

# initialise the main window which contains all of the gui/tkinter elements and begin gui loop
main = tk.Tk()
main.resizable(False, False)
main.title("Project")
main.geometry("1200x800")

# intialise the variable strings required for dropdowns and radio buttons
choiceMaze = tk.StringVar(main)
choiceMaze.set("Select an Option")
choicePath = tk.StringVar(main)
choicePath.set("Select an Option")
choiceSize = tk.StringVar(main)
choiceSize.set("Small")
choiceGrid = tk.StringVar(main)
choiceGrid.set("Off")
choiceSpeed = tk.StringVar(main)
choiceSpeed.set("Fastest")

#initalise the variable strings required for data outputs
outputVariableTimeElapsedSeconds = tk.StringVar(main)
outputVariableTimeElapsedSeconds.set(outputTimeElapsedSeconds)
outputVariableSearchedPercent = tk.StringVar(main)
outputVariableSearchedPercent.set(outputSearchedPercent)
outputVariableSolvedLength = tk.StringVar(main)
outputVariableSolvedLength.set(outputSolvedLength)

# tkinter objects for window and decoration
canvas = tk.Canvas(main, height=800, width=1200, bg="#22323d")
canvas.pack()
canvasOpt = tk.Frame(main, bg="#b0d1d9")
canvasOpt.place(x=806, y=2, width=392, height=800)
canvasRadioSize = tk.Frame(canvasOpt)				# Radiobuttons to change the size
canvasRadioSize.place(relx=0.25, rely=0.23, anchor="n")
canvasRadioGrid = tk.Frame(canvasOpt)				# Radiobuttons to toggle the grid
canvasRadioGrid.place(relx=0.5, rely=0.23, anchor="n")
canvasRadioSpeed = tk.Frame(canvasOpt)				# Radiobuttons to change the speed
canvasRadioSpeed.place(relx=0.75, rely=0.23, anchor="n")

# Labels for the right side of the window
mazeTitle = tk.Label(canvasOpt, text="Algorithm Options", bg="#b0d1d9", font=("Calibri Bold", 25))
mazeTitle.place(relx=0.2, rely=0.01)
credits = tk.Label(canvasOpt, text="Project by Keith Taylor", bg="#b0d1d9", font=("Calibri Bold", 8))
credits.place(relx=1, rely=1, anchor="se")


#######################
## Algorithm Utility ##
#######################

# tkinter objects relating to selection and generation of mazes
mazeGenLabel = tk.Label(canvasOpt, text="Maze Gen Algorithm", bg="#b0d1d9", font=("Calibri Bold", 8))
mazeGenLabel.place(relx=0.25, rely=0.085, anchor="center")
mazeDrop = tk.OptionMenu(canvasOpt, choiceMaze, *optionMaze)
mazeDrop.configure(width=15)
mazeDrop.pack()
mazeDrop.place(relx=0.25, rely=0.1, anchor=tk.N)
mazeGenButton = tk.Button(canvasOpt, text="Generate", command=mazeGen)
mazeGenButton.pack()
mazeGenButton.place(relx=0.25, rely=0.15, anchor=tk.N)

# tkinter objects relating to selection and pathfinding of mazes
pathFindLabel = tk.Label(canvasOpt, text="Pathfinding Algorithm", bg="#b0d1d9", font=("Calibri Bold", 8))
pathFindLabel.place(relx=0.75, rely=0.085, anchor="center")
pathDrop = tk.OptionMenu(canvasOpt, choicePath, *optionPath)
pathDrop.configure(width=23)
pathDrop.pack()
pathDrop.place(relx=0.75, rely=0.1, anchor=tk.N)
pathFindButton = tk.Button(canvasOpt, text="Generate", command=pathFind)
pathFindButton.pack()
pathFindButton.place(relx=0.75, rely=0.15, anchor=tk.N)

# tkinter object for resetting the current pathfinding visualisation while maintaining the current maze
mazeResetButton = tk.Button(canvasOpt, text="Reset", command=mazeReset)
mazeResetButton.pack()
mazeResetButton.place(relx=0.5, rely=0.15, anchor=tk.N)


###################
## Radio Buttons ##
###################

# tkinter objects for changing the size of the maze
mazeGenSizeLabel = tk.Label(canvasOpt, text="Maze Size", bg="#b0d1d9", font=("Calibri Bold", 8))
mazeGenSizeLabel.place(relx=0.25, rely=0.215, anchor="center")
for value in optionSize:
	tk.Radiobutton(	canvasRadioSize,text=value,indicatoron=0,width=7,padx=20,variable=choiceSize,value=value).pack(fill="both")

# tkinter objects for toggling the grid of the visualisation
mazeGenGridLabel = tk.Label(canvasOpt, text="Grid", bg="#b0d1d9", font=("Calibri Bold", 8))
mazeGenGridLabel.place(relx=0.5, rely=0.215, anchor="center")
for value in optionGrid:
	tk.Radiobutton(canvasRadioGrid,text=value,indicatoron=0,width=3,padx=20,variable=choiceGrid,value=value).pack(fill="both")

# tkinter objects for changing the speed of the pathfinding
pathFindSpeedLabel = tk.Label(canvasOpt, text="Pathfinder Speed", bg="#b0d1d9", font=("Calibri Bold", 8))
pathFindSpeedLabel.place(relx=0.75, rely=0.215, anchor="center")
for value in optionSpeed:
	tk.Radiobutton(canvasRadioSpeed,text=value,indicatoron=0,width=7,padx=20,variable=choiceSpeed,value=value).pack(fill="both")


###################
## 	Data Outputs ##
###################

# tkinter objects for displaying the time taken for the pathfinder to solver
outputTimeTitle = tk.Label(canvasOpt, text="Time Taken (s)", bg="#b0d1d9", font=("Calibri Bold", 8))
outputTimeTitle.place(relx=0.25, rely=0.415, anchor="center")
outputTimeLabel = tk.Label(canvasOpt, textvariable=(outputVariableTimeElapsedSeconds), bg="black", fg = "white", font=("Calibri Bold", 12), height = 1, width =8)
outputTimeLabel.place(relx=0.25, rely=0.45, anchor="center")

# tkinter objects for displaying % of maze searched
outputSearchedTitle = tk.Label(canvasOpt, text="Maze Searched %", bg="#b0d1d9", font=("Calibri Bold", 8))
outputSearchedTitle.place(relx=0.5, rely=0.415, anchor="center")
outputSearched = tk.Label(canvasOpt, textvariable=(outputVariableSearchedPercent), bg="black", fg = "white", font=("Calibri Bold", 12), height = 1, width =8)
outputSearched.place(relx=0.5, rely=0.45, anchor="center")

# tkinter objects for displaying the length of the solved path
outputLengthTitle = tk.Label(canvasOpt, text="Solved Path Length", bg="#b0d1d9", font=("Calibri Bold", 8))
outputLengthTitle.place(relx=0.75, rely=0.415, anchor="center")
outputLength = tk.Label(canvasOpt, textvariable=(outputVariableSolvedLength), bg="black", fg = "white", font=("Calibri Bold", 12, ), height = 1, width =8)
outputLength.place(relx=0.75, rely=0.45, anchor="center")


# close GUI loop
main.mainloop()
