import pandas as pd
import numpy as np
import json
from collections import Counter
import re

def load_and_clean_data():
    print("Loading metal_bands.csv...")
    df = pd.read_csv('data/metal_bands.csv', encoding='utf-8')
    
    print(f"Raw dataset: {len(df):,} bands")
    
    df.columns = df.columns.str.strip()
    df = df.dropna(subset=['Country'])
    df['Country'] = df['Country'].str.strip()
    df['Primary_Genre'] = df['Genre'].apply(extract_primary_genre)
    df['Genre_Category'] = df['Primary_Genre'].apply(map_to_genre_category)
    
    print(f"Cleaned dataset: {len(df):,} bands")
    
    return df


def extract_primary_genre(genre_str):
    if pd.isna(genre_str):
        return 'Unknown'
    
    genre = re.split(r'[/,]|\swith\s', str(genre_str))[0]
    return genre.strip()


def map_to_genre_category(genre):
    genre_lower = genre.lower()
    if any(x in genre_lower for x in ['black', 'atmospheric black']):
        return 'Black Metal'
    elif any(x in genre_lower for x in ['death', 'brutal', 'technical death']):
        return 'Death Metal'
    elif any(x in genre_lower for x in ['thrash', 'crossover']):
        return 'Thrash Metal'
    elif any(x in genre_lower for x in ['doom', 'stoner', 'sludge']):
        return 'Doom/Stoner'
    elif any(x in genre_lower for x in ['power', 'symphonic']):
        return 'Power/Symphonic'
    elif any(x in genre_lower for x in ['progressive', 'prog']):
        return 'Progressive'
    elif any(x in genre_lower for x in ['heavy metal', 'traditional', 'nwobhm']):
        return 'Heavy Metal'
    elif any(x in genre_lower for x in ['grind', 'gore']):
        return 'Grindcore'
    elif any(x in genre_lower for x in ['metalcore', 'deathcore', 'hardcore']):
        return 'Core'
    elif any(x in genre_lower for x in ['folk', 'viking', 'pagan']):
        return 'Folk/Viking'
    elif any(x in genre_lower for x in ['industrial', 'electronic']):
        return 'Industrial'
    elif any(x in genre_lower for x in ['groove']):
        return 'Groove Metal'
    elif any(x in genre_lower for x in ['speed']):
        return 'Speed Metal'
    else:
        return 'Other'

def analyze_by_country(df):
    
    country_stats = df.groupby('Country').agg({
        'Band ID': 'count',
        'Genre_Category': lambda x: x.mode().iloc[0] if len(x) > 0 else 'Unknown'
    }).rename(columns={'Band ID': 'Band_Count', 'Genre_Category': 'Dominant_Genre'})
    
    country_stats = country_stats.sort_values('Band_Count', ascending=False)
    
    total = country_stats['Band_Count'].sum()
    country_stats['Percentage'] = (country_stats['Band_Count'] / total * 100).round(2)
    
    return country_stats


def analyze_genre_by_region(df):
    
    regions = {
        'Scandinavia': ['Sweden', 'Norway', 'Finland', 'Denmark', 'Iceland'],
        'Western Europe': ['Germany', 'United Kingdom', 'France', 'Netherlands', 'Belgium', 'Austria', 'Switzerland'],
        'Southern Europe': ['Italy', 'Spain', 'Portugal', 'Greece'],
        'Eastern Europe': ['Poland', 'Russia', 'Czech Republic', 'Ukraine', 'Hungary', 'Romania'],
        'North America': ['United States', 'Canada'],
        'South America': ['Brazil', 'Argentina', 'Chile', 'Colombia', 'Mexico'],
        'Asia': ['Japan', 'China', 'Indonesia', 'India', 'Philippines'],
        'Oceania': ['Australia', 'New Zealand']
    }
    
    region_data = []
    for region, countries in regions.items():
        region_df = df[df['Country'].isin(countries)]
        if len(region_df) > 0:
            genre_counts = region_df['Genre_Category'].value_counts()
            total = len(region_df)
            
            region_data.append({
                'Region': region,
                'Total_Bands': total,
                'Top_Genre': genre_counts.index[0],
                'Top_Genre_Pct': round(genre_counts.iloc[0] / total * 100, 1),
                'Genre_Distribution': genre_counts.head(5).to_dict()
            })
    
    return pd.DataFrame(region_data)


def analyze_status_distribution(df):
    
    status_by_country = df.groupby(['Country', 'Status']).size().unstack(fill_value=0)
    
    if 'Active' in status_by_country.columns:
        status_by_country['Total'] = status_by_country.sum(axis=1)
        status_by_country['Active_Rate'] = (
            status_by_country['Active'] / status_by_country['Total'] * 100
        ).round(1)
    
    return status_by_country.sort_values('Total', ascending=False)


def get_genre_evolution(df, discography_df):
    
    merged = discography_df.merge(
        df[['Band ID', 'Genre_Category']], 
        on='Band ID', 
        how='inner'
    )
    
    
    merged['Year'] = pd.to_numeric(merged['Year'], errors='coerce')
    merged = merged.dropna(subset=['Year'])
    merged['Decade'] = (merged['Year'] // 10 * 10).astype(int)
    
    merged = merged[(merged['Decade'] >= 1970) & (merged['Decade'] <= 2020)]
    
    evolution = merged.groupby(['Decade', 'Genre_Category']).size().unstack(fill_value=0)
    
    evolution_pct = evolution.div(evolution.sum(axis=1), axis=0) * 100
    
    return evolution_pct

def export_for_dashboard(df, country_stats, region_stats):
    top_countries = country_stats.head(30).reset_index()
    top_countries_data = top_countries.to_dict('records')
    global_genres = df['Genre_Category'].value_counts()
    genre_data = [{'genre': k, 'count': int(v)} for k, v in global_genres.items()]
    region_data = region_stats.to_dict('records')
    
    country_coords = {
        'United States': {'lat': 39.8, 'lon': -98.5},
        'Germany': {'lat': 51.2, 'lon': 10.4},
        'Brazil': {'lat': -14.2, 'lon': -51.9},
        'Italy': {'lat': 41.9, 'lon': 12.6},
        'United Kingdom': {'lat': 55.4, 'lon': -3.4},
        'France': {'lat': 46.2, 'lon': 2.2},
        'Sweden': {'lat': 60.1, 'lon': 18.6},
        'Finland': {'lat': 61.9, 'lon': 25.7},
        'Russia': {'lat': 61.5, 'lon': 105.3},
        'Poland': {'lat': 51.9, 'lon': 19.1},
        'Spain': {'lat': 40.5, 'lon': -3.7},
        'Canada': {'lat': 56.1, 'lon': -106.3},
        'Netherlands': {'lat': 52.1, 'lon': 5.3},
        'Australia': {'lat': -25.3, 'lon': 133.8},
        'Japan': {'lat': 36.2, 'lon': 138.3},
        'Argentina': {'lat': -38.4, 'lon': -63.6},
        'Mexico': {'lat': 23.6, 'lon': -102.6},
        'Norway': {'lat': 60.5, 'lon': 8.5},
        'Greece': {'lat': 39.1, 'lon': 21.8},
        'Chile': {'lat': -35.7, 'lon': -71.5},
        'Austria': {'lat': 47.5, 'lon': 14.6},
        'Belgium': {'lat': 50.5, 'lon': 4.5},
        'Czech Republic': {'lat': 49.8, 'lon': 15.5},
        'Portugal': {'lat': 39.4, 'lon': -8.2},
        'Ukraine': {'lat': 48.4, 'lon': 31.2},
        'Denmark': {'lat': 56.3, 'lon': 9.5},
        'Switzerland': {'lat': 46.8, 'lon': 8.2},
        'Colombia': {'lat': 4.6, 'lon': -74.3},
        'Indonesia': {'lat': -0.8, 'lon': 113.9},
        'Hungary': {'lat': 47.2, 'lon': 19.5}
    }
    
    for country in top_countries_data:
        name = country['Country']
        if name in country_coords:
            country['lat'] = country_coords[name]['lat']
            country['lon'] = country_coords[name]['lon']
        else:
            country['lat'] = None
            country['lon'] = None
    
    top_15_countries = country_stats.head(15).index.tolist()
    genre_country_matrix = df[df['Country'].isin(top_15_countries)].groupby(
        ['Country', 'Genre_Category']
    ).size().unstack(fill_value=0)
    genre_country_pct = genre_country_matrix.div(genre_country_matrix.sum(axis=1), axis=0) * 100
    genre_country_data = genre_country_pct.round(1).to_dict('index')
    dashboard_data = {
        'summary': {
            'total_bands': int(len(df)),
            'total_countries': int(df['Country'].nunique()),
            'total_genres': int(df['Genre_Category'].nunique()),
            'top_country': country_stats.index[0],
            'top_genre': global_genres.index[0]
        },
        'countries': top_countries_data,
        'genres': genre_data,
        'regions': region_data,
        'genre_by_country': genre_country_data
    }
    
    with open('dashboard_data.json', 'w') as f:
        json.dump(dashboard_data, f, indent=2)
    
    print("Exported dashboard_data.json")
    return dashboard_data

def analyze_spotify_data():
    spotify = pd.read_csv('data/heavy_bands_spotify.csv')
    print(f"Spotify data: {len(spotify)} heavy bands analyzed")
    artist_stats = spotify.sort_values('Popularity', ascending=False)
    top_artists_data = artist_stats.head(25).to_dict('records')
    
    top_tracks_data = []
    top_bands = artist_stats.head(10)
    for _, row in top_bands.iterrows():
        top_tracks_data.append({
            'Track': f"Top Track",
            'Artist': row['Artist'],
            'Album': row['Subgenre'],
            'Year': 2024,
            'Popularity': row['Popularity'],
            'Monthly_Listeners': row['Monthly_Listeners'],
            'Genre': row['Genre']
        })
    genre_stats = spotify.groupby('Genre').agg({
        'Popularity': 'mean',
        'Artist': 'count',
        'Monthly_Listeners': 'sum'
    }).rename(columns={'Artist': 'Band_Count'}).round(1)
    
    spotify['Popularity_Tier'] = pd.cut(
        spotify['Popularity'], 
        bins=[0, 45, 55, 65, 100], 
        labels=['Underground', 'Cult', 'Mainstream', 'Top Tier']
    )
    tier_stats = spotify.groupby('Popularity_Tier', observed=True).agg({
        'Monthly_Listeners': 'mean'
    }).round(0)
    tier_data = [{'Popularity_Tier': str(idx), 'Avg_Listeners': int(row['Monthly_Listeners'])} 
                 for idx, row in tier_stats.iterrows()]
    
    return {
        'top_artists': top_artists_data,
        'top_tracks': top_tracks_data,
        'tier_stats': tier_data,
        'genre_breakdown': genre_stats.reset_index().to_dict('records'),
        'total_tracks': len(spotify),
        'total_artists': len(spotify)
    }


def export_enhanced_dashboard(df, country_stats, region_stats, spotify_data):
    top_countries = country_stats.head(30).reset_index()
    top_countries_data = top_countries.to_dict('records')
    global_genres = df['Genre_Category'].value_counts()
    genre_data = [{'genre': k, 'count': int(v)} for k, v in global_genres.items()]
    region_data = region_stats.to_dict('records')
    country_coords = {
        'United States': {'lat': 39.8, 'lon': -98.5},
        'Germany': {'lat': 51.2, 'lon': 10.4},
        'Brazil': {'lat': -14.2, 'lon': -51.9},
        'Italy': {'lat': 41.9, 'lon': 12.6},
        'United Kingdom': {'lat': 55.4, 'lon': -3.4},
        'France': {'lat': 46.2, 'lon': 2.2},
        'Sweden': {'lat': 60.1, 'lon': 18.6},
        'Finland': {'lat': 61.9, 'lon': 25.7},
        'Russia': {'lat': 61.5, 'lon': 105.3},
        'Poland': {'lat': 51.9, 'lon': 19.1},
        'Spain': {'lat': 40.5, 'lon': -3.7},
        'Canada': {'lat': 56.1, 'lon': -106.3},
        'Netherlands': {'lat': 52.1, 'lon': 5.3},
        'Australia': {'lat': -25.3, 'lon': 133.8},
        'Japan': {'lat': 36.2, 'lon': 138.3},
        'Argentina': {'lat': -38.4, 'lon': -63.6},
        'Mexico': {'lat': 23.6, 'lon': -102.6},
        'Norway': {'lat': 60.5, 'lon': 8.5},
        'Greece': {'lat': 39.1, 'lon': 21.8},
        'Chile': {'lat': -35.7, 'lon': -71.5},
        'Austria': {'lat': 47.5, 'lon': 14.6},
        'Belgium': {'lat': 50.5, 'lon': 4.5},
        'Czech Republic': {'lat': 49.8, 'lon': 15.5},
        'Portugal': {'lat': 39.4, 'lon': -8.2},
        'Ukraine': {'lat': 48.4, 'lon': 31.2},
        'Denmark': {'lat': 56.3, 'lon': 9.5},
        'Switzerland': {'lat': 46.8, 'lon': 8.2},
        'Colombia': {'lat': 4.6, 'lon': -74.3},
        'Indonesia': {'lat': -0.8, 'lon': 113.9},
        'Hungary': {'lat': 47.2, 'lon': 19.5}
    }
    
    for country in top_countries_data:
        name = country['Country']
        if name in country_coords:
            country['lat'] = country_coords[name]['lat']
            country['lon'] = country_coords[name]['lon']
        else:
            country['lat'] = None
            country['lon'] = None
    
    top_15_countries = country_stats.head(15).index.tolist()
    genre_country_matrix = df[df['Country'].isin(top_15_countries)].groupby(
        ['Country', 'Genre_Category']
    ).size().unstack(fill_value=0)
    genre_country_pct = genre_country_matrix.div(genre_country_matrix.sum(axis=1), axis=0) * 100
    genre_country_data = genre_country_pct.round(1).to_dict('index')
    
    dashboard_data = {
        'summary': {
            'total_bands': int(len(df)),
            'total_countries': int(df['Country'].nunique()),
            'total_genres': int(df['Genre_Category'].nunique()),
            'top_country': country_stats.index[0],
            'top_genre': global_genres.index[0]
        },
        'countries': top_countries_data,
        'genres': genre_data,
        'regions': region_data,
        'genre_by_country': genre_country_data,
        'spotify': spotify_data
    }
    with open('dashboard_data.json', 'w') as f:
        json.dump(dashboard_data, f, indent=2)
    print("Exported dashboard_data.json (with Spotify data)")
    return dashboard_data

if __name__ == '__main__':
    print("=" * 60)
    print("METAL ON THE ROAD: Global Metal Band Analysis")
    print("=" * 60)
    print()
    df = load_and_clean_data()
    print()
    print("Loading discography data...")
    disco_df = pd.read_csv('data/all_bands_discography.csv', encoding='utf-8')
    print(f"Discography: {len(disco_df):,} album entries")
    print()
    print("-" * 40)
    print("TOP 15 COUNTRIES BY METAL BANDS")
    print("-" * 40)
    country_stats = analyze_by_country(df)
    print(country_stats.head(15).to_string())
    print()
    print("-" * 40)
    print("GENRE PREFERENCES BY REGION")
    print("-" * 40)
    region_stats = analyze_genre_by_region(df)
    print(region_stats.to_string(index=False))
    print()
    print("-" * 40)
    print("GLOBAL GENRE DISTRIBUTION")
    print("-" * 40)
    genre_counts = df['Genre_Category'].value_counts()
    for genre, count in genre_counts.items():
        pct = count / len(df) * 100
        print(f"{genre:20} {count:>8,} ({pct:>5.1f}%)")
    print()
    print("-" * 40)
    print("BAND STATUS (Top 10 Countries)")
    print("-" * 40)
    status_stats = analyze_status_distribution(df)
    print(status_stats.head(10)[['Active', 'Split-up', 'Active_Rate']].to_string())
    print()
    print("-" * 40)
    print("SPOTIFY POPULARITY ANALYSIS")
    print("-" * 40)
    spotify_data = analyze_spotify_data()
    print()
    print("TOP 10 MOST POPULAR METAL ARTISTS:")
    for i, artist in enumerate(spotify_data['top_artists'][:10], 1):
        print(f"{i:2}. {artist['Artist']:30} Popularity: {artist['Popularity']:.0f}")
    print()
    print("-" * 40)
    print("EXPORTING DATA FOR DASHBOARD")
    print("-" * 40)
    dashboard_data = export_enhanced_dashboard(df, country_stats, region_stats, spotify_data)
    
    print()
    print("=" * 60)
    print("Analysis complete!")
    print(f"Summary: {dashboard_data['summary']}")
    print(f"Spotify: {spotify_data['total_artists']} artists, {spotify_data['total_tracks']} tracks")
    print("=" * 60)
