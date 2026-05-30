#!/usr/bin/env python3
"""
pgpg_heatmap.py
===============
Combines PGPg-Finder results from multiple bacterial isolates into a single
comparative heatmap using Z-score normalization per functional category (Lv3).

The Z-score is applied row-wise (axis=1), answering the question:
    "How enriched is this function in each bacterium compared to all others?"

Developed during comparative genomic analysis of Atriplex nummularia
endophytic bacteria at LABEM/UFRJ (2025).

Usage
-----
    python pgpg_heatmap.py --input /path/to/annotated_genomes/ --output /path/to/output/

Requirements
------------
    pip install pandas seaborn matplotlib scipy

Author: Mariana Trujillo
"""

import os
import argparse
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import zscore


def parse_args():
    parser = argparse.ArgumentParser(
        description="Comparative PGPg-Finder heatmap across multiple bacterial isolates."
    )
    parser.add_argument("--input",   "-i", required=True, help="Root directory containing per-isolate _PGPg folders")
    parser.add_argument("--output",  "-o", required=True, help="Output directory for heatmap and CSV tables")
    parser.add_argument("--level",   default="Lv3", choices=["Lv3", "Lv4"], help="Functional level (default: Lv3)")
    parser.add_argument("--cmap",    default="viridis", help="Matplotlib colormap (default: viridis)")
    parser.add_argument("--figsize", nargs=2, type=int, metavar=("W", "H"), default=[14, 10], help="Figure size in inches (default: 14 10)")
    parser.add_argument("--dpi",     type=int, default=300, help="Output image resolution (default: 300)")
    return parser.parse_args()


def main():
    args = parse_args()
    os.makedirs(args.output, exist_ok=True)

    root_dir = args.input
    level    = args.level

    # Find gene_counts files inside _PGPg subfolders
    file_paths = []
    for folder in os.listdir(root_dir):
        full_path = os.path.join(root_dir, folder)
        if os.path.isdir(full_path) and folder.endswith("_PGPg"):
            filepath = os.path.join(full_path, "tables", "non-normalized", f"gene_counts_{level}.txt")
            if os.path.isfile(filepath):
                isolate = folder.replace("_PGPg", "")
                file_paths.append((isolate, filepath))

    # Read and merge all files
    combined_df = pd.DataFrame()
    for isolate, path in file_paths:
        df = pd.read_csv(path, sep="\t")
        df.columns = [level, isolate]
        combined_df = df if combined_df.empty else pd.merge(combined_df, df, on=level, how="outer")

    # Fill NA with 0 and apply row-wise Z-score
    combined_df = combined_df.fillna(0)
    combined_df.set_index(level, inplace=True)
    zscored_df = combined_df.apply(zscore, axis=1)
    zscored_df = pd.DataFrame(zscored_df.tolist(), index=combined_df.index, columns=combined_df.columns)
    zscored_df = zscored_df.dropna(how='any')

    # Plot heatmap
    plt.figure(figsize=tuple(args.figsize))
    sns.heatmap(zscored_df, cmap=args.cmap, linewidths=0.5)
    plt.title("PGPg-Finder heatmap")
    plt.tight_layout()

    # Save outputs
    plt.savefig(os.path.join(args.output, f"heatmap_pgpg_{level}.png"), dpi=args.dpi)
    combined_df.to_csv(os.path.join(args.output, f"combined_gene_counts_{level}.csv"))
    zscored_df.to_csv(os.path.join(args.output, f"zscore_matrix_{level}.csv"))


if __name__ == "__main__":
    main()
