# Practical-Exercises-for-the-Ficha-team
Basic Image Parsing and Coco Data Generation

This is not a final version of the code. Things to be done:
- add a main function to scripts, and possibly use argparse to read arguments for execution;
- test the Coco annotation and update the scrip to write file names so it is readable by any COCO viewer.

**Image parsing: image_parser.py**

To run the image_parser script, place the script in the folder
with the raw images.bin file. The final files will be written to
a sub-folder called RgbOut (the folder is created automatically
if the user has not created it).

The python script runs as standard. In the console, go to the
required folder and run the line: *python image_parser.py*



**Data generation: coco_generator.py**

To run the coco_generator script, place the script in the
folder with background.png and object.png. The final files will
be written to a sub-folder called GeneratedData (the folder is
created automatically if the user has not created it).

The python script runs as standard. In the console, go to the
required folder and run the line: *python coco_generator.py*
