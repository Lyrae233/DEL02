
import csv
from collections import Counter
from pathlib import Path
from statistics import mean, stdev

import matplotlib.pyplot as plt

from model import SpotifyAutoplayModel


OUTPUT_DIR = Path(__file__).resolve().parents[2] / "outputs"

NUM_RUNS = 100
STEPS_PER_RUN = 25
BASE_SEED = 42

CATEGORIES = [
    "same_artist_same_genre",
    "same_artist_different_genre",
    "different_artist_same_genre",
    "neither_match",
]

LABELS = [
    "Same artist\nSame genre",
    "Same artist\nDifferent genre",
    "Different artist\nSame genre",
    "Neither match",
]


def save_csv(filename, fieldnames, rows):
    with (OUTPUT_DIR / filename).open("w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def run_condition(condition, artist_weight):
    all_transitions = []
    run_counts = []

    for run in range(NUM_RUNS):
        model = SpotifyAutoplayModel(
            artist_weight=artist_weight,
            rng=BASE_SEED + run
        )

        # Run 25 song selections
        for _ in range(STEPS_PER_RUN):
            model.step()

        # Store individual transitions
        for transition in model.transitions:
            all_transitions.append({
                "run": run + 1,
                **transition
            })

        # Count transition categories for this run
        counts = Counter(
            row["category"] for row in model.transitions
        )
        run_counts.append(counts)

    # Raw output: all 2,500 transitions
    save_csv(
        f"{condition}_raw_00_song_transitions.csv",
        [
            "run", "step", "from_song", "to_song",
            "category", "unfamiliar_artist"
        ],
        all_transitions
    )

    # Calculate average results across runs
    summary = []

    for category in CATEGORIES:
        counts = [run[category] for run in run_counts]
        percentages = [
            count / STEPS_PER_RUN * 100
            for count in counts
        ]

        summary.append({
            "category": category,
            "mean_count": round(mean(counts), 2),
            "mean_percentage": round(mean(percentages), 2),
            "std_percentage": round(stdev(percentages), 2)
        })

    save_csv(
        f"{condition}_processed_00_transition_summary.csv",
        [
            "category", "mean_count",
            "mean_percentage", "std_percentage"
        ],
        summary
    )

    return summary


def create_chart(condition, summary):
    means = [row["mean_percentage"] for row in summary]
    stds = [row["std_percentage"] for row in summary]

    plt.figure(figsize=(10, 6))
    plt.bar(LABELS, means, yerr=stds, capsize=5)

    plt.title(f"{condition.capitalize()} - 100 Simulation Runs")
    plt.ylabel("Average Percentage of Transitions (%)")
    plt.ylim(0, 100)
    plt.tight_layout()

    plt.savefig(
        OUTPUT_DIR / f"{condition}_processed_01_transition_chart.png",
        dpi=200
    )
    plt.close()


def create_comparison_chart(baseline, alternative):
    positions = list(range(len(CATEGORIES)))
    width = 0.35

    baseline_means = [
        row["mean_percentage"] for row in baseline
    ]
    alternative_means = [
        row["mean_percentage"] for row in alternative
    ]

    baseline_stds = [
        row["std_percentage"] for row in baseline
    ]
    alternative_stds = [
        row["std_percentage"] for row in alternative
    ]

    plt.figure(figsize=(11, 6))

    plt.bar(
        [x - width / 2 for x in positions],
        baseline_means,
        width,
        yerr=baseline_stds,
        capsize=4,
        label="Baseline (50/50)"
    )

    plt.bar(
        [x + width / 2 for x in positions],
        alternative_means,
        width,
        yerr=alternative_stds,
        capsize=4,
        label="Alternative (70/30)"
    )

    plt.xticks(positions, LABELS)
    plt.ylabel("Average Percentage of Transitions (%)")
    plt.title("Spotify Autoplay - Condition Comparison")
    plt.ylim(0, 100)
    plt.legend()
    plt.tight_layout()

    plt.savefig(
        OUTPUT_DIR / "baseline_processed_02_baseline_vs_alternative.png",
        dpi=200
    )
    plt.close()


if __name__ == "__main__":
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    baseline = run_condition("baseline", 0.5)
    alternative = run_condition("alternative", 0.7)

    create_chart("baseline", baseline)
    create_chart("alternative", alternative)
    create_comparison_chart(baseline, alternative)

    print("BASELINE RESULTS")
    for row in baseline:
        print(row)

    print("\nALTERNATIVE RESULTS")
    for row in alternative:
        print(row)

    print("\nAll results saved to outputs/")
