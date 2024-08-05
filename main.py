import pygame
import numpy as np
import math

pygame.init()

width, height = 800, 600
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
pygame.display.set_caption("3D-ish Render")


def connect_points(i, j, points, color):
    pygame.draw.line(screen, color, (points[i][0], points[i][1]), (points[j][0], points[j][1]))


projection_matrix = np.matrix([
    [1, 0, 0],
    [0, 1, 0],
    [0, 0, 1]
])
scale = 100
angle = 0
origin = (width / 2, height / 2)

# points
points = [np.matrix([-1, -1, 1]),
          np.matrix([1, -1, 1]),
          np.matrix([1, 1, 1]),
          np.matrix([-1, 1, 1]),
          np.matrix([1, -1, -1]),
          np.matrix([1, 1, -1]),
          np.matrix([-1, 1, -1]),
          np.matrix([-1, -1, -1])]

projected_points = [
    [n, n] for n in range(len(points))
]

while True:
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    # rotation matrices
    rotation_x_matrix = np.matrix([
        [1, 0, 0],
        [0, math.cos(angle), -math.sin(angle)],
        [0, math.sin(angle), math.cos(angle)]
    ])
    rotation_y_matrix = np.matrix([
        [math.cos(angle), 0, math.sin(angle)],
        [0, 1, 0],
        [-math.sin(angle), 0, math.cos(angle)]
    ])
    rotation_z_matrix = np.matrix([
        [math.cos(angle), -math.sin(angle), 0],
        [math.sin(angle), math.cos(angle), 0],
        [0, 0, 1]
    ])
    angle += 0.01

    screen.fill((0, 0, 0))

    i = 0
    for point in points:
        # rotation
        rotated_x_point = np.dot(rotation_x_matrix, point.reshape((3, 1)))  # multiply the rotation matrix by the original point
        rotated_y_point = np.dot(rotation_y_matrix, rotated_x_point)  # multiply the rotation matrix by the original point
        rotated_point = np.dot(rotation_z_matrix, rotated_y_point)  # multiply the rotation matrix by the original point

        # final projection
        projected_point = np.dot(projection_matrix, rotated_point)  # multiply the rotation matrix by the original point

        projected_x = int(projected_point[0][0] * scale) + origin[0]
        projected_y = int(projected_point[1][0] * scale) + origin[1]

        projected_points[i] = [projected_x, projected_y]  # storing the projected points in a list
        pygame.draw.circle(screen, (255, 0, 0), (projected_x, projected_y), 5)
        i += 1

        # connect the points
        connect_points(0, 1, projected_points, (255, 255, 255))
        connect_points(1, 2, projected_points, (255, 255, 255))
        connect_points(2, 3, projected_points, (255, 255, 255))
        connect_points(3, 0, projected_points, (255, 255, 255))

        connect_points(4, 5, projected_points, (255, 255, 255))
        connect_points(5, 6, projected_points, (255, 255, 255))
        connect_points(6, 7, projected_points, (255, 255, 255))
        connect_points(7, 4, projected_points, (255, 255, 255))

        connect_points(0, 7, projected_points, (255, 255, 255))
        connect_points(1, 4, projected_points, (255, 255, 255))
        connect_points(2, 5, projected_points, (255, 255, 255))
        connect_points(3, 6, projected_points, (255, 255, 255))

    pygame.display.update()
    clock.tick(60)
