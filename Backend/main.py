from dictionary import *
from deck_validator import DeckValidator
from full_counter import FullCounter
from tile_classifier import TileClassifier
import tkinter as tk
from tkinter import filedialog
import os

if __name__ == "__main__":
    # Create a hidden root window for the file dialog
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    
    # Open file dialog to select image
    print("請選擇麻將牌圖片 / Please select mahjong tiles image...")
    image_path = filedialog.askopenfilename(
        title="選擇麻將牌圖片 / Select Mahjong Tiles Image",
        filetypes=[
            ("Image files", "*.jpg *.jpeg *.png *.bmp *.heic"),
            ("JPEG files", "*.jpg *.jpeg"),
            ("HEIC files", "*.heic *.heic"),
            ("PNG files", "*.png"),
            ("All files", "*.*")
        ]
    )
    
    # Check if user selected a file
    if not image_path:
        print("未選擇圖片，程式結束 / No image selected, exiting...")
        exit()
    
    print(f"已選擇: {image_path}")
    
    # Use the selected image
    tile_classifier = TileClassifier(image_path)
    tile_classifier.classify()
    winner_tiles = tile_classifier.get_classified_decks()
    
    print("\n" + "="*60)
    print("處理中... / Processing...")
    print("="*60 + "\n")
    
    for set_of_tiles in winner_tiles:
        deck_validator = DeckValidator(set_of_tiles)

        if deck_validator.full_check():
            print("\n" + "="*60)
            print("台灣麻將計番器 - Taiwan Mahjong Counter")
            print("="*60)
            
            # Winner seat (1-4)
            while True:
                try:
                    winner_seat = int(input("\n贏家座位 (1-4) / Winner seat (1-4): "))
                    if 1 <= winner_seat <= 4:
                        break
                    print("請輸入 1-4 之間的數字 / Please enter a number between 1-4")
                except ValueError:
                    print("請輸入有效的數字 / Please enter a valid number")
            
            # Current wind
            print("\n當前風圈 / Current wind:")
            print("1. 東風 (East)")
            print("2. 南風 (South)")
            print("3. 西風 (West)")
            print("4. 北風 (North)")
            while True:
                try:
                    wind_choice = int(input("選擇風圈 (1-4) / Choose wind (1-4): "))
                    wind_map = {1: 'east', 2: 'south', 3: 'west', 4: 'north'}
                    if wind_choice in wind_map:
                        current_wind = wind_map[wind_choice]
                        break
                    print("請輸入 1-4 之間的數字 / Please enter a number between 1-4")
                except ValueError:
                    print("請輸入有效的數字 / Please enter a valid number")
            
            # Self-draw (自摸)
            while True:
                mo_input = input("\n自摸? (y/n) / Self-draw? (y/n): ").lower()
                if mo_input in ['y', 'n', 'yes', 'no']:
                    mo_myself = mo_input in ['y', 'yes']
                    break
                print("請輸入 y 或 n / Please enter y or n")
            
            # Door clear (門清)
            while True:
                door_input = input("門清? (y/n) / Door clear (no exposed sets)? (y/n): ").lower()
                if door_input in ['y', 'n', 'yes', 'no']:
                    door_clear = door_input in ['y', 'yes']
                    break
                print("請輸入 y 或 n / Please enter y or n")

            # 胡牌底 (Base score)
            while True:
                try:
                    base_score = int(input("\n胡牌底 / Base score: "))
                    break
                except ValueError:
                    print("請輸入有效的數字 / Please enter a valid number")
            
            # 胡牌乘數 (Multiplier)
            while True:
                try:
                    multiplier = int(input("胡牌乘數 / Score multiplier: "))
                    break
                except ValueError:
                    print("請輸入有效的數字 / Please enter a valid number")
            
            # Winning tile (optional)
            winning_tile = input("\n胡牌 (可選，按Enter跳過) / Winning tile (optional, press Enter to skip): ").strip() or None
            
            validated_decks = deck_validator.get_validated_decks()
            full_counter = FullCounter(set_of_tiles, winner_seat, current_wind, winning_tile, mo_myself, door_clear, base_score, multiplier)
            count, logs, winning_deck, winning_deck_organized = full_counter.full_count()
            
            print("\n" + "="*60)
            print("結果 / Results")
            print("="*60)
            print(f"\n牌組 / Tiles: {set_of_tiles}")
            print(f"總分 / Total Score: {count}")
            print(f"計分明細 / Score Breakdown: {logs}")
            print(f"勝利牌組 / Winning Deck: {winning_deck_organized}")
            print("="*60)
        else:
            print(f"\n無效的牌組 / Invalid deck: {set_of_tiles}")