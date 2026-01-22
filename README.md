# Metal on the Road

Analyzing the Global Geography of Heavy Metal

An interactive data visualization exploring 183,000+ metal bands across 157 countries, using data from the Encyclopaedia Metallum (Metal Archives).

The genre shows all bands including ones I wouldn't consider "Heavy" (Guns N Roses, Kiss, etc.) 

For the individual bands, I curated the list to ensure only genres that are heavy would be included, even if some are loose with the genre.

---

## Key Findings

- **183,397 bands** catalogued from **157 countries**
- **United States** leads with 41,386 bands (22.6% of global total)
- **Black Metal** and **Death Metal** dominate globally (~50% combined)
- Regional genre preferences vary significantly:
  - Scandinavia & Europe → Black Metal dominant
  - Americas & Asia → Death Metal dominant
- **Russia** has the highest "active band" rate (64.3%) among top countries

### Spotify Popularity Insights
- **Bring Me The Horizon** ranks as the most popular heavy band (78/100)
- Metalcore dominates the modern heavy scene with 15 bands in the dataset
- Hardcore acts like Knocked Loose and Turnstile breaking into mainstream (60+ popularity)
- Death metal bands like Gojira proving extreme music has commercial appeal

---

## Tech Stack

- **Python** - Data cleaning and analysis (pandas, numpy)
- **Chart.js** - Interactive visualizations
- **HTML/CSS** - Custom dark-themed dashboard
- **Spotify Data** - Artist popularity and audio feature analysis

---

## Project Structure

```
metal-on-the-road/
├── data/
│   ├── metal_bands.csv           # Main band dataset (183K bands)
│   ├── all_bands_discography.csv # Album/release data (636K entries)
│   ├── heavy_bands_spotify.csv   # Curated heavy bands with Spotify data (50 bands)
│   └── ...                       # Additional datasets
├── analysis.py                   # Python analysis script
├── dashboard_data.json           # Processed data for visualization
├── index.html                    # Interactive dashboard
└── README.md
```

---

## Data Source

**Encyclopaedia Metallum (Metal Archives)** via [Kaggle](https://www.kaggle.com/datasets/guimacrlh/every-metal-archives-band-october-2024)

- Dataset: November 2024 snapshot
- License: Apache 2.0
- Contains: Band info, country, genre, status, discography

---

## Analysis Highlights

### Top 10 Metal Countries
| Rank | Country | Bands | % Global |
|------|---------|-------|----------|
| 1 | United States | 41,386 | 22.6% |
| 2 | Germany | 13,840 | 7.5% |
| 3 | Brazil | 8,408 | 4.6% |
| 4 | Italy | 8,100 | 4.4% |
| 5 | United Kingdom | 7,513 | 4.1% |
| 6 | France | 6,749 | 3.7% |
| 7 | Canada | 6,354 | 3.5% |
| 8 | Russia | 6,237 | 3.4% |
| 9 | Sweden | 5,966 | 3.3% |
| 10 | Finland | 5,469 | 3.0% |

### Genre Distribution
| Genre | Bands | % |
|-------|-------|---|
| Black Metal | 46,249 | 25.2% |
| Death Metal | 45,172 | 24.6% |
| Thrash Metal | 21,045 | 11.5% |
| Heavy Metal | 16,304 | 8.9% |
| Doom/Stoner | 13,314 | 7.3% |

### Spotify Popularity Rankings
| Rank | Artist | Genre | Popularity |
|------|--------|-------|------------|
| 1 | Bring Me The Horizon | Metalcore | 78 |
| 2 | Slipknot | Nu Metal | 75 |
| 3 | Sleep Token | Progressive Metal | 70 |
| 4 | Gojira | Death Metal | 68 |
| 5 | Lamb of God | Groove Metal | 65 |
| 6 | Turnstile | Hardcore | 65 |
| 7 | Architects | Metalcore | 64 |
| 8 | Bad Omens | Metalcore | 63 |
| 9 | Knocked Loose | Hardcore | 62 |
| 10 | Parkway Drive | Metalcore | 61 |

## Author

Bayden Blackwell
Data Analyst | Heavy Music Enthusiast