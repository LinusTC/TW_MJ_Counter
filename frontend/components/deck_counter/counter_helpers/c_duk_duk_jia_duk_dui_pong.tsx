import { ValidatedDeck, CounterResult } from "@/types/counter";
import { checkIsSpecialHu, findTilesThatCompleteSet } from "@/utils/helpers";
import {
  real_solo_value,
  fake_solo_value,
  double_pong_value,
} from "@/constants/values";
import { SHANG_DICT, EYES_DICT, PONG_DICT } from "@/constants/dictionary";

export function c_duk_duk_jia_duk_dui_pong(
  winning_tile: string | null,
  curr_validated_tiles: ValidatedDeck
): CounterResult {
  if (!winning_tile) {
    return { value: 0, log: null };
  }

  const is_special_hu = checkIsSpecialHu(curr_validated_tiles);
  if (is_special_hu) {
    return { value: 0, log: null };
  }

  const groups_with_winning_tile: Map<string, string[]> = new Map();

  if (curr_validated_tiles.tiles) {
    for (const item of curr_validated_tiles.tiles) {
      const tiles = Array.isArray(item) ? item : [item];
      if (tiles.includes(winning_tile)) {
        const remaining_tiles = [...tiles];
        const index = remaining_tiles.indexOf(winning_tile);
        remaining_tiles.splice(index, 1);
        groups_with_winning_tile.set(JSON.stringify(tiles), remaining_tiles);
      }
    }
  }

  const possible_tiles_list = Array.from(groups_with_winning_tile.values()).map(
    (incomplete_group) => findTilesThatCompleteSet(incomplete_group)
  );

  if (groups_with_winning_tile.size === 1) {
    const possible_tiles = possible_tiles_list[0];
    if (
      possible_tiles &&
      possible_tiles.tiles &&
      possible_tiles.complete_type &&
      possible_tiles.tiles.length === 1 &&
      (possible_tiles.complete_type === SHANG_DICT ||
        possible_tiles.complete_type === EYES_DICT)
    ) {
      return {
        value: real_solo_value,
        log: `獨獨 +${real_solo_value}`,
      };
    }
  }

  if (groups_with_winning_tile.size > 1) {
    for (const item of possible_tiles_list) {
      if (!item || !item.tiles || !item.complete_type) {
        continue;
      }
      if (
        (item.complete_type === SHANG_DICT ||
          item.complete_type === EYES_DICT) &&
        item.tiles.length === 1
      ) {
        return {
          value: fake_solo_value,
          log: `假獨 +${fake_solo_value}`,
        };
      }
    }
  }

  for (const item of possible_tiles_list) {
    if (!item || !item.complete_type) {
      continue;
    }
    if (item.complete_type === PONG_DICT) {
      return {
        value: double_pong_value,
        log: `對碰 +${double_pong_value}`,
      };
    }
  }

  return { value: 0, log: null };
}
