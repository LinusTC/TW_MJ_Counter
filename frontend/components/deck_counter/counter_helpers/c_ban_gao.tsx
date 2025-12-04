import { ValidatedDeck, CounterResult } from "@/types/counter";
import {
  ban_gao_value,
  two_ban_gao_value,
  three_ban_gao_value,
} from "@/constants/values";

export function c_ban_gao(curr_validated_tiles: ValidatedDeck): CounterResult {
  let total_value = 0;
  const log: string[] = [];
  const tested_sets: Record<string, number> = {};

  if (curr_validated_tiles.tiles) {
    for (const item of curr_validated_tiles.tiles) {
      const tiles = Array.isArray(item) ? item : [item];
      if (tiles.length === 3) {
        const hashed = [...tiles].sort().join(",");
        tested_sets[hashed] = (tested_sets[hashed] || 0) + 1;
      }
    }
  }

  for (const count of Object.values(tested_sets)) {
    if (count === 2) {
      total_value += ban_gao_value;
      log.push(`般高 +${ban_gao_value}`);
    } else if (count === 3) {
      total_value += two_ban_gao_value;
      log.push(`兩般高 +${two_ban_gao_value}`);
    } else if (count === 4) {
      total_value += three_ban_gao_value;
      log.push(`三般高 +${three_ban_gao_value}`);
    }
  }

  return {
    value: total_value,
    log: log.length > 0 ? log : null,
  };
}
