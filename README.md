# PyBrot

**PyBrot** is a lightweight, PyQt-based interactive python program to visualize the Mandelbrot set and save "Wallpaper" images scaled to your screen resolution.

**PyBrot** is free and open source software

## DEPENDENCIES
PyBrot is built on Python 2.7 and PyQT 4.8

Additional dependencies include:
* PIL
* pyopencl
* numpy

## INSTALLATION
Other than installing the libraries defined in "Dependencies", no additional installation is required.  
Execution can be done by running 
```
python PyBrot.py
```

## USAGE
PyBrot creates an Image and displays it in a QGRAPHICSVIEW pane.  

One can zoom- in or out interactively using a wheel mouse, however, zooming does not initiate recalculating the image.
Instead, one can zoom and pane to an area of interest with the mouse.  When a region of interest has been identified, one can double click with the left mouse button to recalculate the scene.
* The new image will be centered on the point that was double clicked

The number of interations used to determine if a value exists within the set or not can be changed.  At zoomed in regions, this will give much more detail and show additional fractal designs that are otherwise hidden at low iteration counts.
One can change the number of iterations and click 'Plot' without losing the current range or center point.

One can save the current image to the current working directory by clicking 'Save'.  The filename will be a combination of the current values seen in the GUI.
Should the user want to return to that exact point at a later date, they can put the values directly into the InputBoxes and click 'Plot'.

One can resize the window to make it smaller, but the GraphicsScene is always set to your desktop resolution.  Therefore, clicking save will always result in a "Wallpaper" sized image.

## CONTROLS
PyBrot is designed to be used with a wheel mouse.
* Wheel up: Zoom-in
* Wheel down: Zoom-out - Will not zoom out beyond Default dimensions
* Double left click: recalculate scene.  Point where cursor is at will be the center of the new scene.

Known values of a region of interest can be directly input into the text boxes at the top.  This is most likely when the user has saved an image previously which contains the values of the location in the filename.  Once values are put in, the user need only click 'Plot'

Additionally, when the user has zoomed into a region of interest, very little is seen at low iterations due how few evaluations are done to determine if each value exists in the Mandelbrot set or not.  Once can always increase the number of iterations to get more details and Fractal images at high zoom levels.
Clicking 'Plot' after changing the number of iterations will result in recalculating the scene at the current range of values in the InputBoxes.

Clicking 'Save' will result in saving the current image to a tiff image in the current working directory.  The file name will be a combination of values shown in the input boxes.

##AUTHOR

S. Tootle

##Noteable Code Sources
* [OpenCL](https://github.com/inducer/pyopencl/blob/master/examples/demo_mandelbrot.py) - Function utilizing GPU acceleration
* Thanks to [Shufti](https://github.com/danboid/shufti) - Great foundation for figuring out displaying and interacting with images
