import json

def main():
    name = "pondicherry_india"
    file = open(f'data/maps/{name}/{name}.json')
    graph = json.load(file)  

    for node in graph.copy():
        for neighbor in graph[node]['neighbors'].copy():
            if neighbor == node:
                graph[node]['neighbors'].pop(neighbor)
                print("found duplicate for ", node)

    with open(f'data/maps/{name}/{name}.json', 'w') as file:
        file.write(json.dumps(graph))
 
if __name__ == "__main__":
    main()