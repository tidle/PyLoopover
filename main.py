#!/usr/bin/env python3
import pygame
import random
import time
import config
import version

##VARIABLES TO CHANGE
version = version.version
width = config.width
height = config.height
stats_height = config.stats_height
stats_width = config.stats_width
board_size = config.default_board_size
window_name = config.window_name.format(version=version)
scramble_turns = 100
t_round = config.timer_accuracy
FPS = config.FPS
tilemode = 1

##DONT CHANGE THESE BOIS
WHITE = (255,255,255)
BLACK = (0,0,0)
GREEN = (32,200,32)
ORANGE= (250,50,20)
PURPLE= (220,20,250)
GRAY  = (50,220,190)
keys = {"w":0,"a":0,"s":0,"d":0,"q":0}
mouse = {"state":[False,False,False],"sticky":[0,0]}

class Tile:
	def __init__(self,number,s):
		self.number = number
		n = number-1
		red = int(n%s) * (250/s)
		blu = 150 - int(n%s) * (100/s)
		gre = int(n/s) * (250/s)
		self.color = (red,gre,blu)
	def draw(self,screen,font,x,y,width,height,mode):
		if width / config.width != width // config.width:
			width += 1
		if height / config.height != height // config.height:
			height += 1
		display = ""
		if mode == 0: #numbers mode
			display = str(self.number)
		if mode == 1: #letters mode
			display = chr(ord("A")+self.number-1)
		pygame.draw.rect(screen,self.color,(x,y,width,height))
		text = font.render(display,True,BLACK)
		textrect = text.get_rect()
		textrect.centerx = x + width/2
		textrect.centery = y + width/2
		screen.blit(text,textrect)

class Board:
	content = []
	start_t=0
	end_t=0
	game=False
	moves = 0
	def __init__(self,size):
		self.size = size
		for i in range(0,size):
			self.content.append([])
			for j in range(0,size):
				self.content[i].append(None)
				self.content[i][j] = Tile(i+j*size+1,size)
	def rotate_left(self,y):
		new = []
		for i in range(0,self.size):
			new.append(self.content[(i-1)%self.size][y])
		for i in range(0,self.size):
			self.content[i][y] = new[i]
		self.moves+=1
		return new
	def rotate_right(self,y):
		new = []
		for i in range(0,self.size):
			new.append(self.content[(i+1)%self.size][y])
		for i in range(0,self.size):
			self.content[i][y] = new[i]
		self.moves+=1
		return new
	def rotate_down(self,x):
		new = []
		for i in range(0,self.size):
			new.append(self.content[x][(i-1)%self.size])
		for i in range(0,self.size):
			self.content[x][i] = new[i]
		self.moves+=1
		return new
	def rotate_up(self,x):
		new = []
		for i in range(0,self.size):
			new.append(self.content[x][(i+1)%self.size])
		for i in range(0,self.size):
			self.content[x][i] = new[i]
		self.moves+=1
		return new

	def draw(self,screen,font,mode):
		for i in range(0,self.size):
			for j in range(0,self.size):
				w = (width / self.size)
				h = (height / self.size)
				x = i * w
				y = j * h
				self.content[i][j].draw(screen,font,x,y,w,h,mode)
	def scramble(self,n):
		for i in range(0,n):
			o = random.randint(0,3)
			if o == 0:
				self.rotate_left(random.randint(0,board_size-1))
			elif o == 1:
				self.rotate_right(random.randint(0,board_size-1))
			elif o == 2:
				self.rotate_up(random.randint(0,board_size-1))
			else:
				self.rotate_down(random.randint(0,board_size-1))
		self.game=False
		self.moves=0
		return True
	def is_solved(self):
		for i in range(0,self.size):
			for j in range(0,self.size):
				if self.content[i][j].number != i+j*self.size+1:
					return False
		return True
	def start_time(self):
		print("time has started")
		self.start_t = time.monotonic()
		self.game = True
		return self.start_time
	def end_time(self):
		print("time has ended")
		self.end_t = time.monotonic()
		return self.end_time
	def get_time(self):
		if (not self.is_solved()) and self.game:
			return (time.monotonic() - self.start_t , BLACK)
		elif self.is_solved() and self.game:
			return (self.end_t - self.start_t , GREEN)
		else:
			return (0 , BLACK)

def mouse_to_tile(x,y,w,h,s):
	global board_size
	xx = int(x/(w/s))
	yy = int(y/(h/s))
	if xx >= board_size:
		xx = board_size-1
	if yy >= board_size:
		yy = board_size-1
	return (xx,yy)

def average(n,solves):
	m = solves[-n:]
	for i in range(len(m)):
		m[i] = m[i][0]
	m = sorted(m)
	m = m[1:-1] # remove outliers
	s = 0
	for i in m:
		s = s + i
	return s/(n-2)

def main():
	global board_size
	global tilemode
	solves = []
	last_was_Q = False
	gameboard = Board(board_size)
	pygame.init()
	pygame.mixer.quit() #weird workaroud
	#name the window & size it.
	pygame.display.set_caption(window_name)
	screen = pygame.display.set_mode((width+stats_width,height+stats_height),0,32)
	#setup framerate
	pygame.time.set_timer(pygame.USEREVENT+1,int((1/FPS)*1000))
	#setup event que
	pygame.event.set_allowed(None) #start with no events allowed
	pygame.event.set_allowed(pygame.USEREVENT+1) #timer event
	pygame.event.set_allowed(pygame.KEYDOWN)
	pygame.event.set_allowed(pygame.QUIT) #4 quitters
	pygame.event.set_allowed(pygame.MOUSEBUTTONDOWN)
	pygame.event.set_allowed(pygame.MOUSEBUTTONUP)  #mouse stuff
	#setup fonts
	font = pygame.font.Font('Inconsolata-Regular.ttf',int((width/board_size)/1.14))
	font2 = pygame.font.Font('Inconsolata-Regular.ttf',int(stats_height/2.3))
	font3 = pygame.font.Font('Inconsolata-Regular.ttf',int(stats_width/6))
	#main l00p
	running = True
	while running:
		#eevveeentttss???
		event = pygame.event.wait()
		if event.type == pygame.USEREVENT+1:
			#a fresh canvas
			screen.fill(WHITE)

			#draw stats
			time = gameboard.get_time()
			time_str =  "{0:0{r_round}.{t_round}f}".format(time[0],t_round=t_round,r_round=1+t_round+3)
			ao5 = average(5,solves)
			if len(solves) < 5:
				ao5="N/A"
			else:
				ao5 = "{0:0{r_round}.{t_round}f}".format(ao5,t_round=t_round,r_round=1+t_round+3)
			try:
				mps = "{0:0{r}.{t}f}".format(time[0] / gameboard.moves,r=4,t=2)
			except ZeroDivisionError:
				mps = "-"
			mps = mps + "mps"
			#draw history
			line_sep = stats_width/8
			b = [0] * len(solves)
			mtl = [0] * len(solves)
			mml = [0] * len(solves)
			for i in range(len(solves)):
				b[i] = "{0:0{r_round}.{t_round}f}/{1:03}".format(solves[len(solves)-i-1][0],solves[len(solves)-i-1][1],t_round=t_round,r_round=t_round+4)
			for i in range(len(solves)):
				mtl[i] = solves[i][0]
				mml[i] = solves[i][1]
			try:
				mt = min(mtl)
				mm = min(mml)
			except ValueError:
				mt = 0
				mm = 0
			for i in range(len(b)):
				if solves[len(solves)-i-1][0] <= mt:
					r = font3.render(b[i],True,GREEN)
				elif solves[len(solves)-i-1][1] <= mm:
					r = font3.render(b[i],True,GRAY)
				elif i < 5:
					r = font3.render(b[i],True,ORANGE) #visual indication that it will be included in the ao5
				else:
					r = font3.render(b[i],True,BLACK)
				screen.blit(r,(width,line_sep*(i+5)))
			#draw some info
			info1 = font3.render("E-smaller",True,ORANGE)
			info2 = font3.render("R-larger",True,PURPLE)
			info3 = font3.render("Q-scramble",True,GREEN)
			info5 = font3.render("F-tile mode",True,GRAY)
			info4 = font3.render("History:",True,BLACK)
			screen.blit(info1,(width,0))
			screen.blit(info2,(width,line_sep))
			screen.blit(info3,(width,line_sep*2))
			screen.blit(info5,(width,line_sep*3))
			screen.blit(info4,(width,line_sep*4))
			#render boring stuff
			text_timer = font2.render(time_str,True,time[1])
			text_moves = font2.render(str(gameboard.moves).zfill(3),True,time[1])
			text_ao5   = font2.render(ao5,True,ORANGE)
			text_mps   = font2.render(mps,True,PURPLE)
			screen.blit(text_timer,(0,height))
			screen.blit(text_moves,(0,height+(stats_height/2)))
			screen.blit(text_ao5,(width/2,height))
			screen.blit(text_mps,(width/2,height+(stats_height/2)))

			#draw board
			if board_size < 6:
				gameboard.draw(screen,font,tilemode)
			else:
				gameboard.draw(screen,font,0)

			#draggy stuff
			m = mouse_to_tile(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1],width,height,board_size)
			if m != mouse["sticky"] and mouse["state"][0]:
				if m[0] > mouse["sticky"][0] and m[1] == mouse["sticky"][1]:
					gameboard.rotate_left(m[1])
				if m[0] < mouse["sticky"][0] and m[1] == mouse["sticky"][1]:
					gameboard.rotate_right(m[1])
				if m[1] > mouse["sticky"][1] and m[0] == mouse["sticky"][0]:
					gameboard.rotate_down(m[0])
				if m[1] < mouse["sticky"][1] and m[0] == mouse["sticky"][0]:
					gameboard.rotate_up(m[0])
				mouse["sticky"] = m
				if last_was_Q:
					gameboard.start_time()
					last_was_Q = False
			#update da screeeeeen
			pygame.display.update()

			#end the game
			if gameboard.is_solved() and gameboard.start_t > gameboard.end_t:
				gameboard.end_time()
				solves.append([gameboard.get_time()[0],gameboard.moves])
		elif event.type == pygame.KEYDOWN:
			k = chr(event.key) #gimme a CHAR, not some weird integer
			domap = {
				"w":"gameboard.rotate_up(mouse_to_tile(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1],width,height,board_size)[0])",
				"a":"gameboard.rotate_right(mouse_to_tile(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1],width,height,board_size)[1])",
				"s":"gameboard.rotate_down(mouse_to_tile(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1],width,height,board_size)[0])",
				"d":"gameboard.rotate_left(mouse_to_tile(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1],width,height,board_size)[1])",
				"q":"gameboard.scramble(scramble_turns)"
			} #i guess?
			if k in ['w','a','s','d','q']:
				#starting game logic
				if k == "q":
					last_was_Q = True
				else:
					if last_was_Q:
						gameboard.start_time()
						last_was_Q = False
				exec(domap[k])
			if k in ['e','r']: #change board size
				if k == 'r' and board_size < 9:
					cdr = 1
				elif k == 'e' and board_size > 2:
					cdr = -1
				else:
					cdr = 0
				board_size = board_size + cdr
				gameboard = Board(board_size)
				font = pygame.font.Font('Inconsolata-Regular.ttf',int((width/board_size)/1.14))
				solves = []
			if k == 'f':
				tilemode = 1 - tilemode
			#end the game
			if gameboard.is_solved() and gameboard.start_t > gameboard.end_t:
				gameboard.end_time()
				solves.append([gameboard.get_time()[0],gameboard.moves])
		elif event.type == pygame.MOUSEBUTTONDOWN:
			mouse["state"] = pygame.mouse.get_pressed()
			mouse["sticky"] = mouse_to_tile(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1],width,height,board_size)
		elif event.type == pygame.MOUSEBUTTONUP:
			mouse["state"] = pygame.mouse.get_pressed()
		#for quitters
		elif event.type == pygame.QUIT:
			print("Quitting...")
			running = False
		else:
			print("err0r, bAd 3v3nt lol")
			assert False
if __name__ == "__main__":
	main()
