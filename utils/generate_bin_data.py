import json

def main():
    name = "pondicherry_india"
    file = open(f'data/maps/{name}/{name}.json')

    graph = json.load(file)  
    bin_data = {}

    for node in graph:
        if graph[node]['type'] == 'bin':
            bin_data[node] = {'lat': 0.0, 'lon': 0.0, 'state': 0}

    with open(f'data/maps/{name}/{name}_bin_data.json', 'w') as file:
        file.write(json.dumps(bin_data))
 
if __name__ == "__main__":
    main()