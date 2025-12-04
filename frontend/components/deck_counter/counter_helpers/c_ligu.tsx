import { ValidatedDeck, CounterResult } from "@/types/counter";
import { ligu_hu } from "@/constants/dictionary";
import { li_gu_value } from "@/constants/values";

export function c_ligu(
  curr_validated_tiles: ValidatedDeck,
  door_clear: boolean
): CounterResult {
  if (curr_validated_tiles.hu_type === ligu_hu && door_clear) {
    return {
      value: li_gu_value,
      log: `Ligu +${li_gu_value}`,
    };
  }

  return {
    value: 0,
    log: null,
  };
}
