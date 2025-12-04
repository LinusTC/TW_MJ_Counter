import { ValidatedDeck, CounterResult } from "@/types/counter";
import { ZFB_DICT, WIND_DICT } from "@/constants/dictionary";
import {
  three_numbers_fan_value,
  three_numbers_no_fan_value,
  two_numbers_fan_value,
  two_numbers_no_fan_value,
} from "@/constants/values";

export function c_two_or_three_numbers_only(
  curr_validated_tiles: ValidatedDeck,
  has_fan: boolean
): CounterResult {
  const number_set = new Set<string>();

  if (curr_validated_tiles.tiles) {
    for (const item of curr_validated_tiles.tiles) {
      const tiles = Array.isArray(item) ? item : [item];
      for (const tile of tiles) {
        if (ZFB_DICT.has(tile) || WIND_DICT.has(tile)) {
          continue;
        }
        number_set.add(tile[1]);
      }
    }
  }

  if (number_set.size === 3 && has_fan) {
    return {
      value: three_numbers_fan_value,
      log: `三数 有番子 +${three_numbers_fan_value}`,
    };
  }

  if (number_set.size === 3 && !has_fan) {
    return {
      value: three_numbers_no_fan_value,
      log: `三数 無番子 +${three_numbers_no_fan_value}`,
    };
  }

  if (number_set.size === 2 && has_fan) {
    return {
      value: two_numbers_fan_value,
      log: `兩数 有番子 +${two_numbers_fan_value}`,
    };
  }

  if (number_set.size === 2 && !has_fan) {
    return {
      value: two_numbers_no_fan_value,
      log: `兩数 無番子 +${two_numbers_no_fan_value}`,
    };
  }

  return { value: 0, log: null };
}
