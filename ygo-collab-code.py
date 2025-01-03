import requests
from IPython.display import display, HTML
from ipywidgets import Dropdown, Button, Output
from IPython.display import clear_output

# --- Helper Functions ---
def fetch_json_data(url):
    """Fetches JSON data from a given URL."""
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None
    except ValueError:
        print("Error: Invalid JSON response.")
        return None

def display_card_grid(cards):
    """Displays a list of cards in a grid format."""
    if not cards:
        print("No cards found for this set.")
        return

    card_grid_html = "<div style='display: flex; flex-wrap: wrap; gap: 10px;'>"
    for card in cards:
        if 'card_images' in card and card['card_images']:
            image_url = card['card_images'][0]['image_url_small']
            card_name = card['name']
            card_grid_html += f"""
                <div style='text-align: center; width: 120px;'>
                    <img src='{image_url}' alt='{card_name}' style='width: 100px; height: auto;'>
                    <p style='font-size: 0.8em; margin-top: 5px;'>{card_name}</p>
                </div>
            """
    card_grid_html += "</div>"
    display(HTML(card_grid_html))

# --- Main Logic ---
print("Fetching list of Yu-Gi-Oh! card sets...")
card_sets_url = "https://db.ygoprodeck.com/api/v7/cardsets.php"
card_sets_data = fetch_json_data(card_sets_url)

if card_sets_data:
    set_names = sorted([set_info['set_name'] for set_info in card_sets_data])

    dropdown = Dropdown(
        options=set_names,
        description='Select a Set:',
        disabled=False,
    )

    display(dropdown)

    button = Button(description="Show Cards")
    output = Output()

    def on_button_clicked(b):
        with output:
            clear_output()
            selected_set = dropdown.value
            print(f"Fetching cards from '{selected_set}'...")
            card_info_url = f"https://db.ygoprodeck.com/api/v7/cardinfo.php?cardset={selected_set}"
            card_data = fetch_json_data(card_info_url)
            if card_data and 'data' in card_data:
                display_card_grid(card_data['data'])
            else:
                print(f"Could not retrieve card information for '{selected_set}'.")

    button.on_click(on_button_clicked)
    display(button, output)

else:
    print("Failed to fetch the list of card sets. Please check your internet connection.")