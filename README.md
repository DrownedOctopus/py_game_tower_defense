# Errour: Canto

A sci-fi tower defense game built with **Python** and **pygame-ce**. Place towers along the battlefield, socket them with soul gems, and hold the line against waves of monsters as you push across an interstellar overworld map.

## Gameplay

- **Tower & Gem system** — Towers are empty until you insert a gem. Each gem (Fire, Frost, Poison, and more) has its own damage, range, and fire rate, and can be upgraded through tiers and star ranks for stronger effects.
- **Gem Bag & Stash** — Manage your collected gems, swap them between towers mid-battle, and build new ones through each round.
- **Wave-based combat** — Enemies spawn in scripted waves defined in JSON, growing tougher as each level progresses.
- **Smart enemy pathing** — Monsters navigate the map using A* pathfinding.
- **Overworld progression** — Travel between levels on a sci-fi overworld map, unlocking new stages as you complete previous ones.
- **Persistent saves** — Progress, unlocked levels, and your gem inventory are saved between sessions.

## Requirements

- Python 3.x
- [Pygame](https://www.pygame.org/)

```bash
pip install pygame
```

## Running the Game

```bash
python main.py
```

## Controls

- **Left click** — Select / place towers and gems / rush waves
- **Drag & drop** — Move gems between towers, bag, and stash

## Project Structure

```
scripts/
├── tower_defense.py     # Core game loop and scene management
├── overworld_map.py     # Level-select overworld scene
├── menu.py               # Main menu
├── tower.py              # Tower behavior and rendering
├── gem.py / gem_token.py # Gem entities and drag/drop tokens
├── gem_factory.py        # Builds gems from data definitions
├── gem_bag.py            # Player's gem inventory
├── gem_stash.py          # Gem storage UI
├── tilemap.py            # Tile-based map loading and rendering
├── pathfinding.py        # A* pathfinding for monster movement
├── ui.py                 # Custom UI framework (buttons, panels)
├── progression.py        # Level completion and unlock logic
└── utils/                # Asset loading, save/load, audio helpers
data/                      # Level, monster, gem, and map definitions (JSON)
main.py                    # Entry point
```

## Screenshots / Gameplay

<img width="1276" height="717" alt="Errour_Screenshot" src="https://github.com/user-attachments/assets/f4d714f6-3244-4090-895f-b8cc3ea5b689" />

## Status

This project is a **playable demo and still under active development**. Expect rough edges, missing polish, and features in progress.

## License

All rights reserved
