# snake game where the snake (head, tail, middle, corners) is made of png images made with microsoft paint
# i tried to make the game a little bit difficult by increasing the speed of the snake and by moving the food each 30 moves 
# please let me know how i can improve my code and if you like my game project feel free to modify or use it
# contact me at idriss.el.moussaouiti@gmail.com 

import pygame 
from pygame.locals import *
from random import randint
import os

dirname = os.path.dirname(__file__)
pygame.init()
speed = [50,70,90,110,130] # list of possible speeds, each element is the number of milliseconds the program waits before a move
continuer = 0 # pygame main loop 
# the screen "600x600" is divided into 30*30 squares
# the snake parts (head, tail, middle, corners) are 30*30 png images
# the snake is represented as a list of logical positions ex : [2,1] or [10,7] 
# i use the logical position to calculate the actual position on the screen where to draw the png image of the snake part (see function "reality()") 
# to draw the corners aproprietly i made up a concept of a snake part direction
# direction 0 is down, 1 is left, 2 is right, 3 is up 
# 5 means same as the next direction in the list 
# snake_direction variable is the general direction of the snake
# direction list is the list of direction of the snake parts 
# tail_pos serves the same concept but only for the tail 
# move_counter tells when i need to change the tail image direction
snake_direction = 2
direction = [2,5,5,2]
snake = [[1,1],[2,1],[3,1],[4,1]]
tail_pos = [2]
move_counter = 0
# The 6 variable below are not for the snake but for changes in the game in general
moves = [0,0,0,0] # tells wich key is pressed (up,down,left,right), i use this list so as to when the user presses a key the snake keeps moving while the key is pressed
eat = 0 # when the snake eats, i use this variable for the snake to open it's mouth
lock = 0 # game over variable, to draw the game over menu
highscore = 0 # keeps track of scores during the game
clicked = 0 # if the user clicks the new game button
diff = 0 # after each move diff is incremented and when it reachs 30 the position of the food is changed and diff is assigned 0 - modulo
fenetre = pygame.display.set_mode((610,650)) # game screen
myfont = pygame.font.SysFont('arial', 25) # normal text
myotherfont = pygame.font.SysFont('arial', 80) # titles
snake_thumb = pygame.image.load("thumbnail-snake.png")
pygame.display.set_icon(snake_thumb)
pygame.display.set_caption("Animated Snake Game")
# list of tail images in different directions
tail = [pygame.image.load("image\snake_p_tail_d_30.png").convert(),pygame.image.load("image\snake_p_tail_l_30.png").convert(),pygame.image.load("image\snake_p_tail_r_30.png").convert(),pygame.image.load("image\snake_p_tail_u_30.png").convert()]
# list of normal snake head images in different directions
head_m = [pygame.image.load("image\snake_p_m_d_30.png").convert(),pygame.image.load("image\snake_p_m_l_30.png").convert(),pygame.image.load("image\snake_p_m_r_30.png").convert(),pygame.image.load("image\snake_p_m_u_30.png").convert()]
# list of eating snake head images in different directions
head_eat = [pygame.image.load("image\snake_p_eat_d_30.png").convert(),pygame.image.load("image\snake_p_eat_l_30.png").convert(),pygame.image.load("image\snake_p_eat_r_30.png").convert(),pygame.image.load("image\snake_p_eat_u_30.png").convert()]
# list of snake parts with no corners 
snake_parts = [pygame.image.load("image\snake_p_1_30.png").convert(),pygame.image.load("image\snake_p_2_30.png").convert(),pygame.image.load("image\snake_p_3_30.png").convert(),pygame.image.load("image\snake_p_4_30.png").convert(),pygame.image.load("image\snake_p_5_30.png").convert()]
# list of corner snake parts 
snake_moves = [pygame.image.load("image\snake_p_d_30.png").convert(),pygame.image.load("image\snake_p_l_30.png").convert(),pygame.image.load("image\snake_p_r_30.png").convert(),pygame.image.load("image\snake_p_u_30.png").convert()]
food = pygame.image.load("image\\maca.png") # image of food


def make_food(): # generate random position for food, check if new position is valid (not a snake or food position )
	global snake
	global food_pos
	ingrediants = [randint(0,19),randint(0,19)]
	while ((ingrediants in snake) or (ingrediants == food)):
		ingrediants = [randint(0,19),randint(0,19)]
	return ingrediants
	
food_pos = make_food()

def reality(pos): # turn logical position into actual image position on the screen 
	return [29*pos[0],29*pos[1]]

def move_r(): # snake move right , i will comment this function. all 3 function below are the same 
	global snake 
	global snake_direction
	global direction
	global tail_pos
	global move_counter
	global food_pos
	global eat
	global lock
	global diff
	rel_food = food_pos # store food position because it might change 
	if snake_direction != 1: # this function is move right, if the snake is moving left do nothing (left is 1)
		new_snake_part = [(snake[-1][0]+1)%21,snake[-1][1]] # generate the next position for snake head
		if new_snake_part not in snake: # if the new position is already part of the snake, the game ends
			diff = (diff + 1)%31 # increment the number of moves by 1, if equal 30 return to 0 
			if new_snake_part != food_pos: # check if the snake is about to eat, if not  
				snake.pop(0) # the last snake part is removed
				direction.pop(0) # the last element of direction list is also removed 
				eat = 0 # if the snake ate in the last move, return eat to 0 
			else: # the snake is about to eat
				food_pos = make_food() # generate new position for food
				eat = 1 # assign 1 to variable eat, to draw eating snake head
				diff = 0 # assign 0 to number of moves 
			snake.append(new_snake_part) # the snake advances in the right direction
			direction.append(2) # add right direction to eat, 2 is right 
			if snake_direction == 2: # if the snake is moving in the right direction 
				direction[-2] = 5 # assign 5 to the snake part directon after the head
			elif snake_direction == 3: # if the snake was moving in the up direction
				direction[-2] = 1 # the snake part after the head is assigned image 1 in the list snake_moves
			elif snake_direction == 0: # same as function above for direction down
				direction[-2] = 3
			snake_direction = 2 # a new snake general direction is assigned - right in this case 
			if tail_pos[-1] != 2: # add the new tail position if it is not already in the list 
				tail_pos.append(2)
			if new_snake_part != rel_food: # assign the new tail direction in the direction list according to the move_counter variable
				if direction[0] == 5:
					direction[0] = tail_pos[move_counter]
				else :
					move_counter = move_counter + 1
					direction[0] = tail_pos[move_counter]
		else:
			lock = 1

def move_d():
	global snake 
	global snake_direction
	global direction
	global tail_pos
	global move_counter
	global food_pos
	global eat
	global lock
	global diff
	rel_food = food_pos
	if snake_direction != 3:
		new_snake_part = [snake[-1][0],(snake[-1][1]+1)%21]
		if new_snake_part not in snake:
			diff = (diff + 1)%31
			if new_snake_part != food_pos:
				snake.pop(0)
				direction.pop(0)
				eat = 0
			else:
				food_pos = make_food()
				eat = 1
				diff = 0
			snake.append(new_snake_part)
			direction.append(0)
			if snake_direction == 0:
				direction[-2] = 5
			elif snake_direction == 2:
				direction[-2] = 0
			elif snake_direction == 1:
				direction[-2] = 1
			snake_direction = 0
			if tail_pos[-1] != 0:
				tail_pos.append(0)
			if new_snake_part != rel_food:
				if direction[0] == 5:
					direction[0] = tail_pos[move_counter]
				else :
					move_counter = move_counter + 1
					direction[0] = tail_pos[move_counter]
		else:
			lock = 1

def move_l():
	global snake 
	global snake_direction
	global direction
	global tail_pos
	global move_counter
	global food_pos
	global eat
	global lock
	global diff
	rel_food = food_pos
	if snake_direction != 2:
		new_snake_part = [(snake[-1][0]-1)%21,snake[-1][1]]
		if new_snake_part not in snake:
			diff = (diff + 1)%31
			if new_snake_part != food_pos:
				snake.pop(0)
				direction.pop(0)
				eat = 0
			else:
				food_pos = make_food()
				eat = 1
				diff = 0
			snake.append(new_snake_part)			
			direction.append(1)
			if snake_direction == 1:
				direction[-2] = 5
			elif snake_direction == 3 :
				direction[-2] = 0
			elif snake_direction == 0 :
				direction[-2] = 2
			snake_direction = 1
			if tail_pos[-1] != 1:
				tail_pos.append(1)
			if new_snake_part != rel_food:
				if direction[0] == 5:
					direction[0] = tail_pos[move_counter]
				else :
					move_counter = move_counter + 1
					direction[0] = tail_pos[move_counter]
		else:
			lock = 1
		
def move_u():
	global snake 
	global snake_direction
	global direction
	global tail_pos
	global move_counter
	global food_pos
	global eat
	global lock
	global diff
	rel_food = food_pos
	if snake_direction != 0:
		new_snake_part = [snake[-1][0],(snake[-1][1]-1)%21]
		if new_snake_part not in snake:
			diff = (diff + 1)%31
			if new_snake_part != food_pos:
				snake.pop(0)
				direction.pop(0)
				eat = 0
			else :
				food_pos = make_food()
				eat = 1
				diff = 0
			snake.append(new_snake_part)
			direction.append(3)
			if snake_direction == 3:
				direction[-2] = 5
			elif snake_direction == 2 :
				direction[-2] = 2
			elif snake_direction == 1 :
				direction[-2] = 3
			snake_direction = 3
			if tail_pos[-1] != 3:
				tail_pos.append(3)
			if new_snake_part != rel_food:
				if direction[0] == 5:
					direction[0] = tail_pos[move_counter]
				else :
					move_counter = move_counter + 1
					direction[0] = tail_pos[move_counter]
		else :
			lock = 1
	
	
def show_snake(): # draw snake on the screen 
	global snake
	global direction
	global fenetre
	global tail
	global head_m
	global snake_parts
	global snake_moves
	global eat
	global points
	global clicked
	global diff
	global highscore
	pygame.draw.rect(fenetre, (250,240,230), [0,0,600,600]) # paint the screen white
	fenetre.blit(food, reality(food_pos)) # draw the food
	fenetre.blit(tail[direction[0]], reality(snake[0])) # draw the tail
	if eat == 0: # check if the snake is eating or not and draw the head accordingly
		fenetre.blit(head_m[direction[-1]], reality(snake[-1])) 
	else:
		fenetre.blit(head_eat[direction[-1]], reality(snake[-1]))
	for position, move in zip(snake[1:len(snake)-1], direction[1:len(direction)-1]): #draw the middle parts of the snake 
		if move == 5: # if the direction of the part is 5, draw a normale square 
			fenetre.blit(snake_parts[randint(0,len(snake_parts)-1)], reality(position))
		else: # else draw a square with a corner, depending on the direction list
			fenetre.blit(snake_moves[move], reality(position))
	pygame.draw.rect(fenetre, (255,255,0), [0,600,600,50]) # draw the message box down
	pygame.draw.rect(fenetre, (255,69,0), [600,0,10,600]) # draw the entire move counter in red
	pygame.draw.rect(fenetre, (255,69,0), [600,600,10,50]) # draw a white rectangle in the bottom right of the screen
	textsurface = myfont.render(f'Placar : '+str(len(snake)-4), False, (199,21,133)) # print the current score
	fenetre.blit(textsurface, (5, 605))
	if lock == 1: # if the user has lost draw the menu
		if highscore < len(snake)-4:
			highscore = len(snake)-4
		pygame.draw.rect(fenetre, (250,128,114), [90,90,420,430])
		pygame.draw.rect(fenetre, (216,191,216), [100,100,400,410])
		textsurface = myotherfont.render('PERDEU', False, (0,0,0))
		fenetre.blit(textsurface, (150, 105))
		textsurface = myfont.render('Seu resultado : '+str(len(snake)-4), False, (0,0,0))
		fenetre.blit(textsurface, (200, 200))
		textsurface = myfont.render('Seu melhor resultado: '+str(highscore), False, (0,0,0))
		fenetre.blit(textsurface, (194, 260))
		textsurface = myfont.render('Para jogar novamente clique aqui', False, (0,0,0))
		fenetre.blit(textsurface, (112, 320))
		pygame.draw.circle(fenetre, (255,0,0), [290,430], 60)
		pygame.draw.circle(fenetre, (255,0,0), [290,430], 50)
		if clicked == 1: # if the user clicks on the button, color the button red
			pygame.draw.circle(fenetre, (0,255,0), [290,430], 60)
	pygame.draw.rect(fenetre, (0,0,255), [600,0,10,20*diff]) # draw part of the move counter in blue

show_snake() # initial snake drawing
pygame.display.flip()
while continuer == 0:
	for event in pygame.event.get():
		if event.type == QUIT:
			continuer = 1
		if event.type == KEYDOWN and lock == 0:
			if event.key == K_RIGHT or event.key == K_d:
				moves[0] = 1
			if event.key == K_DOWN or event.key == K_s:
				moves[1] = 1
			if event.key == K_LEFT or event.key == K_a:
				moves[2] = 1
			if event.key == K_UP or event.key == K_w:
				moves[3] = 1
		if event.type == KEYUP:
			moves = [0,0,0,0]
		if event.type == MOUSEBUTTONDOWN and lock == 1:
			if (event.pos[0]<340 and event.pos[0]>240) and (event.pos[1]<480 and event.pos[1]>380):
				clicked = 1
				show_snake()
				pygame.display.flip()
		if event.type == MOUSEBUTTONUP and lock == 1:
			if (event.pos[0]<340 and event.pos[0]>240) and (event.pos[1]<480 and event.pos[1]>380):
				snake_direction = 2
				direction = [2,5,5,2]
				snake = [[1,1],[2,1],[3,1],[4,1]]
				tail_pos = [2]
				move_counter = 0
				moves = [0,0,0,0]
				eat = 0
				lock = 0
				clicked = 0
				diff = 0
				show_snake()
				pygame.display.flip()
	if moves[0] == 1:
		if eat == 0:
			pygame.time.wait(speed[2])
		else :
			pygame.time.wait(speed[3])
		move_r()
		show_snake()
		pygame.display.flip()
	if moves[1] == 1:
		if eat == 0:
			pygame.time.wait(speed[2])
		else :
			pygame.time.wait(speed[3])
		move_d()
		show_snake()
		pygame.display.flip()
	if moves[2] == 1:
		if eat == 0:
			pygame.time.wait(speed[2])
		else :
			pygame.time.wait(speed[3])
		move_l()
		show_snake()
		pygame.display.flip()
	if moves[3] == 1:
		if eat == 0:
			pygame.time.wait(speed[2])
		else :
			pygame.time.wait(speed[4])
		move_u()
		show_snake()
		pygame.display.flip()
	if diff == 30:
		food_pos = make_food()
			