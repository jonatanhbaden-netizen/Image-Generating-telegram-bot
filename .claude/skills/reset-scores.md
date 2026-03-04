# Reset Scores

Reset the scoreboard and reload the game to a clean state.

## Steps

1. Open `tic-tac-toe.html` in a browser
2. Open the browser console (F12 → Console)
3. Run:
   ```js
   scores = { X: 0, O: 0, D: 0 };
   document.getElementById('score').textContent = 'X: 0 | O: 0 | Draws: 0';
   init();
   ```

Or refresh the page — scores are not persisted to `localStorage`, so a page reload resets everything.
