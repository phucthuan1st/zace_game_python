import grpc
import logging
import random
import time
from concurrent import futures

import hashlib

from helpers.generate_map import generate_map

import zace_tank_battle_pb2
import zace_tank_battle_pb2_grpc

from constants import *

NUMBER_OF_CELL = SCREEN_HEIGHT // CELL_SIZE

class MatchState:
    def __init__(self):
        self.tanks = []
        self.bullets = []
        self.walls = []
        self.scores = {}

    def update(self, events):
        # TODO: Implement specific game logic here
        pass

class TankBattleServicer(zace_tank_battle_pb2_grpc.TankBattleService):
    def __init__(self):
        self.map_grid = generate_map(SCREEN_HEIGHT // CELL_SIZE, SCREEN_HEIGHT // CELL_SIZE)
        self.game_state = MatchState()  # Centralized game state
        self.player_tanks = {}
        self._game_state_streams = {}  # Track open player streams

    def GetMapGrid(self, request, context):
        # Construct and return the map grid message
        map_grid_message = zace_tank_battle_pb2.MapGrid()
        for row in self.map_grid:
            map_row = map_grid_message.rows.add()  # Add rows directly to the message
            map_row.cells.extend(row)  # Add cells to the row
        return map_grid_message

    def JoinGame(self, request, context):
        # Generate player_id as SHA-256 hash of player_name
        player_name_bytes = request.player_name.encode('utf-8')
        player_id = hashlib.sha256(player_name_bytes).hexdigest()

        player_tank = zace_tank_battle_pb2.Tank(
            id=player_id,
            player_name=request.player_name,
            health=10,
            position=self._find_spawn_point(),
            direction="up"
        )

        self.player_tanks[player_id] = player_tank

         # Log player join information
        logging.info(f"Player joined: Player ID - {player_id}, Player Name - {request.player_name}")

        # Construct and return the initial game state
        initial_game_state = self.construct_game_state()
        yield initial_game_state

        # Start bidirectional streaming for real-time updates
        try:
            stream_context = context
            while True:
                # Implement your game state update logic
                # ...

                # Implement your event handling logic
                # events = self.process_events()
                # for event in events:
                #     event_message = self.convert_event_to_message(event)
                #     # Broadcast event to all clients
                #     stream_context.send(event_message)

                # Yield the updated game state
                updated_game_state = self.construct_game_state()
                
                yield updated_game_state

                # Sleep for a short duration to control the streaming rate
                time.sleep(0.1)

        except grpc.RpcError as e:
            print(f"Client disconnected: {e}")
        except GeneratorExit as e:
            print(f"Client disconnected: {player_id}:{request.player_name}")
            self._cleanup_player(player_id)

    def _cleanup_player(self, player_id):
        print(f"Delete player: {player_id}")
        # Remove the player's tank
        if player_id in self.player_tanks:
            del self.player_tanks[player_id]

        print(self.player_tanks)

        # Add additional cleanup logic for other entities associated with the player
        # ...

    def SendAction(self, request, context):
        player_id = request.player_id

        if request.action_type == "move":
            # Handle tank movement
            self.move_tank(player_id, request.direction)
        elif request.action_type == "shoot":
            # Handle tank shooting
            self.shoot_bullet(player_id, request.direction)

        # Update the game state based on other actions as needed
        # ...

        # Return an empty response
        return zace_tank_battle_pb2.Empty()

    def move_tank(self, player_id, direction):
        if player_id in self.player_tanks:
            tank = self.player_tanks[player_id]

            # Calculate the new position based on the provided direction
            new_x, new_y = tank.position.x, tank.position.y

            if direction == "up":
                new_y -= CELL_SIZE
            elif direction == "down":
                new_y += CELL_SIZE
            elif direction == "left":
                new_x -= CELL_SIZE
            elif direction == "right":
                new_x += CELL_SIZE

            # Check if the new position is within the valid map area
            valid_x = 0 <= new_x < (NUMBER_OF_CELL) * CELL_SIZE
            valid_y = 0 <= new_y < (NUMBER_OF_CELL) * CELL_SIZE

            if valid_x and valid_y and not self._is_occupied(new_x, new_y):
                # Update the tank's position
                tank.position.x = new_x
                tank.position.y = new_y

                # You may want to update other properties of the tank (e.g., direction) if needed
                tank.direction = direction

    def shoot_bullet(self, player_id, direction):
        # Implement bullet shooting logic
        # Create a new bullet, update the game state, and handle collisions
        # ...
        pass

    def process_events(self):
        # Implement your event processing logic
        # ...

        # Return a list of events
        return events

    def construct_game_state(self):
        # Implement your logic to construct the game state message
        game_state_message = zace_tank_battle_pb2.GameState()
        
        # Populate the message with tanks, bullets, walls, scores, etc.
        for tank in self.player_tanks.values():
            game_state_message.tanks.append(tank)

        # Include other game state components as needed
        # ...

        return game_state_message


    def _find_spawn_point(self):
        while True:
            # Generate random cell coordinates within the map area

            cell_x = random.randint(0, NUMBER_OF_CELL - 1)  
            cell_y = random.randint(0, NUMBER_OF_CELL - 1) 

            # Convert cell coordinates to pixel coordinates
            spawn_x = cell_x * CELL_SIZE  # Center of the cell
            spawn_y = cell_y * CELL_SIZE

            # Check if the spawn point is valid (not occupied by walls or other tanks)
            if not self._is_occupied(spawn_x, spawn_y):
                return zace_tank_battle_pb2.Point(x=spawn_x, y=spawn_y)


    def _is_occupied(self, x, y):
        """Checks if a given point on the map is occupied by a wall or another tank."""

        # Check for collisions with walls (using the generated wall coordinates)
        for row in range(len(self.map_grid)):
            for col in range(len(self.map_grid[0])):
                if self.map_grid[row][col] == "wall" and x == col * CELL_SIZE and y == row * CELL_SIZE:
                    return True

        # Check for collisions with other tanks (remains the same)
        for tank in self.player_tanks.values():
            if tank.position.x == x and tank.position.y == y:
                return True

        return False 

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Create a gRPC server
server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

# Add the TankBattleServicer to the server
zace_tank_battle_pb2_grpc.add_TankBattleServiceServicer_to_server(TankBattleServicer(), server)

# Start the server
server.add_insecure_port('[::]:65432')  # Bind to all interfaces on port 65432
server.start()
logging.info(f"Server started on port %d" % 65432)
server.wait_for_termination()
