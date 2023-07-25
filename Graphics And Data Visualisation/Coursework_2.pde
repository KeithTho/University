// import map image
PImage ukMap;
PShape ukMapShape;

// initialise camera parameters
float eyeX, eyeY, eyeZ, centreX, centreY, centreZ, eyeYTilt, centreYTilt, zoomMax, zoomMin;
boolean tilt, begin;

// initialise data variables
float barX, barY, barHeight, barColour, barFilter;
int barCheckX, barCheckY, currentYearPopulation, barColourIndex, currentYear;
Table ukDataTable;        //stores data
String barFilterString = "no filter";

// initialise colour mapping variables
int colourLookup[][] = {
  {26, 151, 80}, // dark green
  {165, 216, 106}, // light green
  {254, 224, 139}, // yellow
  {253, 174, 97}, // orange
  {214, 48, 39}, // red
}; //colourLookup[][]
float minPopulation, maxPopulation;

///////////////////////
//////SETUP////////////
///////////////////////

void setup() {
  size(700, 800, P3D);
  ukMap = loadImage("UKMAP.jpg");
  smooth();

  // assign camera variables for starting position
  eyeX = (ukMap.width/2);
  eyeY = (ukMap.height/2);
  eyeZ = zoomMin;
  centreX = (ukMap.width/2);
  centreY = (ukMap.height/2);
  centreZ = 0;

  // assign default camera settings
  zoomMax = 300;      //maximum amount of zoom (closest to map)
  zoomMin = 2600;     //minimum amount of zoom (furthest away)
  tilt = false;       //maintains consistency across tiled or untilted camera
  begin = false;      //used to show instructions screen at beginning

  // assign starting values for 1991
  currentYear = 1991;
  minPopulation = 81228;
  maxPopulation = 965928;

  // import data to table
  ukDataTable = loadTable("UKDATA.csv", "header");

  // assign ukMapShape and texture
  pushMatrix();
  noStroke();
  ukMapShape = createShape();
  ukMapShape.beginShape(QUAD);
  ukMapShape.texture(ukMap);
  ukMapShape.vertex(0, 0, 0, 0, 0);
  ukMapShape.vertex(ukMap.width, 0, 0, ukMap.width, 0);
  ukMapShape.vertex(ukMap.width, ukMap.height, 0, ukMap.width, ukMap.height);
  ukMapShape.vertex(0, ukMap.height, 0, 0, ukMap.height);
  ukMapShape.endShape();
  popMatrix();
  // finish ukMapShape assignment
}// setup


///////////////////////
//////DRAW/////////////
///////////////////////

void draw() {
  background(168, 205, 234);

  // instruction menu at launch
  if (begin==false) {
    pushMatrix();
    fill(0);
    textSize(100);
    text("Instructions", 20, 100, 0);
    textSize(30);
    text("Change census year with:", 20, 200, 0);
    textSize(20);
    text("      1 = 1991    |    2 = 2001    |    3 = 2011", 20, 230, 0);
    textSize(30);
    text("Change data filter from low to high", 20, 280, 0);
    textSize(20);
    text("      4 - 8 = change filter  |    9 = reset filter", 20, 310, 0);
    textSize(30);
    text("Reset data", 20, 360, 0);
    textSize(20);
    text("      SPACE", 20, 390, 0);
    textSize(30);
    text("Manipulate camera", 20, 440, 0);
    textSize(20);
    text("      W = tilt forwards    |    S = tilt backwards    |    Mouse Wheel = Zoom", 20, 470, 0);
    textSize(30);
    text("Navigate the map", 20, 520, 0);
    textSize(20);
    text("      arrow keys or drag mouse", 20, 550, 0);
    textSize(30);
    text("View City Details", 20, 600, 0);
    textSize(20);
    text("      Mouse Click on bar", 20, 630, 0);
    textSize(30);
    text("Press SPACE to begin", 200, 750, 0);
    fill(255);
    popMatrix();
  }// if begin == false

  // what is drawn after instruction menu is dismissed
  else {
    //modifies camera settings if tilt is true or not
    if (tilt == false) {
      camera(eyeX, eyeY, eyeZ, centreX, centreY, centreZ, 0, 1, 0);
      textSize(15);
      fill(0);
      text("current year: " + currentYear, eyeX-135, eyeY+150, eyeZ-298);
      text("filter: " + barFilterString, eyeX-135, eyeY+165, eyeZ-298);
      fill(255);
    } else {
      eyeYTilt = eyeY + (300*(eyeZ / zoomMax)/2.3);
      centreYTilt = centreY - (150*(eyeZ / zoomMax)/2.3);

      camera(eyeX, eyeYTilt, eyeZ, centreX, centreYTilt, centreZ, 0, 1, 0);
      textSize(15);
      fill(0);
      text("current year: " + currentYear, eyeX-135, eyeYTilt-50, eyeZ-298);
      text("filter: " + barFilterString, eyeX-135, eyeYTilt-35, eyeZ-298);
      fill(255);
    }// if tilt

    spotLight(255, 255, 255, eyeX+50, eyeYTilt+50, eyeZ+200, centreX, centreYTilt, centreZ, PI/3, 0);
    shape(ukMapShape);

    // for loop to process each entry in the table
    for (TableRow row : ukDataTable.rows()) {

      String cityName = row.getString("City");
      int longitude = row.getInt("longitude");
      int latitude = row.getInt("latitude");

      switch(currentYear) {  //switch that processes the population of the current year data
        case(1991):
        String populationOf1991 = row.getString("1991");
        String fixedPopulationOf1991 = populationOf1991.replace(",", "").replace("...", "0");
        currentYearPopulation = Integer.parseInt(fixedPopulationOf1991);
        break;

        case(2001):
        String populationOf2001 = row.getString("2001");
        String fixedpopulationOf2001 = populationOf2001.replace(",", "").replace("...", "0");
        currentYearPopulation = Integer.parseInt(fixedpopulationOf2001);
        break;

        case(2011):
        String populationOf2011 = row.getString("2011");
        String fixedpopulationOf2011 = populationOf2011.replace(",", "").replace("...", "0");
        currentYearPopulation = Integer.parseInt(fixedpopulationOf2011);
        break;
      }// currentYear switch

      // prevents bars from generating if they have no population
      if (currentYearPopulation > 0 ) {
        Bar currentBar = new Bar();
        pushMatrix();
        barColourIndex = currentBar.colorMapping((float)currentYearPopulation);
        currentBar.drawBar(longitude, latitude, currentYearPopulation/10000, barColourIndex, cityName, currentYearPopulation);
        popMatrix();
      }// if > bar generation
    }// for entry loop
  }// else (begin == true)
}//draw


///////////////////////
//////USER INPUT///////
///////////////////////

void keyPressed() {

  // if user input is coded (arrow keys to move)
  if (key == CODED) {

    switch(keyCode) {
    case LEFT:
      eyeX -= 10;
      centreX -= 10;
      break;

    case RIGHT:
      eyeX += 10;
      centreX += 10;
      break;

    case UP:
      eyeY -= 10;
      centreY -= 10;
      break;

    case DOWN:
      eyeY += 10;
      centreY += 10;
      break;
    }//switch for CODED keys
  } else {
    // if key is not coded
    switch(key) {

    case ' ': // full reset of camera and some data
      begin = true;

      // reset camera position
      eyeX = (ukMap.width/2);
      eyeY = (ukMap.height/2);
      eyeZ = zoomMin;
      centreX = (ukMap.width/2);
      centreY = (ukMap.height/2);
      centreZ = 0;
      // reset year to 1991
      currentYear = 1991;
      minPopulation = 81228;
      maxPopulation = 965928;
      // reset camera settings
      tilt = false;
      barFilter = 5;
      barFilterString = "no filter";
      break;

    case 'w':    //tilt camera backward
      tilt = true;
      break;

    case 's':    //tilt camera forward
      tilt = false;
      break;

    case '1':   // change census data to 1991
      currentYear = 1991;
      minPopulation = 81228;
      maxPopulation = 965928;
      break;

    case '2':   // change census data to 2001
      currentYear = 2001;
      minPopulation = 92415;
      maxPopulation = 970892;
      break;

    case '3':   // change census data to 2011
      currentYear = 2011;
      minPopulation = 100153;
      maxPopulation = 1085810;
      break;

    case '4':   // change filter to lowest population
      barFilter = 0;
      barFilterString = "lowest population";
      break;

    case '5':   // change filter to low population
      barFilter = 1;
      barFilterString = "low-medium population";
      break;

    case '6':   // change filter to medium population
      barFilter = 2;
      barFilterString = "medium population";
      break;

    case '7':   // change filter to high population
      barFilter = 3;
      barFilterString = "medium-high population";
      break;

    case '8':   // change filter to highest population
      barFilter = 4;
      barFilterString = "highest population";
      break;

    case '9':   // reset filter
      barFilter = 5;
      barFilterString = "no filter";
      break;
    }// switch
  } // else (not coded)
}// keyInput Method


// Zoom using the mouse wheel
void mouseWheel(MouseEvent event) {
  if ((event.getCount() < 0) && (eyeZ > zoomMax)) {
    eyeZ -= 100;
  }//if zooming out

  if ((event.getCount() > 0) && (eyeZ < zoomMin)) {
    eyeZ += 100;
  }//if zooming in
}//mouseWheel function

// Pan the map holding mouse button
void mouseDragged() {
  if (mouseButton == LEFT) {
    eyeX -= (mouseX - pmouseX)*(eyeZ / zoomMax)/2.3;
    eyeY -= (mouseY - pmouseY)*(eyeZ / zoomMax)/2.3;
    centreX -= (mouseX - pmouseX)*(eyeZ / zoomMax)/2.3;
    centreY -= (mouseY - pmouseY)*(eyeZ / zoomMax)/2.3;
    //  } else if (mouseButton == RIGHT) {
    //   eyeX -= tan(mouseX - pmouseX)*(eyeZ / zoomMax);
  }// if LEFT
}//mouseDragged function

// click to filter bar information and double click to snap to centre
void mouseClicked(MouseEvent event) {
  // records where clicks are, for filtering bar information
  barCheckX = (int)(eyeX - (((width/2) - mouseX)*(eyeZ / zoomMax) /2.3));
  barCheckY = (int)(eyeY - (((height/2) - mouseY)*(eyeZ / zoomMax) /2.3));

  // Double click the mouse to snap position to centre
  if (event.getCount() == 2) {
    eyeX -= (((width/2) - mouseX)*(eyeZ / zoomMax) /2.3);
    eyeY -= (((height/2) - mouseY)*(eyeZ / zoomMax) /2.3);
    centreX -= (((width/2) - mouseX)*(eyeZ / zoomMax) /2.3);
    centreY -= (((height/2) - mouseY)*(eyeZ / zoomMax) /2.3);
  }// double click
  
}// mouse click method


///////////////////////
//////METHODS//////////
///////////////////////


public class Bar {

  // method to draw a bar for the instanced population
  void drawBar(int barX, int barY, int barHeight, int barColourIndex, String cityName, int population) {
    // only draws the bar if this instance passes the population filter
    if (barFilter == barColourIndex || barFilter == 5) {
      pushMatrix();
      stroke(0);
      translate(barX, barY, (barHeight/2)+1);

      // draws city/population data if the user has clicked on that bar
      if ((barCheckX < barX+10 && barCheckX > barX-10) && (barCheckY < barY+10 && barCheckY > barY-10)) {
        textSize(10*(eyeZ / zoomMax));
        fill(0);

        // adjusts height of text to camera
        if (barHeight > eyeZ+200) {
          text(("< " + cityName), 10, 5, eyeZ-250);
          text("population: " + population, 10+(10*(eyeZ / zoomMax)), 5+(15*(eyeZ / zoomMax)), eyeZ-250);
        } else {
          text(("< " + cityName), 10, 5, barHeight/2);
          text("population: " + population, 10+(10*(eyeZ / zoomMax)), 5+(15*(eyeZ / zoomMax)), barHeight/2);
        }//  ifelse text height adjustment for camera
        
      }//  if mouse clicked on bar

      fill(colourLookup[barColourIndex][0], colourLookup[barColourIndex][1], colourLookup[barColourIndex][2]);
      box(10, 10, barHeight);
      popMatrix();
      
    }//  if population filter == instance of bar
    
  } // drawBar method

  // method to map the instanced population to the correct colour
  int colorMapping(float population) {

    int barColourIndex = (int)map(population, minPopulation, maxPopulation, 0, colourLookup.length);    
    if (barColourIndex < 0 )
      barColourIndex = 0;
    else if (barColourIndex >= colourLookup.length)
      barColourIndex = (colourLookup.length)-1;
    return barColourIndex;
  } // colourMapping method
  
} // Bar class
