import { explode_hu_value } from "@/constants/values";
import { BombHuResult } from "@/types/counter";

export function c_bomb_hu(valid: boolean): BombHuResult {
  if (!valid) {
    return {
      value: -explode_hu_value * 3,
      log: `炸胡， 每家賠-${explode_hu_value}`,
      is_bomb_hu: true,
    };
  }

  return {
    value: 0,
    log: null,
    is_bomb_hu: false,
  };
}
