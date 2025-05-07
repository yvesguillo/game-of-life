# *Conway's Game of Life* — Yet another Python edition

![Conway's Game of Life](images/gol.avif)

Welcome to the beautiful chaos of cellular automata! This is a **Tkinter** + **NumPy** implementation of [**Conway's Game of Life**](https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life), where simple rules create mesmerizing patterns. It's fast, interactive, and maybe a bit addictive.

## Why Game of Life?

Because it’s *life*, literally.  
Proposed by [*Matthieu Amiguet*](https://matthieuamiguet.ch/) as an exercise during *HE-Arc*'s *CAS-IDD*'s *Python* module, *Conway's Game of Life* is the perfect blend of simplicity and complexity:
- The rules are minimal.
- The behavior is unpredictable.
- The vibes? Immaculate.

It’s also a brilliant excuse to play with:
- NumPy (yay for matrix magic!)
- Tkinter (surprisingly fun)
- Python (of course)

## Use Cases

- Learn how cellular automata work.
- Experiment with pattern evolution.
- Geek out for hours optimizing the logic.
- Brainstorm new simulations or visualizations.

Or just… stare at it. It’s oddly relaxing.

## Getting Started

This project runs a GUI window where you may:
- **Left-click** to toggle cells manually.
- **Right-click** to start/pause the simulation.
- Watch life unfold. Or implode.

## Requirements

You'll need Python **3.7+** and a couple of friendly packages:

```bash
pip install numpy
````

Tkinter is usually included with Python by default. If not:

- On Ubuntu/Debian: `sudo apt install python3-tk`
- On macOS: You’re probably fine
- On Windows: Already bundled!

## Installation

Clone the repo and enter the simulation lab:

```bash
git clone https://github.com/yvesguillo/game-of-life.git
cd game-of-life
```

## Quick Start

To run with the default grid and some randomized chaos:

```bash
python gol.py
```

Or get fancy:

```bash
python gol.py --width 128 --height 64 --cell-size 8 --delay 16 --random-cell 128
```

**Pro tips:**

- Tweak `--h-line` or `--v-line` to add predefined chaos (horizontal or vertical lines).
- Use bigger `--cell-size` to zoom in.

## Status

- Fully working
- Fast thanks to NumPy
- GUI included
- Pretty colors for cells
- Ready for more upgrades

## Roadmap & Crazy Ideas

- Add pattern import/export (e.g. gliders, pulsars, etc.)
- Color-coded lifespans? Yes please.
- Save/load board state
- Infinite grid with panning/zoom
- Shader-based rendering (just because)
- Web version (maybe with WebAssembly)

Got ideas? Spot a bug? Wanna make this thing even cooler? Open an issue or shoot a PR — we’d love to hear from you!

Made with 𖹭, Python, and curiosity.
