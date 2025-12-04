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
