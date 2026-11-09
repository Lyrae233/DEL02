
# Spotify Autoplay — Mesa Agent-Based Model

## 1. Project Overview

This project implements a simplified Spotify Autoplay recommendation system using the Mesa agent-based modelling framework.

The model investigates how different artist and genre similarity weights affect song-selection patterns. It uses a synthetic music catalogue and compares the distribution of four song-transition categories.

This model does not reproduce Spotify's actual recommendation algorithm.

## 2. Model Description

The model contains:

- 1 recommendation agent responsible for selecting the next song.
- 50 fictional songs from 10 artists across 5 genres.
- A weighted song-transition network based on artist and genre similarity.
- 25 song selections per simulation.
- 100 simulations per experimental condition.

The agent selects each next song probabilistically using:

- Artist similarity weight
- Genre similarity weight
- Baseline selection weight of 0.1

The model records four transition categories:

1. Same artist, same genre
2. Same artist, different genre
3. Different artist, same genre
4. Different artist, different genre (neither match)

## 3. Experimental Conditions

Two conditions are compared:

| Condition | Artist Weight | Genre Weight |
|---|---|---|
| Baseline | 0.5 | 0.5 |
| Alternative | 0.7 | 0.3 |

All other model settings remain unchanged between conditions.

Each condition includes 100 simulations with 25 song selections per simulation, producing 2,500 transitions per condition.

The same set of random seeds, starting at 42, is used for both conditions to support reproducibility.

## 4. Project Structure

```text
spotify-autoplay-model/
├── README.md
├── requirements.txt
├── src/
│   ├── virus_on_network/
│   │   ├── agents.py
│   │   ├── model.py
│   │   ├── app.py
│   │   └── SOURCE.md
│   └── project_model/
│       ├── agents.py
│       ├── model.py
│       └── app.py
├── docs/
└── outputs/
```

- `src/virus_on_network/` contains the original Mesa example.
- `src/project_model/` contains the adapted Spotify Autoplay model.
- `outputs/` contains simulation results and visualizations.
- `docs/` contains supporting documentation.

## 5. Installation

### Requirements

- Python
- Mesa
- NetworkX
- Matplotlib
- Solara (for the original Mesa example visualization)

Install the required dependencies from the repository root:

```bash
python -m pip install -r requirements.txt
```

The dependency versions should be recorded in `requirements.txt`.

## 6. Running the Models

### 6.1 Original Mesa Example

The original Virus on a Network example is located in:

`src/virus_on_network/`

To launch its Solara visualization:

```bash
solara run src/virus_on_network/app.py
```

The original `app.py` imports components from the installed Mesa example, so a compatible Mesa installation is required.

### 6.2 Spotify Autoplay Model

Run the adapted model from the repository root:

```bash
python -m src.project_model.app
```

This command:

1. Runs 100 baseline simulations.
2. Runs 100 alternative simulations.
3. Records 25 song selections per simulation.
4. Calculates transition statistics.
5. Generates CSV files and visualizations.

The results are saved in the `outputs/` folder.

No external datasets or Spotify account are required.

## 7. Generated Outputs

The model produces the following output files:

| Filename | Description |
|---|---|
| `baseline_raw_00_song_transitions.csv` | Individual song transitions from baseline simulations |
| `alternative_raw_00_song_transitions.csv` | Individual song transitions from alternative simulations |
| `baseline_processed_00_transition_summary.csv` | Average baseline transition percentages and standard deviations |
| `alternative_processed_00_transition_summary.csv` | Average alternative transition percentages and standard deviations |
| `baseline_processed_01_transition_chart.png` | Baseline transition distribution |
| `alternative_processed_01_transition_chart.png` | Alternative transition distribution |
| `baseline_processed_02_baseline_vs_alternative.png` | Comparison of both conditions |

The processed results include the mean percentage and standard deviation of each transition category across 100 simulations.

## 8. Original Mesa Example and Adaptation

### Original Source

**Example:** Virus on a Network

**Framework:** Mesa

**Documentation:**  
https://mesa.readthedocs.io/stable/examples/basic/virus_on_network.html

**Original Repository:**  
https://github.com/mesa/mesa

The original model simulates virus transmission between connected agents through probabilistic infection and recovery rules.

### Project Adaptation

The Spotify Autoplay model adapts the network-based and probabilistic modelling approach.

The main changes include:

- Replacing the virus agent with an Autoplay recommendation agent.
- Representing songs as network nodes with artist and genre attributes.
- Replacing infection probability with weighted song-selection probability.
- Recording song-transition categories instead of infection states.
- Comparing artist-focused and balanced recommendation conditions.

The original source example is kept separately from the adapted model.

Additional source information is documented in `src/virus_on_network/SOURCE.md`.

## 9. Known Limitations

- All songs, artists, and genres are synthetic.
- The selection weights are hypothetical and do not represent Spotify's actual recommendation algorithm.
- The model does not simulate active listener behaviour such as skipping, liking, or changing preferences.
- Popularity, listening history, and other recommendation factors are excluded.
- Previously played songs may be recommended again, although the immediately preceding song is excluded.
- The current analysis focuses on transition patterns rather than directly measuring the number of unique unfamiliar artists.
- The Spotify adaptation does not currently include an interactive visualization.

The simulation results only describe the behaviour of this simplified model under the specified conditions. They cannot establish how Spotify's actual recommendation system operates or how real users discover music.

## 10. Future Improvements

Possible future improvements include:

- Adding a genre-focused weighting condition (30% artist, 70% genre).
- Measuring unique unfamiliar artists encountered in each simulation.
- Comparing genre diversity across conditions.
- Adding an interactive visualization of the song-transition network.
- Examining how different catalogue structures affect recommendation outcomes.