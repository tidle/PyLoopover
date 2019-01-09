#!/usr/bin/python3
import pygame
import random
import time

##VARIABLES TO CHANGE
width = 500
height = 500
stats_height = 150
board_size = 5
window_name = "PyLoopover "+str(board_size)+"x"+str(board_size)
scramble_turns = 50
t_round = 3
FPS = 30

##DONT CHANGE THESE BOIS
WHITE = (255,255,255)
BLACK = (0,0,0)
GREEN = (32,200,32)
keys = {"w":0,"a":0,"s":0,"d":0,"q":0}
last_was_Q = False

class Tile:
	def __init__(self,number,s):
		self.number = number
		n = number-1
		self.color = ((n/s)*(255/s),(n%s)*(255/s),128)
	def draw(self,screen,font,x,y,width,height):
		pygame.draw.rect(screen,self.color,(x,y,width,height))
		text = font.render(str(self.number),True,BLACK)
		screen.blit(text,(x,y))

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

	def draw(self,screen,font):
		for i in range(0,self.size):
			for j in range(0,self.size):
				w = (width / self.size)
				h = (height / self.size)
				x = i * w
				y = j * h
				self.content[i][j].draw(screen,font,x,y,w,h)
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

def main():
	gameboard = Board(board_size)
	pygame.init()
	pygame.mixer.quit() #weird workaroud
	#name the window & size it.
	pygame.display.set_caption(window_name)
	screen = pygame.display.set_mode((width,height+stats_height),0,32)
	#setup framerate
	pygame.time.set_timer(pygame.USEREVENT+1,int((1/FPS)*1000))
	#setup event que
	pygame.event.set_allowed(None) #start with no events allowed
	pygame.event.set_allowed(pygame.USEREVENT+1) #timer event
	pygame.event.set_allowed(pygame.KEYDOWN)
	pygame.event.set_allowed(pygame.QUIT) #4 quitters
	#setup fonts
	font = pygame.font.SysFont('mono',int((width/board_size)/1.14))
	font2 = pygame.font.SysFont('mono',int(stats_height/2.3))
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
			time_str = str( int( time[0] * (10 ** t_round) ) / (10 ** t_round) )
			text_timer = font2.render("Time :"+time_str,True,time[1])
			text_moves = font2.render("Moves:"+str(gameboard.moves),True,time[1])
			screen.blit(text_timer,(0,height))
			screen.blit(text_moves,(0,height+(stats_height/2)))
			#draw board
			gameboard.draw(screen,font)

			#update da screeeeeen
			pygame.display.update()

			#end the game
			if gameboard.is_solved() and gameboard.start_t > gameboard.end_t:
				gameboard.end_time()
		elif event.type == pygame.KEYDOWN:
			k = chr(event.key) #gimme a CHAR, not some weird integer
			domap = {
				"w":"gameboard.rotate_up(int(pygame.mouse.get_pos()[0]/(width/board_size)))",
				"a":"gameboard.rotate_right(int(pygame.mouse.get_pos()[1]/(height/board_size)))",
				"s":"gameboard.rotate_down(int(pygame.mouse.get_pos()[0]/(width/board_size)))",
				"d":"gameboard.rotate_left(int(pygame.mouse.get_pos()[1]/(height/board_size)))",
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
			#end the game
			if gameboard.is_solved() and gameboard.start_t > gameboard.end_t:
				gameboard.end_time()
		#for quitters
		elif event.type == pygame.QUIT:
			print("Quitting...")
			running = False
		else:
			print("err0r, bAd 3v3nt lol")
			assert False
if __name__ == "__main__":
	main()
