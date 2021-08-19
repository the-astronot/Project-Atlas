#import RPi.GPIO as GPIO
import time


a = 11
b = 12
c = 13
d = 15
excitors = [a,b,c,d]

'''
GPIO.setmode(GPIO.BOARD)
GPIO.setup(out1,GPIO.OUT)
GPIO.setup(out2,GPIO.OUT)
GPIO.setup(out3,GPIO.OUT)
GPIO.setup(out4,GPIO.OUT)
'''


def run(): # MAIN
	empty_array = []
	recursive_setup(empty_array)


def recursive_setup(array): # Works
	size = len(array)
	if size == 4: # Full orientation
		print("ARRAY:", array)
		time.sleep(.5)
		#move(100, array)

	else:
		# Get the full list of excitors
		remaining_excitors = excitors.copy()
		# Remove those already used
		for x in array:
			remaining_excitors.remove(x)
		# For all remaining possibilities, append and start over
		for x in remaining_excitors:
			new_array = array.copy()
			new_array.append(x)
			recursive_setup(new_array)


def step_forward(act_array): # Works
	num_active = 0
	for x in act_array:
		if x == 1:
			num_active += 1
	if num_active == 0: # Start her up
		act_array[0] = 1
	elif num_active == 1: # Spread Forward
		active_index = act_array.index(1)
		adv_index = (active_index + 1) % 4
		act_array[adv_index] = 1
	elif num_active == 2: # Release Behind
		index_1 = act_array.index(1)
		index_2 = act_array.index(1,index_1+1)
		if index_2 - index_1 == 1: # Regular Case
			act_array[index_1] = 0
		else: # 7-10 Split
			act_array[index_2] = 0
	return act_array



def step_backward(act_array): # Works
	num_active = 0
	for x in act_array:
		if x == 1:
			num_active += 1
	if num_active == 0: # Start her up
		act_array[0] = 1
	elif num_active == 1: # Spread Backwards
		active_index = act_array.index(1)
		adv_index = (active_index - 1) % 4
		act_array[adv_index] = 1
	elif num_active == 2: # Release Forward
		index_1 = act_array.index(1)
		index_2 = act_array.index(1,index_1+1)
		if index_2 - index_1 == 1: # Regular Case
			act_array[index_2] = 0
		else: # 7-10 Split
			act_array[index_1] = 0
	return act_array


'''
def move(num_steps, wiring_array):
	act_array = [0,0,0,0]
	gpio_vals = [GPIO.LOW, GPIO.HIGH]
	for x in range(abs(num_steps)):
		if num_steps > 0:
			act_array = step_forward(act_array)
		else:
			act_array = step_backward(act_array)
		for y in range(4):
			GPIO.output(wiring_array[y], gpio_vals[act_array[y]])
		time.sleep(.03)
'''


if __name__ == '__main__':
	run()
