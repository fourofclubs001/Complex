import pygame as py
import math
import cmath
import numpy as np
import os
import cv2

# Complex number Plane
class Plane:
    # Create a pygame window where different objects can be graph
    # Plane initialization
    def __init__(self, grid, 
    	         center, win_scale):
        
        self.rows = grid[0]
        self.columns = grid[1]
        self.center = center
        self.width = win_scale[0]
        self.height = win_scale[1]
        self.dist_y = self.height//self.rows
        self.dist_x = self.width//self.columns
        
    # Plane begin    
    def begin(self):

        py.init()
        self.win = py.display.set_mode((self.width, self.height))
        py.display.set_caption('Complex animation')
        
    # Plane Update
    def update(self, obj, text):
        
        # background
        self.win.fill((230,230,230))
        
        #Grid
        for i in range(self.rows - 1):
            
            # horizontal
            py.draw.line(self.win, (127, 127, 127), 
                         (0, (i + 1) * self.dist_y), 
                         (self.width, (i + 1) * self.dist_y))
            
        for i in range(self.height - 1):
            
            # vertical
            py.draw.line(self.win, (127, 127, 127), 
                         ((i + 1) * self.dist_x, 0), 
                         ((i + 1) * self.dist_x, self.height))
        
        # center
        py.draw.circle(self.win, 
        	           (127, 127, 127), 
        	           (self.dist_x*self.center[0], 
        	           	self.dist_y*self.center[1]), 5)

        # Draw objects
        for o in obj:
            
            o.draw(self)

        # Write Text
        for t in text:

        	t.write(self)
            
        py.display.update()

    # Given a complex number return the Pygame window position
    def real_position(self, z):

    	return (round((self.center[0] + z.real)*self.dist_x),
    		    round((self.center[1] - z.imag)*self.dist_y)) 
    
    # Quit plane    
    def quit(self):
        
        py.quit()

# Point class
class Point:
	# Create a point that represent a given number on the plane
	# Point initialization
	def __init__(self, z, color):

		self.z = z
		self.color = color
		self.ratio = 10

	# Draw Point
	def draw(self, plane):

		real_pos = plane.real_position(self.z)

		py.draw.circle(plane.win, self.color, real_pos, self.ratio)

# Graph class
class Graph:
	# Create a graphs object from its parametric form
	# Graph initialization
	def __init__(self, x_function, y_function, start, stop, step):

		self.x_function = x_function
		self.y_function = y_function
		self.start = start
		self.stop = stop
		self.step = step

	# Draw graphs
	def draw(self, plane):

		for t in np.arange(self.start, self.stop, self.step):

			real_pos = plane.real_position(complex(self.x_function(t),self.y_function(t)))

			py.draw.circle(plane.win, (0,0,0), real_pos, 2)

# Text class
class Text(object):

	def __init__(self, text, pos, color, typeface, size, bold = False, italic = False):

		self.pos = pos
		self.font = py.font.SysFont(typeface, size, bold, italic)
		self.text_to_write = self.font.render(text, True, color)

	def write(self, plane):

		plane.win.blit(self.text_to_write, plane.real_position(self.pos))

# Video Maker class
# Save animation frames on "images" folder
class Video_Maker():

	def __init__(self, video_name, name, max_images, fps, save_flag = True):

		self.video_name = video_name
		self.save_flag = save_flag # If true the frames are saved
		self.name = name
		self.max_images = max_images
		self.fps = fps

		# Create counter for images names
		self.counter = []

		while max_images > 1:

			max_images /= 10
			self.counter.append(0)

	# Create openCV videoWritter
	def begin(self, plane):

		fourcc = cv2.VideoWriter_fourcc(*'XVID')
		self.video_writter = cv2.VideoWriter(self.video_name,fourcc, self.fps, (plane.width,plane.height), True)

	def save_image(self, plane):

		if self.save_flag: # save images only if save_flag == True

			# Verify self.counter digit overflow
			for i in range(len(self.counter)):

				if self.counter[i] > 9:

					if i+1 < len(self.counter):

						self.counter[i+1] += 1
						self.counter[i] = 0

					else:

						self.save_flag = False

				else:

					break

			# convert to string the counter number
			number = ""

			for i in range(len(self.counter)-1, -1, -1):

				number += str(self.counter[i])

			# Save image and increment the counter
			if (int(number) <= self.max_images) and self.save_flag:

				# save image
				py.image.save(plane.win, 
					          os.path.join("C:\\Repositories\\Complexn\\images\\", 
					          	           self.name + number + ".jpeg"))

				# get image
				img = cv2.imread(os.path.join("C:\\Repositories\\Complexn\\images\\", 
											  self.name + number + ".jpeg"))

				# add to videdo
				self.video_writter.write(img)

				self.counter[0] += 1 # increment counter

			else:

				self.save_flag = False

	# save the final video
	
	def release(self):

		self.video_writter.release()