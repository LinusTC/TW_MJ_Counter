import { ValidatedDeck, CounterResult } from "@/types/counter";
import { ZFB_DICT, WIND_DICT } from "@/constants/dictionary";
import { only_fan_value } from "@/constants/values";

export function c_only_fan(curr_validated_tiles: ValidatedDeck): CounterResult {
  if (curr_validated_tiles.tiles) {
    for (const item of curr_validated_tiles.tiles) {
      const tile_group = Array.isArray(item) ? item : [item];
      for (const tile of tile_group) {
        if (!ZFB_DICT.has(tile) && !WIND_DICT.has(tile)) {
          return {
            value: 0,
            log: null,
          };
        }
      }
    }
  }

  return {
    value: only_fan_value,
    log: `全番子 +${only_fan_value}`,
  };
}
