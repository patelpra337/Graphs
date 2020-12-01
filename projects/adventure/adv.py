from room import Room
from player import Player
from world import World

import random
from ast import literal_eval
from util import Queue


def add_room(room):
	if room not in room_map:
		room_map[room] = {'n': '?', 's': '?', 'e': '?', 'w': '?'}
		exits = room.get_exits()
		for direction in room_map[room]:
			if direction not in exits:
				room_map[room][direction] = 'NONE'
		return True
	else:
		return False


def add_relation(starting_room, direction, ending_room):
	room_map[starting_room][direction] = ending_room
	room_map[ending_room][inverse[direction]] = starting_room


def get_path(starting_room):
	visited = set()
	q = Queue()
	q.enqueue((starting_room, []))

	while q.size() > 0:
		room, path = q.dequeue()
		if room in visited:
			continue
		else:
			visited.add(room)
		for exit in room_map[room]:
			if room_map[room][exit] == '?':
				return path
			elif room_map[room][exit] != 'NONE':
				new_path = path.copy()
				new_path.append(exit)
				new_room = room_map[room][exit]
				q.enqueue((new_room, new_path))
	return []

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []
change_direction = {'n': 'e', 'e': 's', 's': 'w', 'w': 'n'}
inverse = {'n': 's', 's': 'n', 'e': 'w', 'w': 'e'}
room_map = {}
add_room(player.current_room)

while len(room_map) < len(room_graph):
	room = player.current_room
	exits = room.get_exits()
	explored = False
	direction = 's'

	for _ in range(len(change_direction)):
		if room_map[room][direction] == '?' and direction in exits:
			explored = True
			player.travel(direction)
			next_room = player.current_room
			traversal_path.append(direction)
			if not add_room(next_room):
				player.travel(inverse[direction])
				traversal_path.pop()
			add_relation(room, direction, next_room)
			break
		else:
			direction = change_direction[direction]
	if not explored:
		path = get_path(room)
		traversal_path.extend(path)
		for direction in path:
			player.travel(direction)


# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
player.current_room.print_room_description(player)
while True:
    cmds = input("-> ").lower().split(" ")
    if cmds[0] in ["n", "s", "e", "w"]:
        player.travel(cmds[0], True)
    elif cmds[0] == "q":
        break
    else:
        print("I did not understand that command.")
