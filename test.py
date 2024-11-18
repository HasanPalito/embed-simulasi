import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from threading import Thread
import time
import digits as digit
import keyboard

canvas = np.zeros((8, 32), dtype=int)

class Player:
  def __init__(self,pos_x):
    self.score = 0
    self.pos_y = 1
    self.power = 0
    self.pos_x = pos_x
    self.ready=0

player1=Player(9)
player2=Player(22)

class Ball:
    global player1
    global player2
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
    
    def hit(self,obj):
        print("x:",obj.pos_y,"x+4:",obj.pos_y+4, self._pos_x)
        print("y:",obj.pos_y, self._pos_y)
        return (obj.pos_y <= self._pos_y <= obj.pos_y + 4) and self.pos_x == obj.pos_x

    @pos_x.setter
    def pos_x(self, new_value):
        self._pos_x = new_value
        if self._pos_x == self.border_x_min or self._pos_x == self.border_x_max:
            player1.ready=0
            player2.ready=0
            if self._pos_x == self.border_x_min:
                player2.score=player2.score+1
            else:
                player1.score=player1.score+1
            self.pos_x=16
            self.pos_y=4
            

        elif self.hit(player1) or self.hit(player2):
            print("hit")
            self.dx = -self.dx
            #self.dy = np.random.choice([-1, 0, 1])



bola = Ball()

def on_button_press(event):
    global player1
    global player2
    if event.name == "d":  
        if player1.pos_y>=0 and player1.pos_y<4 : 
            player1.pos_y=player1.pos_y+1
    if event.name == "e":  
        if player1.pos_y>0 and player1.pos_y<=4 : 
            player1.pos_y=player1.pos_y-1
    if event.name == "down":
        if player2.pos_y>=0 and player2.pos_y<4 : 
            player2.pos_y=player2.pos_y+1
    elif event.name == "up":
        if player2.pos_y>0 and player2.pos_y<=4 : 
            player2.pos_y=player2.pos_y-1
    elif event.name == "enter":
        player1.ready= 1 
        player2.ready=1

keyboard.on_press(on_button_press)
def render_score():
    global player1
    global player2
    canvas[:,:]=0
    canvas[1:6, 1:6] = digit.digits[player1.score]
    canvas[1:6, 26:31] = digit.digits[player2.score]
    canvas[:,7:8]= 1
    canvas[:,24:25]= 1
    canvas[player1.pos_y:player1.pos_y+4,9:10]=1
    canvas[player2.pos_y:player2.pos_y+4,22:23]=1
    if player1.ready and player2.ready :
        bola.pos_x += bola.dx
        bola.pos_y += bola.dy

    # Set the ball's new position in the canvas
    canvas[bola.pos_y, bola.pos_x] = 1

# Function to simulate changes in the binary array
def update_array():
    global canvas
    while True:
        render_score()#binary_image = np.random.choice([0, 1], size=(8, 32))
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
