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
    
    return {
        "filename": image.filename,
        "size": len(payload),
        "classified_decks": classified_decks,
    }

@twmj.post("/get-points")
async def get_points(winner_tiles: dict):
    
    deck_validator = DeckValidator(winner_tiles)
    deck_validator.full_check()

    full_counter = FullCounter(winner_tiles, 1, 1, None, True, True, 0, 1)
    count, logs, winning_deck, winning_deck_organized = full_counter.full_count()
    
    return {
        "count": count,
        "logs": logs,
        "winning_deck_organized": winning_deck_organized,
    }