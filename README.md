# PGPg-Finder Comparative Heatmap

A Python script for combining and visualizing **Plant Growth-Promoting (PGP) gene annotation results** from multiple bacterial isolates into a single comparative heatmap.

Developed during comparative genomic analysis of *Atriplex nummularia* endophytic bacteria at [LABEM/UFRJ](http://www.labem.microbiologia.ufrj.br/), Universidade Federal do Rio de Janeiro (2025).

---

## What this does

[PGPg Finder](https://github.com/tpellegrinetti/PGPg_finder) annotates plant growth-promoting traits (PGPTs) in bacterial genomes individually — one output folder per isolate. This script:

1. Automatically detects all `_PGPg` output folders in a root directory
2. Merges the `gene_counts_Lv3.txt` (or `Lv4`) tables from all isolates
3. Applies **row-wise Z-score normalization** to each functional category
4. Saves a heatmap image and the merged data tables as CSV

The Z-score is applied per row (functional category), answering:
> *"How enriched is this PGP function in each isolate compared to all others?"*

---

## Installation

```bash
git clone https://github.com/mtrujilloma/pgpg-comparative-heatmap.git
cd pgpg-comparative-heatmap
pip install -r requirements.txt
```

---

## Usage

### Expected input structure

```
annotated_genomes/
├── isolate_A_PGPg/
│   └── tables/
│       └── non-normalized/
│           ├── gene_counts_Lv3.txt
│           └── gene_counts_Lv4.txt
├── isolate_B_PGPg/
│   └── tables/non-normalized/gene_counts_Lv3.txt
└── ...
```

### Run

```bash
python pgpg_heatmap.py --input /path/to/annotated_genomes/ --output results/
```

### All options

| Argument | Default | Description |
|----------|---------|-------------|
| `--input` / `-i` | required | Root folder containing `_PGPg` subfolders |
| `--output` / `-o` | required | Folder where outputs will be saved |
| `--level` | `Lv3` | Functional annotation level: `Lv3` or `Lv4` |
| `--cmap` | `viridis` | Any [matplotlib colormap](https://matplotlib.org/stable/gallery/color/colormap_reference.html) |
| `--figsize` | `14 10` | Figure width and height in inches |
| `--dpi` | `300` | Output image resolution |

---

## Outputs

| File | Description |
|------|-------------|
| `heatmap_pgpg_Lv3.png` | Comparative heatmap (Z-score normalized) |
| `combined_gene_counts_Lv3.csv` | Raw merged gene count table |
| `zscore_matrix_Lv3.csv` | Z-score matrix used for the heatmap |

---

## Scientific context

This script was developed as part of a comparative genomic study evaluating the phytoremediation and plant growth-promoting potential of 23 endophytic bacterial isolates from *Atriplex nummularia*, a halophyte plant with high tolerance to salinity and heavy metals. Genomes were annotated with PGPg Finder v1.1.0 using the PLaBAse database (Patz et al., 2021).

Related publication: *(in preparation)*

---

## References

Pellegrinetti, T. A., et al. (2024). PGPg_finder: A comprehensive and user-friendly pipeline for identifying plant growth-promoting genes in genomic and metagenomic data. *Rhizosphere*.

Patz, S., et al. (2021). PLaBAse: A comprehensive web resource for analyzing the plant growth-promoting potential of plant-associated bacteria [preprint].


---

*Developed at LABEM — Laboratory of Biotechnology and Microbial Ecology, UFRJ, Brazil.*
Author: Mariana Trujillo
