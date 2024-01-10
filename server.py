import grpc
import logging
import random
from concurrent import futures

from helpers.generate_map import generate_map

import zace_tank_battle_pb2
import zace_tank_battle_pb2_grpc

from constants import *

class TankBattleServicer(zace_tank_battle_pb2_grpc.TankBattleService):

    def __init__(self):
        NUMBER_OF_CELL = SCREEN_HEIGHT // CELL_SIZE

        self.map_grid = generate_map(NUMBER_OF_CELL, NUMBER_OF_CELL)  # Generate the map once
        self.player_tanks = {}  # Track connected tanks (users)
        self.next_player_id = 1  # Assign unique IDs to joining tanks

    def GetMapGrid(self, request, context):
        map_grid_message = zace_tank_battle_pb2.MapGrid()

        for row in self.map_grid:
            map_row = zace_tank_battle_pb2.Row()
            for cell in row:
                map_row.cells.append(cell)

            map_grid_message.rows.append(map_row)

        return map_grid_message


    def JoinGame(self, request, context):
        logging.info(f"Player {request.player_name} is joining the game.")
        player_id = self.next_player_id
        self.next_player_id += 1

        # Create a new Tank object for the joining player
        player_tank = zace_tank_battle_pb2.Tank(
            id=player_id,
            player_name=request.player_name,
            health=10,  # Set initial health
            position=self._find_spawn_point(),  # Assign a spawn point
            direction="up"  # Set initial direction
        )
        self.player_tanks[player_id] = player_tank

        # Add the player's tank to the game state
        self._add_tank_to_game_state(player_tank)

        # Broadcast the updated game state to all connected players
        updated_game_state = self._create_game_state_message()
        for stream in self._game_state_streams.values():
            stream.send_message(updated_game_state)

        # Start streaming game state updates to the joining player
        for game_state in self._generate_game_updates():
            yield game_state


    def SendAction(self, request, context):
        logging.info(f"Received action from player {request.player_id}: {request.action_type}")
        # Process player action and update game state
        # ... (Implement game logic here)

        # Broadcast updated game state to all players
        updated_game_state = self._create_game_state_message()
        for stream in self._game_state_streams.values():
            stream.send_message(updated_game_state)

        return zace_tank_battle_pb2.Empty()

    # Helper methods for game state management
    def _generate_game_updates(self):
        while True:
            yield self._create_game_state_message()

    def _create_game_state_message(self):
        game_state = zace_tank_battle_pb2.GameState(
            tanks=list(self.player_tanks.values()),
            bullets=[],  # Replace with actual bullet data
            walls=[],  # Replace with actual wall data
            scores=self._calculate_scores(),
        )
        return game_state

    # ... (Other helper methods)

    def _find_spawn_point(self):
        while True:
            # Generate random cell coordinates within the map area
            cell_x = random.randint(0, 31)  # 32 cells wide
            cell_y = random.randint(0, 31)  # 24 cells tall for the map

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
