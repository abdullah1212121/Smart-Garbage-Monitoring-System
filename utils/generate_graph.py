import sys
import json
import math
import pygame
import numpy as np
from PIL import Image

class GraphGenerator:
    def __init__(self, name):
        pygame.init()

        self.name = name
        
        map = pygame.image.load(f'data/maps/{self.name}/{self.name}.png')
        self.screen = pygame.display.set_mode((map.get_width(), map.get_height()))
        self.screen.blit(map, (0, 0))

        self.graph = {
            0: {'x': 10, 'y': 20, 'neighbors': {1: 100, 2:300}},
            1: {'x': 40, 'y': 55, 'neighbors': {5: 900, 7:500}}
        }

    def update(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    print("saving graph")

                    with open(f'data/maps/{self.name}/{self.name}.json', 'w') as file:
                        file.write(json.dumps(self.graph))

        pygame.display.update()

def main():
    graph_generator = GraphGenerator("pondicherry_india")
    
    running = True

    while running:
        graph_generator.update()   
 
if __name__ == "__main__":
    main()