# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Single-file static web project: a tic-tac-toe game with score tracking.

## Running the Project

Open `tic-tac-toe.html` directly in a browser. No build step, server, or dependencies required.

## Architecture

All game logic, styles, and markup live in `tic-tac-toe.html`. There are no external files, frameworks, or package managers.

### Key JS state (inline `<script>`)
- `board`: flat 9-element array of `''`, `'X'`, or `'O'`
- `current`: active player (`'X'` or `'O'`)
- `over`: boolean, prevents moves after game ends
- `scores`: `{ X, O, D }` — persists across games within a session
- `WINS`: hardcoded array of the 8 winning index triples

### Game flow
1. `init()` resets `board`, `current`, and `over`; clears cell classes/text
2. Click handler on each `.cell` updates `board`, applies CSS classes (`x`/`o`, `taken`), calls `checkWin()`
3. `checkWin()` iterates `WINS` and returns the winning triple or `null`
4. Win → highlight cells with `.win` class, increment score; draw → all cells filled, no winner

### CSS classes of note
- `.taken` — prevents re-clicking a cell (checked via `board[i]`, not the class)
- `.win` — glowing highlight on winning cells
- `.x` / `.o` — player-specific text color

## Git Workflow

This project uses Git (local) and GitHub (remote) for version control.
Remote: https://github.com/jonatanhbaden-netizen/tic-tac-toe

### Rules for Claude Code
- After every meaningful change, commit and push to GitHub
- Write clean, descriptive commit messages that explain what changed and why
- Never leave work uncommitted — every completed task should result in a pushed commit
- This ensures the project history is always recoverable and up to date
