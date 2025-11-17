This repository contains a double pendulum project. 

#Goal
The goal of this project is to write a double pendulum simulation, while writing some nice reusable code, learning a new library, improving upon shortcomings of similarly scoped projects on itch.io and improving python

#Why a double pendulum?
The idea started out from writing a double pendulum simulation in numpy with linear algebra for a university course. It slowly transformed into exploring other more profesional options. 
Drawing on earlier experiences with low level graphics engines as raylib and pygame, the natural choice was to look for a python physics library that can be used with pygame. The solution was found in pymunk.
As the project started out in python it has remained in python. 


#Challenge
Although pymunk has drawing options to draw objects in pygame and handles all the physics, it really does not contain any functions to construct or draw more complex scenes.
Both pygame and pymunk leave handling, drawing, translating and implementing more complex functions to the user. 
The challenge here lies in writing a resuable section of code that handles:

1. Adding any number of physics objects and keeping track of them
2. Making slightly more complex objects.
3. A simple camera system that can follow any object.
4. making a nearly infinite world
5. Wherein the code to handle this should be reusable and expandable in the future. 
6. This naturally meant exploring classes and inheritance and learning a new library.


#Shortcomings of other physics programs on itch.io
Some brief exploration of other physics based projects was done on itch.io of similar scope. it was found that hobby projects where not that good.

-Objects where not interactable with the mouse and sometimes even the keyboard.
-No textures where used.
-If it was physics puzzler, it had no overview of levels.
-If it was a game where you control an object
    -you'd get stuck often
    -no room for errors, tight collision
-No clear controls where provided.
-No goal was provided.
-Most often there was no proper camera implemented.
