import Adafruit_PCA9685
import kbHit

pwm = Adafruit_PCA9685.PCA9685()
pwm.set_pwm_freq(60)


def constrain(val,minValue,maxValue):
	if val<minValue: return minValue
	if val>maxValue: return maxValue
	return val

minPwm   = 50
maxPwm   = 1000
curServo = 0
curPwm   = 400

kb = kbHit.KBHit()
print('Hit any key, or ESC to exit')
cmd = ''
while True:
	if kb.kbhit():
		c = kb.getch()
		if ord(c) == 27: # ESC
			break
		if c in ('o','i'):
			if c=='o':
				curPwm = constrain(curPwm+20,minPwm,maxPwm)
			if c=='i':
				curPwm = constrain(curPwm-20,minPwm,maxPwm)
			print('Move Servo {curServo} to {curPwm}'.format(**locals()))
			pwm.set_pwm(curServo,0,curPwm)
		elif c == ';':
			print(c)
			try:
				curServo = int(cmd)
				print('Now driving Servo {curServo}'.format(**locals()))
			except:
				print('Unknown command "{cmd}"'.format(**locals()))
			cmd = ''
		else:
			print(c,)
			cmd += c
kb.set_normal_term()
