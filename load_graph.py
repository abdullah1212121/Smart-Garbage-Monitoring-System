import numpy as np
import pygame
import sys


def main():
    pygame.init()
    screen = pygame.display.set_mode((1000, 600))
    map = pygame.image.load('map_big.png')
    screen.blit(map, (0, 0))

    adj = np.load('adj_mat.npy')
    locs = np.load('locations.npy')

    running = True

    for loc in locs:
        if (loc[2] == 1):
            pygame.draw.circle(screen, (255,0,0), (loc[0], loc[1]), 5)
        elif (loc[2] == 0):
            pygame.draw.circle(screen, (0,255,0), (loc[0], loc[1]), 5)

    for i in range(len(adj)):
        for j in range(len(adj[0])):
            if adj[i][j] != 0:
                pygame.draw.line(screen, (255, 0, 0), (locs[i][0], locs[i][1]), (locs[j][0], locs[j][1]))



    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False

        pygame.display.update()  

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()