# README
## Scripting format
### Functions
- A string preceded by '#' is a function. 
- Functions should always be followed with parenthesis. Arguments inside the parenthesis should be seperated with a comma and a space
- When the instruction is executed, functions will be evaluated and replaced with the value they return. A command should not be run more than once
- There are three internal functions in cardParser.py:
  - $set(x, val): creates a variable named x with the value of val. Val can (and generally should) be a function
  - $get(x, val): returns the value in variable x
  - $cond(Condition(), Function()): runs Condition. If it return True, runs and returns Function
- set and get should not appear in the card text. When parsing a card command they are automatically inserted where needed
- All other functions are defined in cards.py

### Variables
- Variables are used to store a value and then use it in multiple function inputs
- Variables are assigned using commands of the format "\<varname>=#Function([args])"
- Variables in function arguments are preceded by $. This causes them to be read as a variable and not a value
- Variables in arguments are replaced by their value before the command is run

### Values
- A value not preceded by '$' will be read as a value. Often that will mean its cast to an int, but strings or bools are appropriate in some cases
- Bools have values 'T' or 'F' in function inputs. These are NOT the values return by functions, which are real, non-string True/False values

### Notes
- Multiple functions can be run in one card. They should be seperated by a semicolon and space
- Variable values will remain through all functions executed in one multicommand
- Simple example: village runs '$draw(1); $changeActions(2)'
   - This first executes a draw command and passes 1 as an argument, drawing a card. Then it calls changeActions to increase actions by 2
- More complicated example: cellar runs 'x=#chooseSubset(#getHand(), -1, T); #discard($x); #draw(#count($x))'
  - This asks the player to choose any number of cards in their hand, and assigns these cards to the variable x
  - It then discards the cards in x, and draws the number of cards in x
- Very complicated example:
- vassal runs '#changeCoins(2); x=#getFirst(#fromTop(1)); #discard($x); #cond(#eval(#getType($x), =, action), #cond(#getChoice("Play {}?", #getName($x)), #play($x)))'
- In order, this:
  - Increases coins by 2
  - sets the variable x to refer to the the first card from list of the top 1 cards of the deck, e.g. sets x to the top card of the deck
  - moves x to the discard pile
  - Checks if x is an action card.
  - If it is, asks the player "Play {name of x}?". If the player says yes, plays x.