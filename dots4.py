#  @TheWorldFoundry

import pygame
import random
import math

class Shape:
    def __init__(self, pos, radius, facing, level):
        self.pos = pos
        self.radius = radius
        self.facing = facing
        self.level = level
        self.colour = [random.randint(120,255),random.randint(120,255),255]

def check_for_collision( circles, circle ):
    (x1, y1), r1, dir1, i1 = circle.pos, circle.radius, circle.facing, circle.level
    for c in circles:
        (x2, y2), r2, dir2, i2 = c.pos, c.radius, c.facing, c.level
        # If the distance between the two circles is less than the sum of their radius then they overlap
        dx = x2-x1
        dy = y2-y1
        # print ( int(dx**2 + dy**2) , int((r1+r2)**2) )
        if math.sqrt(dx**2 + dy**2) < math.sqrt((r1+r2)**2)-1:
            return True
    return False

def plot(circles, img):
    print ("Plotting...")

    for c in circles:
        (x, y), r, d, i = c.pos, c.radius, c.facing, c.level
        col = float(i)/255.0
        R,G,B = c.colour
        R = R*col
        G = G*col
        B = B*col
        if r > 1:
            pygame.draw.circle(img, [int(R),int(G),int(B),255], [int(x),int(y)], int(r+1)) # Introduce a slight overlap for traversability

    pygame.image.save(img, "plot_"+str(random.randint(1000000000,9999999999))+".png")


width = 8192
height = 8192

cx, cy = width >>1, height>>1

img = pygame.Surface([width, height], pygame.SRCALPHA)
img.fill( [0,0,0,255] )


circles = [ Shape((cx, cy), 30.0, 0.0, 255.0),
            Shape((cx, cy), 30.0, 45.0, 255.0),
            Shape((cx, cy), 30.0, 90.0, 255.0),
            Shape((cx, cy), 30.0, 135.0, 255.0),
            Shape((cx, cy), 30.0, 180.0, 255.0),
            Shape((cx, cy), 30.0, 225.0, 255.0),
            Shape((cx, cy), 30.0, 270.0, 255.0),
            Shape((cx, cy), 30.0, 315.0, 255.0)
            

  ]   #  Seed circle

circles = []
for i in xrange(0, random.randint(8,13)):
    degrees = random.randint(1,5)+1
    start_angle = random.randint(0,359)
    x,y = random.randint(width>>2, width-(width>>2)), random.randint(height>>2, height-(height>>2))
    size = 2 # float(random.randint(30,50))
    for j in xrange(0, degrees):
        circle = Shape((x,y), size, start_angle+j*(360/degrees), 255.0)
        circles.append(circle)



rules = [
    [ (10, 1.05, 0.95), (-10, 1.05, 0.95),(20, 1.05, 0.95), (-20, 1.05, 0.95),  ],
    [ (30, 1.05, 0.95), (-30, 1.05, 0.95) ],
  #  [ (60, 0.9, 0.99), (-60, 0.9, 0.99) ],
  #  [ (90, 0.9, 0.99), (-90, 0.9, 0.99) ],
    
    #  Seed rules
]

angle = math.pi/180.0

keep_going = 0
LOOP_LIMIT = 700
changes = True
while keep_going < LOOP_LIMIT and changes == True:
    print ("Step "+str(keep_going)+" circles = "+str(len(circles)))
    if keep_going%5 == 1:
        plot(circles, img)
    changes = False
    keep_going += 1
    new_circles = []
    for c in circles:
        new_circles.append(c)
    # random.shuffle(circles)
    for c in circles:
        (x, y), r, d, i = c.pos, c.radius, c.facing, c.level
        rule = rules[random.randint(0, len(rules)-1)]
        
        #for rule in rules:
        if True:
            rul = rule[random.randint(0, len(rule)-1)]
            # for rul in rule:
            if True:
                d_angle, d_radius, d_intensity = rul
                
                new_intensity = d_intensity * i
                if new_intensity < 16:
                    new_intensity = 16
                if new_intensity > 0:
                    new_radius = d_radius*r
                    if new_radius < 2:
                        new_radius = 2
                    if new_radius > 1:
                        #  span = r+new_radius
                        px = math.cos(angle*(d+d_angle)) * (r+new_radius) + x
                        py = math.sin(angle*(d+d_angle)) * (r+new_radius) + y
                        if new_radius <= px < width-new_radius and new_radius <= py < height-new_radius:  # Check bounds
                            new_circle = Shape((px, py), new_radius, d_angle+d, d_intensity * i )
                            #  Check for collisions
                            if check_for_collision( new_circles, new_circle ) == False:
                                new_circles.append(new_circle)
                                changes = True
    circles = new_circles
print ("Complete after "+str(keep_going)+" steps")

plot(circles, img)

print ("Done.")    
