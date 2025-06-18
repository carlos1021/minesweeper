let GRID_SIZE = 9;

let gameState = {
    board: [],
    revealed: [],
    flagged: [],
    mines: [],
    game_over: false,
    win: false,
    grid_size: GRID_SIZE,
    mine_count: 10
};

// Number images mapping
const numberImages = {
    1: '/static/media/one.png',
    2: '/static/media/two.png',
    3: '/static/media/three.png',
    4: '/static/media/four.png',
    5: '/static/media/five.png',
    6: '/static/media/six.png',
    7: '/static/media/seven.png',
    8: '/static/media/eight.png',
    9: '/static/media/nine.png'
};

function initializeGame() {
    // Get initial game state from server
    fetch('/game_state')
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                gameState = data.game_state;
                GRID_SIZE = gameState.grid_size;
                updateGridCSS();
                renderGrid();
                updateInfo();
            }
        })
        .catch(error => {
            console.error('Error getting game state:', error);
            renderGrid();
            updateInfo();
        });
}

function updateGridCSS() {
    const gridElement = document.getElementById('grid');
    gridElement.style.gridTemplateColumns = `repeat(${GRID_SIZE}, 30px)`;
    gridElement.style.gridTemplateRows = `repeat(${GRID_SIZE}, 30px)`;
}

function updateDifficultyButtons(activeDifficulty) {
    // Remove active class from all buttons
    document.querySelectorAll('.difficulty-button').forEach(button => {
        button.classList.remove('active');
    });
    
    // Add active class to the selected difficulty
    const activeButton = document.querySelector(`[onclick="setDifficulty('${activeDifficulty}')"]`);
    if (activeButton) {
        activeButton.classList.add('active');
    }
}

async function setDifficulty(difficulty) {
    try {
        const response = await fetch('/set_difficulty', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                difficulty: difficulty
            })
        });
        
        if (response.ok) {
            const data = await response.json();
            if (data.success) {
                gameState = data.game_state;
                GRID_SIZE = gameState.grid_size;
                updateGridCSS();
                updateDifficultyButtons(difficulty);
                renderGrid();
                updateInfo();
                updateGameStatus();
            }
        }
    } catch (error) {
        console.error('Error setting difficulty:', error);
    }
}

async function revealTile(row, col) {
    try {
        const response = await fetch('/click_tile', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                row: row,
                col: col
            })
        });
        
        if (response.ok) {
            const data = await response.json();
            if (data.success) {
                gameState = data.game_state;
                renderGrid();
                updateInfo();
                updateGameStatus();
            }
        }
    } catch (error) {
        console.error('Error sending tile click:', error);
    }
}

async function flagTile(row, col) {
    try {
        const response = await fetch('/flag_tile', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                row: row,
                col: col
            })
        });
        
        if (response.ok) {
            const data = await response.json();
            if (data.success) {
                gameState = data.game_state;
                renderGrid();
                updateInfo();
            }
        }
    } catch (error) {
        console.error('Error flagging tile:', error);
    }
}

function renderGrid() {
    const gridElement = document.getElementById('grid');
    gridElement.innerHTML = '';

    for (let row = 0; row < GRID_SIZE; row++) {
        for (let col = 0; col < GRID_SIZE; col++) {
            const tile = document.createElement('div');
            tile.className = 'tile';
            
            // Add click handlers
            tile.onclick = () => revealTile(row, col);
            tile.oncontextmenu = (e) => {
                e.preventDefault();
                flagTile(row, col);
            };

            const isRevealed = gameState.revealed.some(pos => pos[0] === row && pos[1] === col);
            const isFlagged = gameState.flagged.some(pos => pos[0] === row && pos[1] === col);
            const isMine = gameState.mines.some(pos => pos[0] === row && pos[1] === col);
            const tileValue = gameState.board[row] ? gameState.board[row][col] : 0;

            if (isFlagged) {
                // Show flag
                tile.textContent = '🚩';
            } else if (isRevealed) {
                tile.classList.add('revealed');
                
                if (isMine) {
                    tile.classList.add('mine');
                    tile.textContent = '💣';
                } else if (tileValue > 0) {
                    // Show number
                    if (numberImages[tileValue]) {
                        const img = document.createElement('img');
                        img.src = numberImages[tileValue];
                        img.width = 20;
                        img.height = 20;
                        tile.appendChild(img);
                    } else {
                        tile.textContent = tileValue;
                    }
                } else {
                    // Empty tile (0 value) - add empty class for darker background
                    tile.classList.add('empty');
                }
            }

            gridElement.appendChild(tile);
        }
    }
}

function updateInfo() {
    document.getElementById('revealed-count').textContent = gameState.revealed.length;
    document.getElementById('mine-count').textContent = gameState.mine_count;
}

function updateGameStatus() {
    const statusElement = document.getElementById('game-status');
    if (gameState.game_over) {
        if (gameState.win) {
            statusElement.textContent = 'YAYYYYY Congratulations! You won!';
        } else {
            statusElement.textContent = 'NOOOOO Game Over! You hit a mine!';
        }
    } else {
        statusElement.textContent = '';
    }
}

async function resetGame() {
    try {
        const response = await fetch('/reset_game', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            }
        });
        
        if (response.ok) {
            const data = await response.json();
            if (data.success) {
                gameState = data.game_state;
                renderGrid();
                updateInfo();
                updateGameStatus();
            }
        }
    } catch (error) {
        console.error('Error resetting game:', error);
    }
}

// Initialize the game when page loads
window.onload = initializeGame; 