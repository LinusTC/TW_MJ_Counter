import { BaseCounter } from "./components/deck_counter/base_counter";
import { DeckValidator } from "./components/deck_validator/deck_validator";
import { TileCount } from "./types/counter";

const standardHand: TileCount = {
  f1: 1,
  ff1: 1,
  f2: 1,
  ff2: 1,
  f3: 1,
  ff3: 1,
  f4: 1,
  ff4: 1,
  south: 4,
  m1: 2,
  m9: 4,
  north: 4,
  east: 4,
  west: 4,
};

const deck_validator_test = new DeckValidator(standardHand);
const is_valid_test = deck_validator_test.fullCheck();
console.log("Valid:", is_valid_test);
console.log(
  "Number of possible decks:",
  deck_validator_test.possibleDecks.length
);
for (let i = 0; i < deck_validator_test.possibleDecks.length; i++) {
  console.log("\nDeck ${i + 1}:");
  console.log(deck_validator_test.possibleDecks[i]);
}

const winner_seat = 1;
const current_wind = 'west';
const myself_mo = true;
const door_clear = true;
const winning_tile = Object.keys(standardHand)[0];
const base_value = 0;
const multiplier = 1;

const base_counter = new BaseCounter(standardHand, winner_seat, current_wind, winning_tile, myself_mo, door_clear, base_value, multiplier);

const count_results = base_counter.base_count()
const value = count_results.value
const logs = count_results.log
const winning_deck = count_results.winning_deck
const winning_deck_organized = count_results.winning_deck_organized

console.log(`Value: ${value}`)
console.log(`Logs: ${logs}`)
console.log(`Winning deck: ${winning_deck}`)
console.log(`Winning deck_organized: ${winning_deck_organized}`)