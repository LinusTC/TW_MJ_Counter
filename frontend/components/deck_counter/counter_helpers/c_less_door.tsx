import { ValidatedDeck, CounterResult } from "@/types/counter";
import { checkIsSpecialHu } from "@/utils/mj_helpers";
import { less_one_door_value } from "@/constants/values";

export function c_less_door(
    curr_validated_tiles: ValidatedDeck,
    has_fan: boolean
): CounterResult {
    const is_special_hu = checkIsSpecialHu(curr_validated_tiles);
    if (is_special_hu) {
        return {
            value: 0,
            log: null,
        };
    }

    if (has_fan) {
        return {
            value: 0,
            log: null,
        };
    }

    const doors = new Set<string>();
    if (curr_validated_tiles.tiles) {
        for (const item of curr_validated_tiles.tiles) {
            const tiles = Array.isArray(item) ? item : [item];

            if (tiles.length > 2) {
                doors.add(tiles[0][0]);
            }
        }
    }

    if (doors.size > 2) {
        return {
            value: 0,
            log: null,
        };
    }

    return {
        value: less_one_door_value,
        log: `缺一門 +${less_one_door_value}`,
    };
}
