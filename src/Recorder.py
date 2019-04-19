import sounddevice as sd
import jack
from scipy.io import wavfile
#https://jackclient-python.readthedocs.io/en/0.4.6/

class TrackRecorder():
	
	def __init__(self, device='default', rate=44100):
		self.client = jack.Client("Pythniszer")
		self.inport = self.client.inports.register('input_1')
		self.outport = self.client.outports.register('output_1')
		
		self.client.activate()
		self.client.connect('system:capture_1', 'Pythniszer:input_1')
		self.client.connect('Pythniszer:output_1', 'system:playback_1')
		
		self.device = device
		self.rate = rate
		self.recording = None
		
		sd.default.samplerate = rate
		sd.default.device = self.device
		sd.default.channels = 2
		#print(self.client.get_ports())
		print(sd.query_devices())
		
	def record(self, duration):
		self.recording = sd.rec(int(duration*self.rate))
	
	def playback(self):
		print("Wait")
		sd.wait()
		self.writeData()
		print("Sound Ready")
		print(self.recording)
		sd.play(self.recording, self.rate)
		
	def writeData(self):
		wavfile.write("temp.wav", self.rate, self.recording)
