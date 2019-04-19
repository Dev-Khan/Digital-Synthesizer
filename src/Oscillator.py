from enum import Enum
import numpy as np
import scipy.signal as signal
import pygame 
from pygame.mixer import Channel, Sound, get_init, pre_init

import time

class Waveform(Enum):
	sine = "sine"
	square = "square"
	sawtooth = "sawtooth"
	triangle = "triangle"
	
class Notes(Enum):
	# Start Here
	F4  = (349.23, 0)
	FS4 = (369.99, 1)
	Gb4 = (369.99, 1)
	G4  = (392.00, 2)
	GS4 = (415.30, 3)
	Ab4 = (415.30, 3)
	A4  = (440.00, 4)
	AS4 = (466.16, 5)
	Bb4 = (466.16, 5)
	B4  = (493.88, 6)
	C5  = (523.25, 7)
	CS5 = (554.37, 8)
	Db5 = (554.37, 8)
	D5  = (584.33, 9)
	DS5 = (622.25, 10)
	Eb5 = (622.25, 10)
	E5  = (659.25, 11)
	F5  = (698.46, 12)
	FS5 = (739.99, 13)
	Gb5 = (739.99, 13)
	G5  = (783.99, 14)
	GS5 = (830.61, 15)
	Ab5 = (830.61, 15)
	A5  = (880.00, 16)
	AS5 = (923.33, 17)
	Bb5 = (923.33, 17)
	B5  = (987.77, 18)
	C6  = (1046.50, 19)
	
	def __init__(self, freq, channel):
		self.freq = freq
		self.channel = channel


class Oscillator():#Sound):
	
	def __init__(self, waveform, volume=0.0, freq_transpose=1.0):
		self.waveform = waveform
		self.volume = volume
		self.freq_transpose = freq_transpose
		
		pygame.mixer.set_num_channels(20) # 20 key/notes 
		self.channels = [Channel(x) for x in range(20)]
		
		#self.sound = Sound.__init__(self, buffer=self.generate_wave())
		#self.set_volume(self.volume)
		
		
	def play_osillator(self, adsr, frequencies=[Notes.A4]):
		live_channels = []
		for frequency in frequencies:
			channel = self.channels[frequency.channel] # get the channel object for this note
			#                                                                        attack the sound
			channel.play(Sound(buffer=self.generate_wave(frequency.freq)), loops=-1, maxtime=10000, fade_ms=int(adsr[0]*1000))
			channel.set_volume(self.volume)
			live_channels.append(channel)
			
		
		# What is the different in volume between max volume and the sustain
		sound_delta = self.volume - adsr[2]
		####print(sound_delta)
		# Decay the Sound to sustain level
		while self.volume > adsr[2] and adsr[1] != 0:
			self.volume -= sound_delta/adsr[1] # move the volume down by a rate of sound_delta/time
			for channel in live_channels:
				channel.set_volume(self.volume)
		
		return live_channels
		
		
		
	def volume(self):
		return self.volume
	
	@property
	def _wave_func(self):
		if self.waveform is Waveform.sine:
			return np.sin
		elif self.waveform is Waveform.sawtooth:
			return signal.sawtooth
		elif self.waveform is Waveform.square:
			return signal.square
		elif self.waveform is Waveform.triangle:
			return self.gen_triang
		raise TypeError("Unkown waveform: {0}".format(self.waveform))
		
	@staticmethod
	def gen_triang(t, width=0.5):
		return signal.sawtooth(t, width)
	
	def generate_wave(self, frequency):
		if self.freq_transpose < 0:
			freq = frequency / abs(self.freq_transpose) #frequency/abs(self.freq_transpose)
		elif self.freq_transpose > 0:
			freq = frequency * abs(self.freq_transpose)
		else:
			freq = frequency
			
		print(freq)
		sample_rate = pygame.mixer.get_init()[0]
		period = int(round(sample_rate/freq))
		amplitude = 2 ** (abs(get_init()[1]) - 1 ) -1
		
		
		def frame_value(i):
			return amplitude * self._wave_func(2.0 * np.pi * freq * i / sample_rate)
		
		return np.array([frame_value(x) for x in range(0, period)]).astype(np.int16)
	

if __name__ == "__main__":
	for note in Notes:
		print(round(note.freq%12))
		
	pre_init(44100, -16, 2, 8192)
	#pygame.init()
	pygame.mixer.init()

	o = Oscillator(Waveform.square, volume=0.25)
	o.play_osillator([Notes.C5, Notes.E5, Notes.G5, Notes.C6])
