import sys
import json
import pygame
from src.dijkstra import dijkstra
from src.firebase_reader import FirebaseReader
import argparse

class ShortestPath:
    def __init__(self, name):
        pygame.init()
        self.firebase_reader = FirebaseReader()

        self.name = name
        
        self.map = pygame.image.load(f'data/maps/{self.name}/{self.name}.png')
        self.screen = pygame.display.set_mode((self.map.get_width(), self.map.get_height()))
        self.screen.blit(self.map, (0, 0))

        self.graph = self.load_graph(f'data/maps/{self.name}/{self.name}.json')
        self.bins = self.get_bins()
        self.garage = self.get_garage()

        self.active_bins = self.firebase_reader.get_active_bins()
        # self.active_bins = random.sample(self.bins, 5)
        # self.active_bins = self.bins[:5]
        
        if len(self.active_bins) > 0:
            trajectory = self.compute_path(self.active_bins.copy())
            self.draw_bins(trajectory)

    def load_graph(self, path):
        file = open(path)
        return json.load(file)

    def get_bins(self):
        bins = []
        for node in self.graph:
            if self.graph[node]['type'] == 'bin':
                bins.append(node)

        return bins

    def get_garage(self):
        for node in self.graph:
            if self.graph[node]['type'] == 'garage':
                return node

        return None
        
    def compute_path(self, bins):
        num_of_bins = len(bins)
        min_idx = None
        min_cost = float('inf')
        min_path = []
        start = self.garage

        full_path = []

        for j in range(num_of_bins):
            for i in range(len(bins)):
                cost, path = dijkstra(self.graph, start, bins[i])
                if cost < min_cost:
                    min_idx = i
                    min_cost = cost
                    min_path = path
                    min_path.append(bins[i])

            full_path += min_path

            start = bins.pop(min_idx)
            min_idx = None
            min_cost = float('inf')
            min_path = []

        cost, path = dijkstra(self.graph, start, self.garage)
        path.append(self.garage)

        full_path += path
        
        return full_path


    def update_graph_complete(self):
        self.screen.blit(self.map, (0, 0))
        for node in self.graph:
            if self.graph[node]['type'] == 'bin':
                pygame.draw.circle(self.screen, (255,0,0), (self.graph[node]['pos']['x'], self.graph[node]['pos']['y']), 5)
            elif self.graph[node]['type'] == 'node':
                pygame.draw.circle(self.screen, (0,255,0), (self.graph[node]['pos']['x'], self.graph[node]['pos']['y']), 5)
            elif self.graph[node]['type'] == 'garage':
                pygame.draw.circle(self.screen, (0,0,255), (self.graph[node]['pos']['x'], self.graph[node]['pos']['y']), 5)

            for neighbor in self.graph[node]['neighbors']:
                pygame.draw.line(self.screen, (255, 0, 0), (self.graph[node]['pos']['x'], self.graph[node]['pos']['y']), (self.graph[neighbor]['pos']['x'], self.graph[neighbor]['pos']['y']))

    def draw_bins(self, trajectory):
        # self.screen.blit(self.map, (0, 0))
        for node in self.graph:
            if self.graph[node]['type'] == 'bin':
                if node in self.active_bins:
                    pygame.draw.circle(self.screen, (255,0,0), (self.graph[node]['pos']['x'], self.graph[node]['pos']['y']), 5)
                else:
                    pygame.draw.circle(self.screen, (0,255,0), (self.graph[node]['pos']['x'], self.graph[node]['pos']['y']), 5)
            
            if self.graph[node]['type'] == 'garage':
                pygame.draw.circle(self.screen, (0,0,255), (self.graph[node]['pos']['x'], self.graph[node]['pos']['y']), 5)

        if trajectory:
            for i in range(len(trajectory)-1):
                pygame.draw.line(self.screen, (255, 0, 0), (self.graph[trajectory[i]]['pos']['x'], self.graph[trajectory[i]]['pos']['y']), (self.graph[trajectory[i+1]]['pos']['x'], self.graph[trajectory[i+1]]['pos']['y']))


    def update(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # self.update_graph(None)
        pygame.display.update()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--town_name', type=str, default="pondicherry_india")
    
    shortest_path = ShortestPath(parser.parse_args().town_name)
    
    running = True

    while running:
        shortest_path.update()   
 
if __name__ == "__main__":
    main()