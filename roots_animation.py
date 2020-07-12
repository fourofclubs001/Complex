import pygame as py
import complexn
import math
import cmath
import numpy as np
import complex_animation

# Create plane
grid = (4,4) # rows and colums
center_position = (2,2) # center on grid relative to up left corner
win_scale = (500, 500) # win width and height
plane = complex_animation.Plane(grid, center_position, win_scale)
plane.begin() 

# Create Video_Maker
frames = 1003
fps = 75
video_Maker = complex_animation.Video_Maker("complex_animation.avi","frame", frames, fps)
video_Maker.begin(plane)

# Before loop math
unit_circle = complex_animation.Graph(math.cos, math.sin, 0, 2*math.pi, 0.01)

p = 1 # roots power to graph
n_root = 0 # number of roots

# main loop
run = True
while run:

	# event watcher
	for event in py.event.get():

		if event.type == py.QUIT:

			run = False

	# root calculations
	if p > n_root:

		p = 1 # reset power
		n_root+=1 # add one root to graph

		roots_pos = complexn.unitary_roots(n_root) # calculate roots position on complex plain
		
		# Create roots Points to graph
		roots = []
		for root_pos in roots_pos:

			roots.append(complex_animation.Point(root_pos, (np.random.randint(0, 256),
				                          np.random.randint(0, 256),
				                          np.random.randint(0, 256))))

	# Change roots position with their powers
	moving_roots = roots.copy()

	for i in range(len(roots)):

		moving_roots[i] = complex_animation.Point(complexn.pow(roots[i].z, p), roots[i].color)

	p += 0.01

	# Update plane
	obj = [unit_circle] + moving_roots # Objects to graph
	text = [complex_animation.Text("G{}".format(n_root), complex(-0.7, 0.35),
	        (0,0,0), 'comicsans', 150, True, True)] # text to show

	plane.update(obj, text)

	# save frame image
	video_Maker.save_image(plane)

	# Loop delay
	py.time.delay(10)

plane.quit() # quit pygame
video_Maker.release() # finish video