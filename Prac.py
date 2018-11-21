import pygame as pg
import time
import random

pg.init()

display_width = 800
display_height = 600

black = (0,0,0)
white = (255,255,255)
blockColor = (53,115,255)

red = (200,0,0,)
green = (0,200,0)
blue = (0,0,255)

b_red = (255,0,0)
b_green = (0,255,0)

car_width = 59

gameDisplay = pg.display.set_mode((display_width,display_height))
pg.display.set_caption('Run for life')
clock = pg.time.Clock()

carImg = pg.image.load("C:\\Users\\Sanyog\\Desktop\\Man.png")

def thingsDodged(count):
	font = pg.font.SysFont(None, 25)
	text = font.render("Dodged : "+ str(count),True,black)
	gameDisplay.blit(text,(0,0))

def things(thingx,thingy,thingw,thingh,color,thingc):
	for i in range(thingc):
		pg.draw.rect(gameDisplay,color,[thingx,thingy,thingw,thingh])

def car(x,y):
	gameDisplay.blit(carImg,(x,y))

def textOjects(text,font):
	textSurface = font.render(text,True,black)
	return textSurface,textSurface.get_rect()

def messageDisplay(text):
	largeText = pg.font.Font('freesansbold.ttf',115)
	TextSurf,TextRect = textOjects(text,largeText)
	TextRect.center = ((display_width//2,display_height//2))
	gameDisplay.blit(TextSurf,TextRect)

	pg.display.update()
	time.sleep(2)

	gameLoop()

def crashGame():
	messageDisplay("You Crashed")

def button(msg,x,y,w,h,i,a,action = None):
	mouse = pg.mouse.get_pos()
	click = pg.mouse.get_pressed()

	if x + w > mouse[0] > x and y + h > mouse[1] > y:
		pg.draw.rect(gameDisplay,a,(x,y,w,h))
		if click[0] == 1 and action != None:
			action()
	else:
		pg.draw.rect(gameDisplay,i,(x,y,w,h))

	smallText = pg.font.Font('freesansbold.ttf',25)
	TextSurf,TextRect = textOjects(msg,smallText)
	TextRect.center =( (x + (w // 2)) , (y + (h // 2)) )
	gameDisplay.blit(TextSurf,TextRect)

def gameIntro():
	intro = True
	while intro:
		for events in pg.event.get():
			if events.type == pg.QUIT:
				pg.quit()
				quit()
		gameDisplay.fill(white)
		largeText = pg.font.Font('freesansbold.ttf',45)
		TextSurf,TextRect = textOjects("Welcome to Racey",largeText)
		TextRect.center = ((display_width - 400,display_height//4))
		gameDisplay.blit(TextSurf,TextRect)

		
		button("GO!", 250, 300, 100, 50, green,b_green,gameLoop)
		button("Exit!", 450, 300, 100, 50, red, b_red,)
	
		pg.display.update()
		clock.tick(15)


def gameLoop():
	x = (display_width * 0.45)
	y = (display_height * 0.78)

	x_change = 0
	thing_startx = random.randrange(0,display_width)
	thing_starty = -600
	thing_speed = 5
	thing_width = 100
	thing_height = 100
	thing_count = 1

	Dodged = 0

	gameExit = False
	while not gameExit:

		for events in pg.event.get():
			if events.type == pg.QUIT:
				pg.quit()
				quit()

			if events.type == pg.KEYDOWN:
				if events.key == pg.K_LEFT:
					x_change = -5
				if events.key == pg.K_RIGHT:
					x_change = 5

			if events.type == pg.KEYUP:
				if events.key == pg.K_LEFT or events.key == pg.K_RIGHT:
					x_change = 0


		x += x_change
		gameDisplay.fill(white)

		things(thing_startx, thing_starty, thing_width, thing_height, blockColor,thing_count)
		
		thing_starty += thing_speed
		car(x, y)
		thingsDodged(Dodged)
		
		if x > display_width - car_width  or x < 0:
			crashGame()
		
		if thing_starty > display_height:
			thing_starty = 0 - thing_height
			thing_startx = random.randrange(0,display_width)
			Dodged += 1
			thing_speed += 0.5
			thing_width += Dodged*1.2

		if thing_starty + thing_height > y :
			if x > thing_startx and x < thing_startx + thing_width or x + car_width > thing_startx and x + car_width < thing_startx + thing_width:
				crashGame()

		pg.display.update()
		clock.tick(60)
gameIntro()
gameLoop()
pg.quit()
