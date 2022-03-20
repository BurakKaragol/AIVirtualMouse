import cv2 as cv
import numpy as np

###
# Force Field Application
# Simulating the force fields in space
# key bindings
# W / S select up / down node
# A / D select left / right node
# Q / E set angle of the selected node
# + / - set the angle of all the nodes
# F enter editing mode
# X exit the application
###

# Editable
background_color = (255, 255, 255)
arrow_color = (0, 0, 255)
ball_color = (255, 0, 0)
node_color = (215, 215, 215)
node_selected_color = (235, 235, 235)
node_unactive_color = (155, 155, 155)
corner_dist = 40
node_number = 8
node_size = 100
node_arrow_size = (node_size // 2)
node_force = 0.01
node_dist = 2

# Non Editable
img_width = (node_number * node_size) + (corner_dist * 2) + ((node_number - 1) * node_dist)
img_height = img_width
img = np.zeros((img_height, img_width, 3), dtype=np.uint8)
img[0:img_height, 0:img_width] = background_color
node_selected_index_x = 0
node_selected_index_y = 0
node_selected_index = 0
force_field_active = True

# field class:
# this class is responsible for creating and editing force fields
class Field():
    mid_x = 0
    mid_y = 0

    def __init__(self, x, y, w, h, a, f, a_s):
        self.x = x
        self.y = y
        self.width = w
        self.height = h
        self.angle = a
        self.force = f
        self.arrow = a_s

        self.left = self.x
        self.top = self.y
        self.right = self.x + self.width
        self.bottom = self.y + self.height

        self.force_x = self.force * np.cos(np.deg2rad(self.angle))
        self.force_y = self.force * np.sin(np.deg2rad(self.angle))

        self.arrow_x = self.arrow * np.cos(np.deg2rad(self.angle))
        self.arrow_y = self.arrow * np.sin(np.deg2rad(self.angle))

    # change angle of the field
    def angle_up(self):
        self.angle += 5
        if self.angle > 355:
            self.angle = 0

    # change engle of the field
    def angle_down(self):
        self.angle -= 5
        if self.angle < 0:
            self.angle = 355

    # check if the ball inside the field
    def inside(self, x, y):
        if self.left < x and x < self.right:
            if self.top < y and y < self.bottom:
                return True
            return False
        return False

    # draw the field
    def draw(self, i, selected = False):
        if selected:
            i = cv.rectangle(i, (self.left, self.top), (self.right, self.bottom),
            node_unactive_color, cv.FILLED)
        else:
            if force_field_active:
                i = cv.rectangle(i, (self.left, self.top), (self.right, self.bottom),
                node_selected_color, cv.FILLED)
            else:
                i = cv.rectangle(i, (self.left, self.top), (self.right, self.bottom),
                node_color, cv.FILLED)

        self.mid_x = int(self.x + (self.width // 2))
        self.mid_y = int(self.y + (self.height // 2))
        self.force_x = self.force * np.cos(np.deg2rad(self.angle))
        self.force_y = self.force * -np.sin(np.deg2rad(self.angle))
        self.arrow_x = self.arrow * np.cos(np.deg2rad(self.angle))
        self.arrow_y = self.arrow * -np.sin(np.deg2rad(self.angle))
        i = cv.line(i, (self.mid_x, self.mid_y),
        (int(self.mid_x + self.arrow_x), int(self.mid_y + self.arrow_y)), arrow_color, 2, cv.LINE_4)

# Ball class for seeing the force field effect
class Ball():
    def __init__(self, x, y, r):
        self.x = x
        self.y = y
        self.radius = r

        self.acc_x = 0
        self.acc_y = 0

    # calculate the acceleration
    def calculateAcc(self, fields):
        if force_field_active:
            for field in fields:
                if field.inside(self.x, self.y):
                    self.acc_x += field.force_x
                    self.acc_y += field.force_y

    # collide with walls
    def collide(self):
        if ((self.x - self.radius) <= 0) or ((self.x + self.radius) >= img_width):
            self.acc_x *= -1
        if ((self.y - self.radius) <= 0) or ((self.y + self.radius) >= img_height):
            self.acc_y *= -1

    # move corresponding to acceleration
    def move(self):
        if force_field_active:
            self.x += self.acc_x
            self.y += self.acc_y
            self.collide()

    # draw the ball
    def draw(self, i):
        i = cv.circle(i, (int(self.x), int(self.y)), self.radius, ball_color, cv.FILLED)

# creating the field nodes
fields = []
for i in range(0, node_number):
    for j in range(0, node_number):
        temp = Field(corner_dist + i * (node_size + node_dist),
        corner_dist + j * (node_size + node_dist), node_size, node_size, 90, node_force, node_arrow_size)
        fields.append(temp)
ball = Ball(120, 120, 15)

# calculate the index of the fields array
def CalculateIndex(x, y):
    if x == 0:
        node_selected_index = y
    elif y == 0:
        node_selected_index = 8 * x
    else:
        node_selected_index = 8 * x + y
    
    return node_selected_index

while True:
    img[0:img_height, 0:img_width] = background_color
    node_selected_index = CalculateIndex(node_selected_index_x, node_selected_index_y)

    for i in range(0, len(fields)):
        if i == node_selected_index:
            fields[i].draw(img, True)
        else:
            fields[i].draw(img, False)

    ball.calculateAcc(fields)
    ball.move()
    ball.draw(img)

    cv.imshow("Ingredient Checker", img)

    c = cv.waitKey(1) % 256

    if c == ord('q'):
        fields[node_selected_index].angle_up()

    if c == ord('e'):
        fields[node_selected_index].angle_down()

    if c == ord('a'):
        node_selected_index_x -= 1
        if node_selected_index_x < 0:
            node_selected_index_x = node_number - 1

    if c == ord('d'):
        node_selected_index_x += 1
        if node_selected_index_x > node_number - 1:
            node_selected_index_x = 0

    if c == ord('w'):
        node_selected_index_y -= 1
        if node_selected_index_y < 0:
            node_selected_index_y = node_number - 1

    if c == ord('s'):
        node_selected_index_y += 1
        if node_selected_index_y > node_number - 1:
            node_selected_index_y = 0

    if c == ord('f'):
        if force_field_active:
            force_field_active = False
        else:
            force_field_active = True

    if c == ord('-'):
        for field in fields:
            field.angle_up()

    if c == ord('+'):
        for field in fields:
            field.angle_down()

    if c == ord('x'):
        break

cv.destroyAllWindows()