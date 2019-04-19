from Oscillator import Waveform, Oscillator, Notes
import numpy as np
import pygame
from pygame.mixer import Channel, Sound, pre_init
from time import sleep
from Recorder import TrackRecorder
from GUI import GUI, Keyboard_Handler
import sys



class Synthesizer:
	
	keyNote = { 113: Notes.F4,  # Q
				50 : Notes.FS4, # 2
				119: Notes.G4,  # W
				51 : Notes.GS4, # 3
				101: Notes.A4,  # E
				52 : Notes.AS4, # 4
				114: Notes.B4,  # R
				116: Notes.C5,  # T
				54 : Notes.CS5, # 6
				121: Notes.D5,  # Y
				55 : Notes.DS5, # 7
				117: Notes.E5,  # U
				105: Notes.F5,  # I
				57 : Notes.FS5, # 9
				111: Notes.G5,  # O
				48 : Notes.GS5, # 0
				112: Notes.A5,  # P
				45 : Notes.AS5, # -
				91 : Notes.B5,  # [
				93 : Notes.C6}  # ]
	
	def __init__(self, osc1_waveform=Waveform.sine, osc1_volume=0.25, rate=44100):
		# initilizie pygame gubs
		pre_init(rate, -16, 2, 4096)
		pygame.init()
		#pre_init(rate, -16, 2, 4096)
		#pygame.mixer.init()
		self.rate = rate
		
		self.adsr = [0.0, 0.5, 0.015, 9.0] # In seconds, except s (volume level [0.0, 1.0])
		self.live_channels = []
		
		# Object Handlers
		self.osc1 = Oscillator(waveform=osc1_waveform, volume=osc1_volume, freq_transpose=-2.0)
		
		self.gui = GUI()
		#self.key_handler = Keyboard_Handler()
		#self.recorder = TrackRecorder()
		



	def adsr(self, delta=[0, 0, 0, 0]):
		for i in len(adsr):
			adsr[i] += delta[i]
		
		
	def play(self, freq=[Notes.A4]):
		self.live_channels.extend(self.osc1.play_osillator(self.adsr, frequencies=freq))

	def release(self, freq=None):
		
		if freq:
			Channel(freq.channel).fadeout(int(self.adsr[3]*1000))
		
	def main_loop(self):
		
		active = []
		quit = False
		self.gui.start()
		while not quit:
			for key in self.gui.keyHandler.input_loop():
				print("Update")
				print(key)
				if key == -1:
					quit = True
					break
				else:
					try:
						print(key)
						note = self.keyNote[key]
						if note:
							if key in active:
								self.release(note)
								active.remove(key)
							else:
								self.play([note])
								active.append(key)
					except KeyError:
						print("{0} is not a supported key".format(key))
		
		self.gui.stop()
		


	
	
if __name__ == "__main__":
	synth = Synthesizer(osc1_waveform=Waveform.sine)
	synth.main_loop()
	print("here")
	#synth._audio_stream.play_wave(synth.generate_constant_wave(261.6, 3.0)) # Hz, Duration | Middle C, 3s
	
