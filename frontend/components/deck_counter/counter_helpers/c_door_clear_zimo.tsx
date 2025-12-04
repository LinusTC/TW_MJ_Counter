import { ValidatedDeck, CounterResult } from "@/types/counter";
import { checkIsSpecialHu } from "@/utils/helpers";
import {
  door_clear_zimo_value,
  myself_mo_value,
  door_clear_value,
} from "@/constants/values";

export function c_door_clear_zimo(
  mo_myself: boolean,
  door_clear: boolean,
  curr_validated_tiles: ValidatedDeck
): CounterResult {
  const is_special_hu = checkIsSpecialHu(curr_validated_tiles);

  if (mo_myself && door_clear && !is_special_hu) {
    return {
      value: door_clear_zimo_value,
      log: `門清自摸 +${door_clear_zimo_value}`,
    };
  }

  if (mo_myself) {
    return {
      value: myself_mo_value,
      log: `自摸 +${myself_mo_value}`,
    };
  }

  if (door_clear && !is_special_hu) {
    return {
      value: door_clear_value,
      log: `門清 +${door_clear_value}`,
    };
  }

  return {
    value: 0,
    log: null,
  };
}
