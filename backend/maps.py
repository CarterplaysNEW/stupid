# Game maps and navigation data for SNOWE RUN

MAP_LIST = [
    {"id": "snow_arena", "name": "Snowy Arena", "max_players": 10},
    {"id": "ice_maze", "name": "Frozen Labyrinth", "max_players": 8}
]

MAPS = {
    "snow_arena": {
        "width": 100,
        "height": 100,
        "spawn_points": [{"x": 10, "z": 10}, {"x": 90, "z": 90}, {"x": 50, "z": 50}]
    },
    "ice_maze": {
        "width": 80,
        "height": 80,
        "spawn_points": [{"x": 5, "z": 5}, {"x": 75, "z": 75}]
    }
}

NAVS = {
    "snow_arena": {"nodes": [], "edges": []},
    "ice_maze": {"nodes": [], "edges": []}
}
