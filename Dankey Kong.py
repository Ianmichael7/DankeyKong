import sys, math, random
from pyglet.gl import *
from pyglet.window import *
from math import *

window = pyglet.window.Window(600,500)

b1,b2,b3,b4 = True,False,False,False

heroTrans = [0,0]

monkey = pyglet.graphics.vertex_list(4, ('v2f', [100,400, 100,443, 150,443, 150,400]))
levels = pyglet.graphics.vertex_list(8, ('v2f', [100,400, 500,360, 550,325, 150,275, 100,240, 500,200, 550,165, 150,115]))
ground = pyglet.graphics.vertex_list(2, ('v2f', [0,85, 600,85]))
latters = pyglet.graphics.vertex_list(8, ('v2f', [160,85, 160,128, 165,85, 165,128, 160,99, 165,99, 160,113, 165,113]))
hero = pyglet.graphics.vertex_list(4, ('v2f', [300,85, 300,100, 305,100, 305,85]))

points = [0,0] #Circle code provided by Dave Pape
colors = [0.7,0.4,0.3]
for i in range(0,41):
    angle = (i/40.0) * math.pi * 2
    x,y = math.sin(angle), math.cos(angle)
    r,g,b = random.uniform(0.6,1), random.uniform(0.3,0.6), random.uniform(0.2,0.4)
    points += [x,y]
    colors += [r,g,b]
wheel = pyglet.graphics.vertex_list(42, ('v2f', points), ('c3f', colors))
wheelScale = 10.0
wheelRot = [0.0, 0.0, 0.0, 0.0]
wheelTrans = [165,404, 165,404, 165,404, 165,404]

def makeBarrel(bValue, bx, by, bRot):
    if bValue:
        glPushMatrix() #Barrel 1
        glLoadIdentity()
        glTranslatef(wheelTrans[bx], wheelTrans[by], 0)
        glRotatef(wheelRot[bRot], 0, 0, 1)
        glScalef(wheelScale, wheelScale, wheelScale)
        wheel.draw(GL_TRIANGLE_FAN)
        glPopMatrix()

def gogo(bValue, bx, by, bRot,b):
    global b1,b2,b3,b4
    if bValue:
        #Falls Down at end of Levels
        if wheelTrans[by] < 369.3 and wheelTrans[by] > 331 or wheelTrans[by] < 125.01 and wheelTrans[by] > 95 or wheelTrans[by] < 210.1 and wheelTrans[by] > 172 or wheelTrans[by] < 286.1 and wheelTrans[by] > 247.7:
            wheelTrans[by] -= 1
        #To the Right
        if wheelTrans[by] < 405 and wheelTrans[by] > 369.2 or wheelTrans[by] < 247.71 and wheelTrans[by] > 210:
            wheelTrans[bx] += 1
            wheelTrans[by] -= 0.1
            wheelRot[bRot] -= 2
        #To the Left
        if wheelTrans[by] < 331.1 and wheelTrans[by] > 286 or wheelTrans[by] < 171.71 and wheelTrans[by] > 125:
            wheelTrans[bx] -= 1
            wheelTrans[by] -= 0.12
            wheelRot[bRot] += 2

        #Barrel is destroyed at bottom
        if wheelTrans[by] < 96:
            if b == 1:
                b1 = False
            if b == 2:
                b2 = False
            if b == 3:
                b3 = False
            if b == 4:
                b4 = False
            wheelTrans[bx],wheelTrans[by] = 165,404

        #Activate next barrel to roll down    
        if wheelTrans[by] > 330 and wheelTrans[by] < 332:
            if b == 1:
                b2 = True
            if b == 2:
                b3 = True
            if b == 3:
                b4 = True
        if wheelTrans[by] > 300 and wheelTrans[by] < 302:
            if b == 4:
                b1 = True


@window.event
def on_draw(): #DRAW FUNCTION
    glClear(GL_COLOR_BUFFER_BIT)

    glPushMatrix()
    glTranslatef(heroTrans[0], heroTrans[1], 0)
    glColor3f(1,0,0) #Box that represents Mario
    hero.draw(GL_QUADS)
    glPopMatrix()
    
    glColor3f(1,1,0) #Box that represents Donkey Kong
    monkey.draw(GL_QUADS)
    
    glColor3f(0,1,1)
    levels.draw(GL_LINES) #Blue Levels
    glColor3f(0,1,0)
    ground.draw(GL_LINES) #Green Bottom Level (Ground)

    glColor3f(1,1,0)
    latters.draw(GL_LINES) #Latters starting from the bottom, up

    glTranslatef(330,75,0)
    latters.draw(GL_LINES)
    glTranslatef(-330,-75,0)
    
    glTranslatef(0,150,0)
    latters.draw(GL_LINES)
    glTranslatef(0,-150,0)
    
    glTranslatef(330,232,0)
    latters.draw(GL_LINES)
    glTranslatef(-330,-232,0)

    makeBarrel(b1,0,1,0)
    makeBarrel(b2,2,3,1)
    makeBarrel(b3,4,5,2)
    makeBarrel(b4,6,7,3)

@window.event
def on_key_press(key,modifiers):
    global heroCoordinates
    if key == pyglet.window.key.LEFT:
        heroTrans[0] -= 10
    elif key == pyglet.window.key.RIGHT:
        heroTrans[0] += 10

def update(dt): #UPDATE FUNCTION
    gogo(b1,0,1,0, 1)
    gogo(b2,2,3,1, 2)
    gogo(b3,4,5,2, 3)
    gogo(b4,6,7,3, 4)

pyglet.clock.schedule_interval(update,1/80.0)
pyglet.app.run()
