import pygame


WHITE = (255, 255, 255)

class GUI:
	
	
	def __init__(self, resoultion=(1280, 720)):
		self.screen = pygame.display.set_mode(resoultion)
		pygame.display.set_caption("Pythesizer")
		
		self.width, self.height = resoultion
		self.clock = pygame.time.Clock()
		
		self.screen.fill(WHITE)
		
		self.keyHandler = Keyboard_Handler()
		
	def drawText(self, msg):
		font = pygame.font.Font('freesansbold.ttf', 100)
		TextSurf, TextRect = text_object(msg, font)
		TextRect.center = ((self.width/2, self.height/2))
		self.screen.blit(TextSurf, TextRect)
	
	
	def start(self):
		pygame.init()
		
	def render(self):
		pygame.display.update()
	
	def stop(self):
		pygame.quit()

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
