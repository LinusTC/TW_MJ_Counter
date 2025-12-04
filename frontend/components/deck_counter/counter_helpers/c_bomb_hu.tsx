import { explode_hu_value } from "@/constants/values";
import { BombHuResult } from "@/types/counter";

export function c_bomb_hu(valid: boolean): BombHuResult {
  if (!valid) {
    return {
      value: -explode_hu_value * 3,
      log: `炸胡， 每家賠-${explode_hu_value}`,
      isBombHu: true,
    };
  }

  return {
    value: 0,
    log: null,
    isBombHu: false,
  };
}
