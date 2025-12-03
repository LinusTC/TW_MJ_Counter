from fastapi import FastAPI, File, UploadFile
from tile_classifier import TileClassifier
from deck_validator import DeckValidator
from full_counter import FullCounter
from PIL import Image
from io import BytesIO
from pillow_heif import register_heif_opener

register_heif_opener()
twmj = FastAPI()

@twmj.get("/")
def root():
    return('hello world')

@twmj.post("/classify-hand")
async def classify_hand(image: UploadFile = File(...)):
    
    payload = await image.read()
    pil_image = Image.open(BytesIO(payload))
    
    tile_classifier = TileClassifier(pil_image)
    tile_classifier.classify()
    classified_decks = tile_classifier.get_classified_decks()

    results = []
    for deck in classified_decks:
        deck_validator = DeckValidator(deck)
        deck_validator.full_check()

        full_counter = FullCounter(deck, 1, 1, None, True, True, 0, 1)
        count, logs, winning_deck, winning_deck_organized = full_counter.full_count()
        
        results.append({
            "count": count,
            "logs": logs,
            "winning_deck_organized": winning_deck_organized,
        })
    
    return {
        "filename": image.filename,
        "size": len(payload),
        "classified_decks": classified_decks,
        "results": results
    }