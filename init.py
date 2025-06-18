import random
from typing import Set, Tuple, Dict, List

class MinesweeperGame:
    def __init__(self, grid_size: int = 9, mine_count: int = 10):
        self.grid_size = grid_size
        self.mine_count = mine_count
        self.mines: Set[Tuple[int, int]] = set()
        self.revealed: Set[Tuple[int, int]] = set()
        self.flagged: Set[Tuple[int, int]] = set()
        self.game_over = False
        self.win = False
        self.first_click = True
        self.board = [[0 for _ in range(grid_size)] for _ in range(grid_size)]
        
    def set_difficulty(self, difficulty: str):
        """Set game difficulty"""
        if difficulty == "beginner":
            self.grid_size = 9
            self.mine_count = 10
        elif difficulty == "intermediate":
            self.grid_size = 16
            self.mine_count = 40
        elif difficulty == "expert":
            self.grid_size = 16
            self.mine_count = 99
        else:
            # Default to beginner
            self.grid_size = 9
            self.mine_count = 10
        
        # Reset game with new settings
        self.reset_game()
        
    def place_mines(self, first_click_row: int, first_click_col: int):
        """Place mines randomly, avoiding the first clicked position"""
        self.mines.clear()
        
        while len(self.mines) < self.mine_count:
            row = random.randint(0, self.grid_size - 1)
            col = random.randint(0, self.grid_size - 1)
            
            # Avoid placing mine on first click
            if (row, col) != (first_click_row, first_click_col):
                self.mines.add((row, col))
        
        # Update board with mine positions
        for row, col in self.mines:
            self.board[row][col] = -1  # -1 represents a mine
        
        # Calculate numbers for all non-mine tiles
        self._calculate_numbers()
    
    def _calculate_numbers(self):
        """Calculate the number of adjacent mines for each tile"""
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                if (row, col) not in self.mines:
                    count = self._count_adjacent_mines(row, col)
                    self.board[row][col] = count
    
    def _count_adjacent_mines(self, row: int, col: int) -> int:
        """Count mines adjacent to a given position"""
        count = 0
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                new_row, new_col = row + dr, col + dc
                if (0 <= new_row < self.grid_size and 
                    0 <= new_col < self.grid_size and 
                    (new_row, new_col) in self.mines):
                    count += 1
        return count
    
    def click_tile(self, row: int, col: int) -> Dict:
        """Handle tile click and return game state update"""
        if self.game_over or (row, col) in self.revealed or (row, col) in self.flagged:
            return self._get_game_state()
        
        # Place mines on first click
        if self.first_click:
            self.place_mines(row, col)
            self.first_click = False
        
        # Check if clicked on mine
        if (row, col) in self.mines:
            self.game_over = True
            self.win = False
            self.revealed.add((row, col))
            return self._get_game_state()
        
        # Reveal the tile
        self.revealed.add((row, col))
        
        # Auto-reveal adjacent tiles if current tile has 0 adjacent mines
        if self.board[row][col] == 0:
            self._auto_reveal_adjacent(row, col)
        
        # Check for win condition
        if len(self.revealed) == self.grid_size * self.grid_size - self.mine_count:
            self.game_over = True
            self.win = True
        
        return self._get_game_state()
    
    def _auto_reveal_adjacent(self, row: int, col: int):
        """Automatically reveal adjacent tiles for empty tiles"""
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                new_row, new_col = row + dr, col + dc
                if (0 <= new_row < self.grid_size and 
                    0 <= new_col < self.grid_size and
                    (new_row, new_col) not in self.revealed and
                    (new_row, new_col) not in self.flagged):
                    
                    if (new_row, new_col) not in self.mines:
                        self.revealed.add((new_row, new_col))
                        # Recursively reveal if this tile also has 0 adjacent mines
                        if self.board[new_row][new_col] == 0:
                            self._auto_reveal_adjacent(new_row, new_col)
    
    def flag_tile(self, row: int, col: int) -> Dict:
        """Flag or unflag a tile"""
        if self.game_over or (row, col) in self.revealed:
            return self._get_game_state()
        
        if (row, col) in self.flagged:
            self.flagged.remove((row, col))
        else:
            self.flagged.add((row, col))
        
        return self._get_game_state()
    
    def reset_game(self):
        """Reset the game to initial state"""
        self.mines.clear()
        self.revealed.clear()
        self.flagged.clear()
        self.game_over = False
        self.win = False
        self.first_click = True
        self.board = [[0 for _ in range(self.grid_size)] for _ in range(self.grid_size)]
    
    def _get_game_state(self) -> Dict:
        """Get current game state for frontend"""
        return {
            'board': self.board,
            'revealed': list(self.revealed),
            'flagged': list(self.flagged),
            'mines': list(self.mines),
            'game_over': self.game_over,
            'win': self.win,
            'grid_size': self.grid_size,
            'mine_count': self.mine_count
        }
    
    def get_tile_value(self, row: int, col: int) -> int:
        """Get the value of a specific tile"""
        return self.board[row][col]
    
    def is_mine(self, row: int, col: int) -> bool:
        """Check if a tile is a mine"""
        return (row, col) in self.mines
    
    def is_revealed(self, row: int, col: int) -> bool:
        """Check if a tile is revealed"""
        return (row, col) in self.revealed
    
    def is_flagged(self, row: int, col: int) -> bool:
        """Check if a tile is flagged"""
        return (row, col) in self.flagged

# Global game instance
game = MinesweeperGame()

def get_game() -> MinesweeperGame:
    """Get the global game instance"""
    return game

def reset_game():
    """Reset the global game"""
    game.reset_game()

def set_difficulty(difficulty: str):
    """Set game difficulty"""
    game.set_difficulty(difficulty)

def click_tile(row: int, col: int) -> Dict:
    """Click a tile and return game state"""
    return game.click_tile(row, col)

def flag_tile(row: int, col: int) -> Dict:
    """Flag a tile and return game state"""
    return game.flag_tile(row, col)

def get_game_state() -> Dict:
    """Get current game state"""
    return game._get_game_state() 