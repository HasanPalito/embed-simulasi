import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from threading import Thread
import time

canvas = np.zeros((8, 32), dtype=int)

class Ball:
    def __init__(self, pos_y=4, pos_x=16):
        self._pos_x = pos_x
        self._pos_y = pos_y
        self.border_y_min = 0
        self.border_y_max = 7
        self.border_x_min = 8
        self.border_x_max = 24
        self.dx = 1
        self.dy = 1

    @property
    def pos_y(self):
        return self._pos_y

    @pos_y.setter
    def pos_y(self, new_value):
        self._pos_y = new_value
        if self._pos_y == self.border_y_min or self._pos_y == self.border_y_max:
            self.dy = -self.dy

    @property
    def pos_x(self):
        return self._pos_x

    @pos_x.setter
    def pos_x(self, new_value):
        self._pos_x = new_value
        if self._pos_x == self.border_x_min or self._pos_x == self.border_x_max:
            self.dx = -self.dx

# Create an instance of the ball
bola = Ball()

def update_array():
    global canvas
    while True:
        # Clear the canvas
        canvas.fill(0)

        # Update the position of the ball
        bola.pos_x += bola.dx
        bola.pos_y += bola.dy

        # Set the ball's new position in the canvas
        canvas[bola.pos_y, bola.pos_x] = 1

        time.sleep(0.1)  # Update every 100ms

# Function to render the array
def render_array():
    global canvas
    fig, ax = plt.subplots()
    img = ax.imshow(canvas, cmap='gray', interpolation='nearest')
    plt.axis('off')  # Turn off axis labels

    def refresh(frame):
        img.set_data(canvas)
        return [img]

    ani = FuncAnimation(fig, refresh, interval=100)  # Update every 100ms
    plt.show()

# Start the update thread
update_thread = Thread(target=update_array, daemon=True)
update_thread.start()

# Start rendering
render_array()
