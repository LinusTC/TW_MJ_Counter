from flower_counter import FlowerCounter
from fan_counter import FanCounter
class FullCounter:
    def __init__(self, winner_tiles, validated_tiles, winner_seat, current_wind):
        self.winner_tiles = winner_tiles
        self.validated_tiles = validated_tiles
        self.winner_seat = winner_seat
        self.current_wind = current_wind
        self.FlowerCounter = FlowerCounter(self.winner_seat, self.winner_tiles)
        self.FanCounter = FanCounter(self.winner_seat, self.winner_tiles, self.current_wind)
        self.logs = []