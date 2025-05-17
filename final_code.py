import csv
import re
import random
import networkx as nx
from collections import defaultdict


def import_station_data(csv_file):
    with open(csv_file, 'r', encoding='utf-8') as f:
        return list(csv.DictReader(f))


def station_codes_and_map(stations):
    all_codes = set()
    station_map = defaultdict(list)

    for station in stations:
        codes = station['STN_NO'].split('/')
        all_codes.update(codes)
        station_map[station['STN_NAME']].extend(codes)

    return all_codes, station_map


def station_lines(station_codes):
    grouped_stations = defaultdict(list)
    for station_code in station_codes:
        match = re.match(r'([A-Z]+)\d*', station_code)
        if match:
            line = match.group(1)
            grouped_stations[line].append(station_code)
        else:
            print(f"Invalid station code: {station_code}")

    return grouped_stations


def sort_stations(line_stations):
    def find_matches(code):
        match = re.search(r'\d+', code)
        return int(match.group()) if match else 0

    for line in line_stations:
        line_stations[line].sort(key=find_matches)

    return line_stations


def create_edges(graph, line_stations, looped_lines):
    for line, station_codes in line_stations.items():
        for i in range(len(station_codes) - 1):
            graph.add_edge(station_codes[i], station_codes[i + 1], weight=random.randint(2, 8))

        # If the line is a loop line, connect the last to the first
        if line in looped_lines and len(station_codes) > 1:
            graph.add_edge(station_codes[-1], station_codes[0], weight=random.randint(2, 8))


def add_interchanges(graph, station_map):
    for station_codes in station_map.values():
        if len(station_codes) > 1:
            for i in range(len(station_codes)):
                for j in range(i + 1, len(station_codes)):
                    graph.add_edge(station_codes[i], station_codes[j], weight=5)


def metro_graph(csv_file):
    looped_lines = {"CC"}
    graph = nx.Graph()

    stations = import_station_data(csv_file)
    all_codes, station_map = station_codes_and_map(stations)
    graph.add_nodes_from(all_codes)

    line_groups = station_lines(all_codes)
    sorted_lines = sort_stations(line_groups)

    create_edges(graph, sorted_lines, looped_lines)
    add_interchanges(graph, station_map)
    return graph


def find_shortest_route(graph, start, end):
    try:
        return nx.shortest_path(graph, source=start, target=end)
    except nx.NetworkXNoPath:
        return None


def find_fastest_route(graph, start, end):
    try:
        path = nx.shortest_path(graph, source=start, target=end, weight='weight')
        sum_time = sum(graph[path[i]][path[i + 1]]['weight'] for i in range(len(path) - 1))
        return path, sum_time
    except nx.NetworkXNoPath:
        return None, None


if __name__ == '__main__':
    csv_file = 'MRT Stations.csv'
    graph = metro_graph(csv_file)
    s=0
    d=0
    start = str(input("Pick a start station: "))
    while s==0 :
        if start not in graph:
            print(f"Invalid start station: {start}")
            start = str(input("Pick a start station: "))
        else:
            s=1
    end = str(input("Pick your destination station: "))
    while d==0 :
        if end not in graph:
            print(f"Invalid destination station: {end}")
            end = str(input("Pick your destination station: "))
        else:
            d=1

    shortest_route = find_shortest_route(graph, start, end)
    if shortest_route:
        print(f"Shortest route: {' -> '.join(shortest_route)} ({len(shortest_route) - 1} stops)")
    else:
        print("No shortest route found")

    fastest_route, total_time = find_fastest_route(graph, start, end)
    if fastest_route:
        print(f"Fastest route: {' -> '.join(fastest_route)} (Total time: {total_time} mins)")
    else:
        print("No fastest route found")
