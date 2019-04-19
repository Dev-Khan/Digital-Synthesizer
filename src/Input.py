import pygame


class Keyboard_Handler():
	
	def __init__(self):
		self.state = "keyboard"
		#pygame.init()
		#pygame.display.set_mode((128, 128))
		#self.input_loop()
		
	def input_loop(self):
		running = True
		while running:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					running = False
				if event.type == pygame.KEYDOWN:
					yield event.key
				
				if event.type == pygame.KEYUP:
					yield event.key
		yield -1
				
if __name__ == "__main__":
	handler = Keyboard_Handler()
