import { TileCount, ValidatedDeck, FlowerResult } from "@/types/counter";
import { FLOWER_DICT, flower_hu } from "@/constants/dictionary";
import {
  flower_value,
  flower_seat_value,
  seven_flower_value,
  eight_flower_value,
} from "@/constants/values";

export class FlowerCounter {
  private winner_seat: number;
  private winner_tiles: TileCount;
  private logs: string[];

  constructor(winner_seat: number, winner_tiles: TileCount) {
    this.winner_seat = winner_seat;
    this.winner_tiles = winner_tiles;
    this.logs = [];
  }

  countFlowerValue(): [number, boolean, boolean] {
    this.logs = []; // Reset logs for each count
    let value = 0;
    let has_flower = false;
    let counted_pos = false;

    for (const key in this.winner_tiles) {
      if (!(key in FLOWER_DICT)) {
        continue;
      } else {
        has_flower = true;
        value += flower_value;
        this.logs.push(`花${key} +${flower_value}`);

        if (FLOWER_DICT[key] === this.winner_seat) {
          value += flower_seat_value;
          counted_pos = true;
          this.logs.push(`花位${key} +${flower_seat_value}`);
        }
      }
    }

    if (value === 0) value += flower_value;

    return [value, has_flower, counted_pos];
  }

  getLogs(): string[] {
    return this.logs;
  }
}

export function c_flower(
  winner_seat: number,
  winner_tiles: TileCount,
  curr_validated_tiles: ValidatedDeck
): FlowerResult {
  const flowerCounter = new FlowerCounter(winner_seat, winner_tiles);
  const [flowerValue, has_flower, counted_pos] =
    flowerCounter.countFlowerValue();
  const has_flower_hu = curr_validated_tiles.hu_type === flower_hu;

  if (!has_flower) {
    return {
      value: flowerValue,
      log: `無花 +${flowerValue}`,
      hasFlowerHu: has_flower_hu,
      hasFlower: has_flower,
      countedPos: counted_pos,
    };
  }

  if (has_flower_hu) {
    const value =
      curr_validated_tiles.flowers?.length === 7
        ? seven_flower_value
        : eight_flower_value;
    return {
      value,
      log: `花胡 +${value}`,
      hasFlowerHu: has_flower_hu,
      hasFlower: has_flower,
      countedPos: counted_pos,
    };
  }

  if (has_flower) {
    return {
      value: flowerValue,
      log: flowerCounter.getLogs(),
      hasFlowerHu: has_flower_hu,
      hasFlower: has_flower,
      countedPos: counted_pos,
    };
  }

  return {
    value: 0,
    log: null,
    hasFlowerHu: false,
    hasFlower: false,
    countedPos: false,
  };
}
