import { ValidatedDeck, CounterResult } from "@/types/counter";
import { ZFB_DICT, WIND_DICT, MST_DICT } from "@/constants/dictionary";
import { sister_value, three_sister_value } from "@/constants/values";

export function c_sister(curr_validated_tiles: ValidatedDeck): CounterResult {
  let total_value = 0;
  const log: string[] = [];
  const sisters: Record<string, Set<string>> = {};

  if (curr_validated_tiles.tiles) {
    for (const item of curr_validated_tiles.tiles) {
      const tiles = Array.isArray(item) ? item : [item];
      if (
        tiles.length === 3 &&
        !ZFB_DICT.has(tiles[0]) &&
        !WIND_DICT.has(tiles[0])
      ) {
        const numbers = new Set<number>();
        const suit = tiles[0][0];

        for (const tile of tiles) {
          const tile_number = MST_DICT[tile];
          numbers.add(tile_number);
        }

        if (numbers.size > 1) {
          const hashed = Array.from(numbers)
            .sort((a, b) => a - b)
            .join(",");
          if (!sisters[hashed]) {
            sisters[hashed] = new Set<string>();
          }
          sisters[hashed].add(suit);
        }
      }
    }
  }

  for (const [item, value] of Object.entries(sisters)) {
    if (value.size === 3) {
      total_value += three_sister_value;
      log.push(`三姐妹/三相逢 +${three_sister_value}`);
    } else if (value.size === 2) {
      total_value += sister_value;
      log.push(`姐妹/二相逢 +${sister_value}`);
    }
  }

  return {
    value: total_value,
    log: log.length > 0 ? log : null,
  };
}
