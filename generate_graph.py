import pygame
import sys
import math
import numpy as np


class GraphGenerator:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1000, 600))
        map = pygame.image.load('map_big.png')
        self.screen.blit(map, (0, 0))

        self.nodes = []  
        self.draw_line_between = [0, 0]
        self.current_idx = 0
        self.adj_mat = 0

    def update(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    print("saving adj_mat")
                    print("saving node locations")

                    locations = np.array(self.nodes)
                    np.save("adj_mat", self.adj_mat)
                    np.save("locations", locations)
            
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()

                if self.node_exists(pos) == None:
                    if (event.button == 1):
                        print("adding node")
                        self.current_idx = 0
                        self.draw_line_between = [0, 0]
                        self.add_node(pos, False)
                    if (event.button == 3):
                        print("adding bin")
                        self.current_idx = 0
                        self.draw_line_between = [0, 0]
                        self.add_node(pos, True)

                else:
                    print("node exitsts")
                    self.draw_line_between[self.current_idx] = self.node_exists(pos)
                    self.current_idx += 1
                    if (self.current_idx == 2):
                        self.draw_line(self.draw_line_between[0], self.draw_line_between[1])
                        self.current_idx = 0
                        self.draw_line_between = [0, 0]

        pygame.display.update()

    def add_node(self, pos, bin=False):
        if bin:
            pygame.draw.circle(self.screen, (255,0,0), pos, 5)
            pos = list(pos)
            pos.append(1)
        else:
            pygame.draw.circle(self.screen, (0,255,0), pos, 5)
            pos = list(pos)
            pos.append(0)

        self.nodes.append(pos)
        temp_adj_mat = np.zeros((len(self.nodes), len(self.nodes)))
        temp_adj_mat[:len(self.nodes)-1, :len(self.nodes)-1] = self.adj_mat
        self.adj_mat = temp_adj_mat

    def node_exists(self, pos):
        for i, node in enumerate(self.nodes):
            if self.distance(pos, node) <= 5:
                return i

        return None

    def distance(self, node1, node2):
        return math.sqrt((node2[0] - node1[0])**2 + (node2[1] - node1[1])**2)

    def draw_line(self, node1_idx, node2_idx):
        dist = self.distance((self.nodes[node1_idx][0], self.nodes[node1_idx][1]), (self.nodes[node2_idx][0], self.nodes[node2_idx][1]))
        self.adj_mat[node1_idx][node2_idx] = dist
        self.adj_mat[node2_idx][node1_idx] = dist
        pygame.draw.line(self.screen, (255, 0, 0), (self.nodes[node1_idx][0], self.nodes[node1_idx][1]), (self.nodes[node2_idx][0], self.nodes[node2_idx][1]))
        print(self.adj_mat)

def main():
    graph_generator = GraphGenerator()
    running = True

    while running:
        graph_generator.update()    

if __name__ == "__main__":
    main()
