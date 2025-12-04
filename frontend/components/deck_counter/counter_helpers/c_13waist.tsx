import { ValidatedDeck, CounterResult } from "@/types/counter";
import { thirteen_waist_hu } from "@/constants/dictionary";
import { thirteen_waist_value } from "@/constants/values";

export function c_13waist(
  curr_validated_tiles: ValidatedDeck,
  door_clear: boolean
): CounterResult {
  if (curr_validated_tiles.hu_type === thirteen_waist_hu && door_clear) {
    return {
      value: thirteen_waist_value,
      log: `13么/腰 +${thirteen_waist_value}`,
    };
  }

  return {
    value: 0,
    log: null,
  };
}
