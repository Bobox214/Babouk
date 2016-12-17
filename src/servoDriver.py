import Adafruit_PCA9685
from  collections import namedtuple

ServoConf = namedtuple('ServoConf',['channel','minAngle','maxAngle','minPwm','maxPwm'])

def constrain(val,minValue,maxValue):
	if val<minValue: return minValue
	if val>maxValue: return maxValue
	return val

class BaboukServo:
	conf = {
		'RL' : (
				ServoConf(channel=1,minAngle=   0,maxAngle=135,minPwm=310,maxPwm=580)
			,	ServoConf(channel=2,minAngle= -90,maxAngle= 90,minPwm=650,maxPwm=150)
			,	ServoConf(channel=0,minAngle=-180,maxAngle=  0,minPwm=630,maxPwm=170)
			)
	,	'RR' : (
				ServoConf(channel=6,minAngle=   0,maxAngle=135,minPwm=540,maxPwm=200)
			,	ServoConf(channel=5,minAngle= -90,maxAngle= 90,minPwm=650,maxPwm=170)
			,	ServoConf(channel=4,minAngle=-180,maxAngle=  0,minPwm=250,maxPwm=650)
			)
	}
	def __init__(self):
		self.pwm = Adafruit_PCA9685.PCA9685()
		self.pwm.set_pwm_freq(60)
		self.servoValues = {}

	def setLeg(self,legName,angles):
		assert legName in ('RL','RR','FL','FR'), 'Unexpeced legName "{legName}"'.format(**locals())
		assert len(angles)==3, 'Expected 3 angles not "{angles}"'.format(**locals())
		for i,angle in enumerate(angles):
			conf = self.conf[legName][i]
			angle = constrain(angle,conf.minAngle,conf.maxAngle)
			pwm = conf.minPwm+(angle-conf.minAngle)*(conf.maxPwm-conf.minPwm)/(conf.maxAngle-conf.minAngle)
			self.servoValues[conf.channel] = int(pwm)
	def apply(self):
		for channel,pwm in self.servoValues.items():
			print('**DBG**',channel,pwm)
			self.pwm.set_pwm(channel,0,pwm)
		self.servoValues = {}

if __name__ == '__main__':
	print("Testing  BaboukServo")
	babouk = BaboukServo()
	import kbHit
	kb = kbHit.KBHit()
	while True:
		if kb.kbhit():
			c = kb.getch()
			if ord(c) == 27: # ESC
				break
			print(c)
			if c == 'i':
				babouk.setLeg('RL',(45,0,-90))
				babouk.setLeg('RR',(45,0,-90))
				babouk.apply()
				
	kb.set_normal_term()
