from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random


WINDOW_WIDTH, WINDOW_HEIGHT = 1000, 700

bird_x = -2.0
bird_y = 0.0

bird_vel = 0.0
gravity = -0.0005
jump_strength = 0.025


score = 0
pipes = [[10.0, random.uniform(-2, 1)]]
game_active = True


def draw_text(x, y, text):
    glColor3f(1.0, 1.0, 0.0)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, WINDOW_WIDTH, 0, WINDOW_HEIGHT)

    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()

    glRasterPos2f(x, y)
    for c in text:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(c))

    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)



def draw_pipe_with_cap(x, y_height, is_top=False):
    quad = gluNewQuadric()
    glColor3f(0.0, 0.7, 0.0)

    glPushMatrix()

    y_pos = 6 if is_top else -6
    glTranslatef(x, y_pos, 0)
    glRotatef(90 if is_top else -90, 1, 0, 0)

    pipe_length = 5 - y_height if is_top else 5 + y_height
    gluCylinder(quad, 0.7, 0.7, pipe_length, 32, 32)

    glTranslatef(0, 0, pipe_length)
    gluCylinder(quad, 0.85, 0.85, 0.6, 32, 32)
    gluDisk(quad, 0, 0.85, 32, 1)

    glPopMatrix()


def draw_styled_bird():
    glPushMatrix()
    glTranslatef(bird_x, bird_y, 0)

    
    glRotatef(bird_vel * 300, 0, 0, 1)

   
    glColor3f(0.1, 0.1, 0.1)
    glutSolidSphere(0.6, 50, 50)

    
    glPushMatrix()
    glTranslatef(-0.4, 0, 0)
    glScalef(0.8, 0.6, 0.6)
    glutSolidSphere(0.5, 40, 40)
    glPopMatrix()

    
    glPushMatrix()
    glTranslatef(0.55, 0.25, 0)
    glColor3f(0.15, 0.15, 0.15)
    glutSolidSphere(0.35, 40, 40)

   
    glColor3f(1, 1, 1)
    glTranslatef(0.15, 0.1, 0.2)
    glutSolidSphere(0.12, 20, 20)

    glColor3f(0, 0, 0)
    glTranslatef(0.05, 0.02, 0.05)
    glutSolidSphere(0.05, 10, 10)

    glPopMatrix()

    
    glColor3f(1.0, 0.6, 0.0)
    glPushMatrix()
    glTranslatef(0.75, -0.05, 0)
    glRotatef(90, 0, 1, 0)
    glutSolidCone(0.18, 0.5, 30, 30)
    glPopMatrix()

  
    glColor3f(0.05, 0.05, 0.05)
    glPushMatrix()
    glTranslatef(-0.1, 0.1, 0.5)
    glRotatef(25, 0, 0, 1)
    glScalef(0.4, 0.1, 0.8)
    glutSolidCube(1)
    glPopMatrix()

   
    glPushMatrix()
    glTranslatef(-0.1, 0.1, -0.5)
    glRotatef(-25, 0, 0, 1)
    glScalef(0.4, 0.1, 0.8)
    glutSolidCube(1)
    glPopMatrix()

   
    glColor3f(0.08, 0.08, 0.08)
    glPushMatrix()
    glTranslatef(-0.7, -0.1, 0)
    glScalef(0.2, 0.2, 0.4)
    glutSolidCube(1)
    glPopMatrix()

    glPopMatrix()


def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    draw_text(50, 650, f"SCORE : {score}")

    gluLookAt(10, 4, 16,
              0, 0, 0,
              0, 1, 0)

    draw_styled_bird()

    for p in pipes:
        draw_pipe_with_cap(p[0], p[1], is_top=False)
        draw_pipe_with_cap(p[0], p[1] + 3.8, is_top=True)

    
    glColor3f(0.2, 0.5, 0.2)
    glPushMatrix()
    glTranslatef(0, -6.5, 0)
    glScalef(60, 0.2, 60)
    glutSolidCube(1.0)
    glPopMatrix()

    glutSwapBuffers()


def update(v):
    global bird_y, bird_vel, pipes, score, game_active

    if game_active:

        bird_vel += gravity
        bird_y += bird_vel

        for p in pipes:
            p[0] -= 0.10

            if abs(p[0] + 2) < 0.1:
                score += 1

            if abs(p[0] + 2) < 0.9:
                if bird_y < p[1] + 0.6 or bird_y > p[1] + 3.2:
                    reset_game()

        if pipes[-1][0] < 5:
            pipes.append([15.0, random.uniform(-2, 1)])

        if pipes[0][0] < -15:
            pipes.pop(0)

        if bird_y < -5.8 or bird_y > 8.0:
            reset_game()

    glutPostRedisplay()
    glutTimerFunc(16, update, 0)


def reset_game():
    global bird_y, bird_vel, score, pipes
    bird_y = 0
    bird_vel = 0
    score = 0
    pipes = [[10.0, random.uniform(-2, 1)]]


def keyboard(key, x, y):
    global bird_vel

    if key == b' ' or key == b'w':
        bird_vel = jump_strength
    elif key == b's':
        bird_vel = -jump_strength


def special_input(key, x, y):
    global bird_vel

    if key == GLUT_KEY_UP:
        bird_vel = jump_strength
    elif key == GLUT_KEY_DOWN:
        bird_vel = -jump_strength


glutInit()
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
glutInitWindowSize(WINDOW_WIDTH, WINDOW_HEIGHT)
glutCreateWindow(b"FULL 3D Flappy Bird")

glEnable(GL_DEPTH_TEST)

glMatrixMode(GL_PROJECTION)
gluPerspective(45, WINDOW_WIDTH/WINDOW_HEIGHT, 0.1, 100)

glMatrixMode(GL_MODELVIEW)
glClearColor(0.4, 0.8, 1.0, 1.0)

glutDisplayFunc(display)
glutKeyboardFunc(keyboard)
glutSpecialFunc(special_input)
glutTimerFunc(0, update, 0)

glutMainLoop()
