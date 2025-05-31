import csv
import requests

base_url = "https://api.jikan.moe/v4/"

def get_anime_genres():
    url = f"{base_url}genres/anime?filter=genres"
    #url = f"{base_url}genres/anime"
    response = requests.get(url)
    if response.status_code == 200:
        #return response.json()
        #genres = response.json()
        #print(genres)
        #print("It worked!")
        return response.json().get('data', [])
    else:
        #print(f"Error: {response.status_code}")
        #return None
        print(f"Error fetching genres: {response.status_code}")
        return []


def get_anime_by_genre(genre_id):
    url = f"{base_url}anime?genres={genre_id}"
    response = requests.get(url)
    if response.status_code == 200:
        #return response.json()
        return response.json().get('data', [])
    else:
        #print(f"Error: {response.status_code}")
        #return None
        print(f"Error fetching anime for genre {genre_id}: {response.status_code}")
        return []


def create_csv():
    genres = get_anime_genres()
    if not genres:
        print("No genres found. Exiting.")
        return
    
    # Open a CSV file for writing
    with open("anime_by_genre.csv", mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        # Write the header row
        writer.writerow(["Genre", "Anime", "Score", "Eps", "Link"])

        # Fetch anime for each genre and write to the CSV
        for genre in sorted(genres, key=lambda g: g['name']):  # Sort genres by name
            genre_name = genre['name']
            genre_id = genre['mal_id']

            if genre_id == 28:
                continue

            #print(f"Fetching anime for genre: {genre_name}...")
            print(f"Loading anime database...")

            anime_list = get_anime_by_genre(genre_id)
            for anime in anime_list:
                title = anime.get('title', 'N/A')
                score = anime.get('score', 'N/A')
                episodes = anime.get('episodes')
                if not episodes:  # Check if episodes is None, 0, or an empty string
                    episodes = 'Unknown'
                link = anime.get('url', 'N/A')
                # Write a row for each anime
                writer.writerow([genre_name, title, score, episodes, link])

    #print("CSV file 'anime_by_genre.csv' created successfully.")

# Run the function to create the CSV
#create_csv()









'''genre_info = get_anime_genres()

if genre_info:
    for genre in genre_info['data']:
        genre_id = genre['mal_id']
        genre_name = genre['name']
        #print(f"Genre ID: {genre_id}, Genre Name: {genre_name}")
        print(f"Genre Name: {genre_name}, Genre ID: {genre_id}")

action_genre_id = 1
anime_info = get_anime_by_genre(action_genre_id)

if anime_info:
    print("Anime in the Action genre:")
    for anime in anime_info['data']:
        title = anime['title']
        link = anime['url']
        score = anime['score']
        eps = anime['episodes']
        print(f"Title: {title}, Link: {link}, Score: {score}, Episodes: {eps}")
        #print(f"Title: {title}, Link: {link}")
        #print(anime.keys()) 
        #break'''


