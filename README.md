# Pokemon GO Data
 
Motivation
==========
My mother is an avid Pokemon GO player, with an account at Level 47 and a collection that consistently maxes out the backpack capacity. It's also given her an activity to do with her friends, since they were already going on walks together and this gave them an extra aspect to their routine. From a video game perspective, she has really mechanically gifted (used to be top 10 on the Fruit Ninja leaderboard while toying with opponents) and incredibly persistent. However, since playing Pokemon GO for her is both a hobby and a means of physical activity, she's never thought too much about optimizing her teams for either PvE or PvP play. She has found some online resources, including moveset grading and IV calculators, but she never really went into battles with a plan other than to tap and hope for the best. She also has the disadvantage of never having played the original Pokemon series of games, so her memorization of Pokemon types and strengths/resistances is her main blind spot for a game like Pokemon GO, which rewards avoiding losing type matchups and acknowledging that certain Pokemon, Pokemon movesets, and teams are just better in the meta than others.

Objectives
==========
Develop a dashboard or at least tools that would help me formulate a gameplan for her extensive Pokemon collection. Luckily, she has a few iterations of most meta-dominant Pokemon, which is crucial for developing a roadmap. However, she also hasn't optimized her individual Pokemon outside of leveling up high-IV (high stat) Pokemon, so very few of them have two charge moves. Restrictions include only one charge move and no XL pokemon (too difficult to farm up without spending lots of money).

Code - Scraping
==========
I needed to acquire data on numerous different aspects of the Pokemon GO experience.

* Pokemon - Names and Variants, Base stats (attack, defense, stamina), CP (Combat Power) calculations, Types (e.g., Fire, Water...)
* Move Combinations - Out of the list of fast moves and charge moves, each possible combination should be considered
* Moves - Type, Power, Energy charge/discharge, frequency (in terms of turns)
* Types - Multipliers

These came from various sources, including the following URLs.

https://gamepress.gg/pokemongo/pvp-fast-moves

https://gamepress.gg/pokemongo/pvp-charge-moves


Tableau
==========
[I used Tableau, Public version to generate an interesting display of the available movesets with only one charge move.](https://public.tableau.com/app/profile/roger3881/viz/PokemonGoAllPossibleMovesets/UltraLeague2500CP)

![image](https://user-images.githubusercontent.com/78449574/142749909-7ac69911-c714-477b-8c71-be8b50f27fc5.png)

DPS was calculated with a combination of Power, turns (0.5 seconds per turn in PvP), a Pokemon's attack, and an assumed opponent defense of 100. For Ultra League, these attack values were calculated from a 15/15/15 intermediate value (IV) pokemon at 2500 CP. Also, same type attack bonus (STAB) was accounted for, but other bonuses, including weather and buddy bonuses, were not included. Multipliers for/against a move were also not included.

Some interesting conclusions were determined.

* Given her available Pokemon, I suggested a team of Swampert (Mud Shot + Hydro Cannon) | Giratina Altered (Shadow Claw + Shadow Sneak) OR Cresselia (Confusion + Future Sight) | Venusaur (Razor Leaf + Sludge Bomb). I arrived at this team after consulting both DPS charts and [a self-made type chart](https://public.tableau.com/app/profile/roger3881/viz/PokemonTypeEffectivenessTable/Sheet1). Swampert's main weakness is to Grass, and Giratina can cover solidly for Swampert. However, Giratina struggles against a number of meta options, including Fairy-type moves (like Togekiss), Ice Pokemon (such as Lapras and Suicune), and Pokemon with Dark moves. Meanwhile, while Venusaur has some weaknesses to Fire/Flying/Ice/Psychic, this combination fo three Pokemon leads to a pretty easy roadmap for a fight.
* Current gameplan: Swampert comes out first. If the opposing Pokemon is grass, then a switch to Giratina is reasonable to force an opponent switch. It's unlikely the opponent has two grass Pokemon, so Giratina or Cresselia, should win that 1 on 1 matchup. That leaves Swampert available to take out the remaining Pokemon, with its solid type coverage.
* High IV Regice and Regirock with the fast move Lock On are now priority finds. 
* Also, I was able to advise on self-debuff moves and their potential. Raikou with Wild Charge, Ho-oh with Brave Bird, and others are intriguing for their ability to turn a losing situation into a winning one. Extended usage reduces their effectiveness, but they can quickly clean up the opposition with a strong leading charge attack, especially with a fast-charging fast move.
* Not related to the data, but I was also able to advise on reducing actions per minute (APM). Because an action only occurs every 0.5 second (at the fastest), she has been able to go from continuously tapping on the screen to tapping more conservatively.

![image](https://user-images.githubusercontent.com/78449574/142749886-4b638a77-a9dc-46d3-9a8a-09e60f7ed7b1.png)


Future Improvements
==========
* Mark buffing/debuffing moves on the Tableau graph.
* Randomized teams of 3 fighting each other, and the winningest combinations have a weighted-chance of reappearing.
