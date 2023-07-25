# Graphics and Data Visualisation

This folder contains the code and necessary files to run the application I created for the second coursework in my Graphics and Data Visualisation module. The goal of this application was to create an interactive 3D visualisation of population data across the uk. Creating this required a solid grasp of trigonometry to manipulate the camera precisely in code. The rationale below explains some of the decisions I made, and is an excerpt from the written report. I achieved a grade of 45/50 in this coursework.

### Rationale

>Creating objects on top of a map relative to the cities means that many of those objects will have inconsistent space. Some objects may be very close, while others could be far apart. Using bars with a consistent and small width/length means that the data can still be visualised accurately while avoiding different objects overlapping with one another, such as if circles were placed on top of the map relative to the population size.
>The bars are coloured using a colour map relating the size of the population to traffic light colours, where green is a low population and red is a high population. The colour map limitations specifically exclude the population of London, as it is such an outlier that it warps all of the data and even using a logarithmic scale does not create a useful visualisation.
>On the screen at all times the user can see the filter for the current year and the population size, this is shown in the bottom left. Further, if the user clicks on a bar then text detailing the name of the corresponding city and population size will appear near the top of the bar.

### Instructions

To run this program, you must first install Processing 4.2. Open **Coursework_2.pde** and if a dialogue box opens asking to create a new directory, say No. Press play in the top left. From there, instructions will be available in the application. I have also included a copy of the instructions for reference below.

![Screenshot of Instructions window, detailing keybinds for user interaction](https://github.com/KeithTho/University/assets/102043623/9b9d78a9-9bfb-4787-91cd-4152137d0ad9)
