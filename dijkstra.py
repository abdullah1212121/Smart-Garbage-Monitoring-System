import numpy as np
import pygame
import utils
import heapq


def dijkstra(graph, start):
    node_data = {}
    for node in graph:
        node_data[node] = {'cost': float('inf'), 'pred': []}

    node_data[start]['cost'] = 0
    visited = set()
    pq = [(0, start)]

    while pq:
        current_cost, current_vertex = heapq.heappop(pq)

        if current_vertex not in visited: 
            visited.add(current_vertex)     

        for neighbor in graph[current_vertex]:
            if neighbor not in visited: 
                cost = current_cost + graph[current_vertex][neighbor]

                if cost < node_data[neighbor]['cost']:
                    node_data[neighbor]['cost'] = cost
                    node_data[neighbor]['pred'] = node_data[current_vertex]['pred'] + [current_vertex]
                
                heapq.heappush(pq, (cost, neighbor))

    return node_data


def main():
    pygame.init()
    screen = pygame.display.set_mode((1000, 600))
    map = pygame.image.load('map_big.png')
    screen.blit(map, (0, 0))

    adj_mat = np.load('adj_mat.npy')
    adj_list = utils.mat_to_list(adj_mat)

    node_data = dijkstra(adj_list, 0)


    locs = np.load('locations.npy')

    running = True

    for loc in locs:
        if (loc[2] == 1):
            pygame.draw.circle(screen, (255,0,0), (loc[0], loc[1]), 5)
        elif (loc[2] == 0):
            pygame.draw.circle(screen, (0,255,0), (loc[0], loc[1]), 5)

    for t in range(10):

        traj = node_data[t]['pred'] + [t]

        for i in range(len(traj)-1):
            pygame.draw.line(screen, (255, 0, 0), (locs[traj[i]][0], locs[traj[i]][1]), (locs[traj[i+1]][0], locs[traj[i+1]][1]))

    # for i in range(len(adj_mat)):
    #     for j in range(len(adj_mat[0])):
    #         if adj_mat[i][j] != 0:
    #             pygame.draw.line(screen, (255, 0, 0), (locs[i][0], locs[i][1]), (locs[j][0], locs[j][1]))



    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False

        pygame.display.update()  

    pygame.quit()

if __name__ == "__main__":
    main()