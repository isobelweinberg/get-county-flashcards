import genanki
import argparse
import os

# Get image files from the data folder
parser = argparse.ArgumentParser(description="Create flashcard deck from saved images")
parser.add_argument(
    "--image-folder",
    type=str,
    default="data",
    help="Folder containing image files (default: data)"
)
parser.add_argument(
    "--output-file",
    type=str,
    default="county_deck2.apkg",
    help="Name of the output file for the Anki deck (default: data/county_deck.apkg)"
)
args = parser.parse_args()
img_folder = args.image_folder
img_files = [f for f in os.listdir(img_folder) if f.endswith(".jpg")]
output_file = args.output_file

# Hardcode unique IDs for the model and deck
MODEL_ID = 1615543476 # python -c "import random; print(random.randrange(1 << 30, 1 << 31))" 
DECK_ID = 1919294516

# Create the model for the flashcards
county_model = genanki.Model(
    MODEL_ID,
    "County Flashcard Notes",
    fields=[
        {"name": "Image"},
        {"name": "Name"},
    ],
    templates=[
        {
            "name": "Image to Name",
            "qfmt": '{{Image}}',
            "afmt": '{{FrontSide}}<hr id="answer">{{Name}}',
        },
    ],
)

# Create the deck
county_deck = genanki.Deck(
    DECK_ID,
    "English Counties",
)

# # Add flashcards to the deck
counties = [(f, f.removesuffix(".jpg").replace("_", " ")) for f in img_files]
# print(counties)

# Add cards and images to the deck
for image_file, county_name in counties:
    card = genanki.Note(
        model=county_model,
        fields=['<img src="' + image_file + '">', county_name],
    )
    county_deck.add_note(card)

# Create package
package = genanki.Package(county_deck)
print([os.path.abspath(os.path.join(img_folder, img)) for img in img_files])
package.media_files = [os.path.abspath(os.path.join(img_folder, img)) for img in img_files]

# Save package
package.write_to_file(output_file)

print(f"Anki deck created: {output_file}")
