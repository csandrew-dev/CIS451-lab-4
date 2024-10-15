import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
import pyrr

# Define cube vertices and indices
vertices = np.array([
    -0.5, -0.5, 0.5, 1.0, 1.0, 0.0, 0.0, 1.0,  # point 0
    0.5, -0.5, 0.5, 1.0, 1.0, 1.0, 0.0, 1.0,  # point 1
    0.5, 0.5, 0.5, 1.0, 1.0, 1.0, 1.0, 1.0,  # point 2
    -0.5, 0.5, 0.5, 1.0, 1.0, 0.0, 1.0, 1.0,  # point 3
    -0.5, -0.5, -0.5, 1.0, 0.0, 0.0, 0.0, 1.0,  # point 4
    0.5, -0.5, -0.5, 1.0, 0.0, 1.0, 0.0, 1.0,  # point 5
    0.5, 0.5, -0.5, 1.0, 0.0, 1.0, 1.0, 1.0,  # point 6
    -0.5, 0.5, -0.5, 1.0, 0.0, 0.0, 1.0, 1.0   # point 7
], dtype=np.float32)

indices = np.array([
    0, 1, 2, 0, 2, 3,  # front face
    5, 4, 7, 5, 7, 6,  # back face
    3, 2, 7, 7, 2, 6,  # top
    2, 1, 5, 2, 5, 6,  # right
    1, 0, 5, 5, 0, 4,  # bottom
    3, 7, 4, 3, 4, 0   # left
], dtype=np.uint32)

def draw_cube(transformation_matrix):
    glBegin(GL_TRIANGLES)
    for index in indices:
        # Get the original vertex data
        original_vertex = vertices[index * 8:index * 8 + 8]
        
        # Transform the position using the transformation matrix
        transformed_vertex = transformation_matrix @ np.array(original_vertex[:4], dtype=np.float32)
        
        # Extract the color from the original vertex data
        color = original_vertex[4:8]  # RGBA
        
        # Set the vertex color
        glColor4f(color[0], color[1], color[2], color[3])
        glVertex3f(transformed_vertex[0], transformed_vertex[1], transformed_vertex[2])
    glEnd()

def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -5)

    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        time = pygame.time.get_ticks() / 1000.0

        # Define transformations
        translation_matrix = pyrr.matrix44.create_from_translation([0.5, 0, 0], dtype=np.float32)
        scaling_matrix = pyrr.matrix44.create_from_scale([0.5, 0.5, 0.5], dtype=np.float32)
        rot_x = pyrr.matrix44.create_from_x_rotation(0.5 * time, dtype=np.float32)
        rot_y = pyrr.matrix44.create_from_y_rotation(0.8 * time, dtype=np.float32)

        # Overall transformations
        overall_transformation_a = rot_x @ rot_y
        overall_transformation_b = scaling_matrix @ rot_x @ rot_y
        overall_transformation_c = translation_matrix @ scaling_matrix @ rot_x @ rot_y

        # Clear the screen and depth buffer
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        # Draw the cube with the desired transformation
        draw_cube(overall_transformation_a)
        draw_cube(overall_transformation_b)
        draw_cube(overall_transformation_c)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()