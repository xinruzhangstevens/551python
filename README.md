INTRODUCTION
===
This project aims to establish a game platform named "AVENGERS-WAR" by module pygame in python. The game rule is that players move the superhero---the Spiderman and the Ironman through the left, right, up, down keys on the keyboard. In addition, the players can destroy the enemy UFO by operating the direction of superheroes until they finally meet the Boss---Thanos. Once players defeat Thanos by shooting bullets, it shows that they win the game and thanos' life is ended. However, if the superheros collides with the enemy UFO or weapons of thanos, it will show the end of the game.

FEATURE
===
Game Initialization
---
* set up window screen
* create time clock
* create sprites and sprite group

Game Loop
---
* set up refreshing frame rate
* monitor events
* collision checking
* update/draw sprite group
* update screen display

TODO
===
Sprites and Sprite Group
---
* define sprites subclass 
* define derive sprite subclass

Build Game Structure
---
* game initialization
* establish window screen by constant 
* build start game program
* realize alternating scrolling of background image
* simplify background implementation by initialization
* monitor exit events and exit games

Enemies
---
* define and monitor timers for creating enemy
* design and prepare enemy class
* timely creation and display of enemy 
* random position and random speed
* delete pictures of enemies out of the screen

Superheroes
---
* prepare hero class
* draw superheroes
* Control the left,right,up,down movement of the hero
* hero’s boundary control

Launch Bullets
---
* add and monitor events(bullets launched by pirate ships)
* define bullets class
* fire three bullets for one time

Collision Check
---
* collision between bullets and enemies
* collision between bullets and boss
* collision between enemies and hero
* collision between hero and weapons

Last Boss
---
* define monster’s class
* add and monitor the fire time of the monster
* add and monitor game winning time

Plan
===
week 1 ~week 3: prepare for the program<br>
week 4: proposal of the project<br>
week 5: build game structure and define sprites and sprite goup<br>
week 6 ~ week 7: create the pirate ship and enemies with bullets launched<br>
week 8 ~ week 9: create the last boss with fire<br>
week 10 ~ week 11: establish collision mode<br>
week 12 ~ week 13: improve and check the whole program<br>
week 14 ~ week 15: submit the final program<br>
