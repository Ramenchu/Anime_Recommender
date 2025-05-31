import random
from tree_node import TreeNode
import csv
from csv_maker import create_csv
from csv_maker import get_anime_by_genre
from csv_maker import get_anime_genres

#set up root for data tree
#anime_tree = TreeNode('Anime Tree')
root = TreeNode("Anime by Genre")

#comparison method for strings for quicksort
#def text_comparison(text_a, text_b):
  #if node_a.name.lower() > node_b.name.lower():
        #return True
  #else:
        #return False
  
#comparison method for lists of nodes based on node values for quicksort
def string_node_comparison(node_a, node_b):
    if node_a.name.lower() > node_b.name.lower():
        return True
    else:
        return False

#quicksort implementation
def quicksort(list, start, end, comparison_function):
  if start >= end:
    return
  pivot_idx = random.randrange(start, end + 1)
  pivot_element = list[pivot_idx]
  list[end], list[pivot_idx] = list[pivot_idx], list[end]
  less_than_pointer = start
  for i in range(start, end):
    if comparison_function(pivot_element, list[i]):
      list[i], list[less_than_pointer] = list[less_than_pointer], list[i]
      less_than_pointer += 1
  list[end], list[less_than_pointer] = list[less_than_pointer], list[end]
  quicksort(list, start, less_than_pointer - 1, comparison_function)
  quicksort(list, less_than_pointer + 1, end, comparison_function)

#function to read csv data into a data tree structure
def new_tree_builder(file_path, root, quicksort):
    """
    Build a tree structure from the anime_by_genre.csv file and add it to the root node.

    Args:
        file_path (str): The path to the CSV file.
        root (TreeNode): The root node of the tree.
        quicksort (function): The quicksort function to sort genre nodes.
    """
    # Open and read the CSV file
    with open(file_path, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        genre_nodes = {}  # Dictionary to store genre nodes

        # Iterate through each row in the CSV
        for row in reader:
            genre = row["Genre"]
            anime = row["Anime"]
            score = row["Score"]
            episodes = row["Eps"]
            link = row["Link"]

            # Check if the genre node already exists
            if genre not in genre_nodes:
                # Create a new genre node
                genre_node = TreeNode(genre)
                genre_nodes[genre] = genre_node

            # Create an anime node with additional data
            anime_node = TreeNode(anime, data={"score": score, "episodes": episodes, "link": link})

            # Add the anime node as a child of the genre node
            genre_nodes[genre].add_child(anime_node)

        # Sort the genre nodes using the quicksort function
        #sorted_genres = quicksort(list(genre_nodes.values()), key=lambda node: node.name)

        # Convert genre_nodes to a list of TreeNode objects
        genre_list = list(genre_nodes.values())

        # Sort the genre nodes using the quicksort function
        quicksort(genre_list, 0, len(genre_list) - 1, string_node_comparison)

        # Add the sorted genre nodes to the root
        for genre_node in genre_list:
            root.add_child(genre_node)

        # Add the sorted genre nodes to the root
        #for genre_node in sorted_genres:
            #root.add_child(genre_node)

def print_animelist(genre_node):
    """
    Compile a list of anime in a genre, sort them using quicksort, and print the list.

    Args:
        genre_node (TreeNode): The genre node containing anime as its children.
    """
    if not genre_node.children:
        print(f"No anime found for genre: {genre_node.name}")
        return

    # Compile a list of anime nodes
    anime_list = genre_node.children

    # Sort the anime list using quicksort
    quicksort(anime_list, 0, len(anime_list) - 1, string_node_comparison)

    # Print the sorted list
    print(f"\nAnime List for Genre: {genre_node.name}")
    print(f"{'Title':<50} {'Score':<10} {'Episodes':<10} {'Link'}")
    print("-" * 80)

    for anime in anime_list:
        title = anime.name
        score = anime.data.get('score', 'N/A') if anime.data else 'N/A'
        episodes = anime.data.get('episodes', 'Unknown') if anime.data else 'Unknown'
        link = anime.data.get('link', 'N/A') if anime.data else 'N/A'
        print(f"{title:<50} {score:<10} {episodes:<10} {link}")

def genre_choice():
   
    selected_genre = None
    genre_list = [child.name for child in root.children]
    print("What genre of anime are you interested in?  Type in the start of the genre name to search.")
    while selected_genre is None:
       user_input = str(input("\n")).lower()
       matchlist = [genre for genre in genre_list if genre.lower().startswith(user_input)]

       if matchlist != []:
        print("\nThese genres match your search:")
        for match in matchlist:
            print(match)
       else:
        print("\nSorry, no genres match your search.  Try again.\n")
        return genre_choice()
        
       if len(matchlist) == 1:
            user_input = str(input(f"\nDo you want to see {matchlist[0]} anime recommendations? (y/n) ")).lower()
            if user_input == 'y':
                selected_genre = root.get_child_node(matchlist[0])
            else:
                print("\nSorry this wasn't what you were looking for.  Type in a new search to keep looking.")
       else:
            print("\nEnter more of the genre name to narrow down the search options, or start a new search for something else.\n")

    print_animelist(selected_genre)

    again = input("\nWould you like to check out some recommendations from other genres? (y/n)\n")
    if again == 'y':
       return genre_choice()

#say hi to the people:
def welcome():
  print("Welcome to my anime recommendation system!  Let's get started.\n")

#say goodbye to the people:
def goodbye():
  print("\nThank you for using my anime recommendation system!  Goodbye.")

#main function
def main():
  file_path = "anime_by_genre.csv"
  create_csv()  
  welcome()
  new_tree_builder(file_path, root, quicksort)
  genre_choice()
  goodbye()

main()
               