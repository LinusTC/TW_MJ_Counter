import { ValidatedDeck, CounterResult } from "@/types/counter";
import { MST_DICT, ZFB_DICT, WIND_DICT } from "@/constants/dictionary";
import { checkIsSpecialHu } from "@/utils/helpers";
import { five_door_value } from "@/constants/values";

export function c_5_doors(curr_validated_tiles: ValidatedDeck): CounterResult {
  const is_special_hu = checkIsSpecialHu(curr_validated_tiles);
  if (is_special_hu) {
    return {
      value: 0,
      log: null,
    };
  }

  const doors = new Set<string>();
  if (curr_validated_tiles.tiles) {
    for (const item of curr_validated_tiles.tiles) {
      const tiles = Array.isArray(item) ? item : [item];
      if (tiles[0] in MST_DICT) {
        const suit = tiles[0][0];
        doors.add(suit);
      }
      if (ZFB_DICT.has(tiles[0])) {
        doors.add("zfb");
      }
      if (WIND_DICT.has(tiles[0])) {
        doors.add("wind");
      }
    }
  }

  if (doors.size === 5) {
    return {
      value: five_door_value,
      log: `五門齊 +${five_door_value}`,
    };
  }

  return {
    value: 0,
    log: null,
  };
}
