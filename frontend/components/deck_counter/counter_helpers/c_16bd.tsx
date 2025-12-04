import { ValidatedDeck, CounterResult } from "@/types/counter"
import { sixteen_bd_hu } from "@/constants/dictionary"
import { sixteenbd_value } from "@/constants/values"

export function c_16bd(curr_validated_tiles: ValidatedDeck, door_clear: boolean): CounterResult {
    if (curr_validated_tiles.hu_type === sixteen_bd_hu && door_clear){
        return{
            value: sixteenbd_value,
            log: `16不搭 ${sixteenbd_value}`
        }

    }
    return {value: 0, log: null}
}