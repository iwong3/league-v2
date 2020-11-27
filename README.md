# league-v2

### VISUALIZATIONS IDEAS
- champions vs. avg win rate
- champions vs. avg win time
- items vs. avg win rate
- items vs. avg win time
- champions vs. avg types of damage dealt
- champiopns vs. time ccing others
- champions vs. wards placed
- champions vs. runes
- runes vs. avg win rate
- runes vs. avg win time
- first blood vs. avg win rate
- first turret vs. avg win rate
- champions vs. killing sprees
- champions vs. time alive
- scatterplot - dmg dealt vs. dmg taken, dots = green/red, win/loss

### ML IDEAS
- Win/loss (and time?) predictions based on kda/items/champs/runes
  - this is really cool, could apply to live games and see if predictions match outcome
- Predict champion being played based on kda/items/runes

### NEXT STEPS
- Load more data (100,000 rows for analysis?)
- Create backend endpoints to access db (probably can just get all data, can create queries based on functionality)
- Backend should map values to more meaningful context
- Create a basic visualization with d3
- Think about meaningful front end UI, functionality (instead of showing a bunch of graphs, maybe have sections/user choice)
  - User could filter by patch/champ/map

### IMMEDIATE NEXT STEPS
- all `__pycache__` to `.gitignore`
- update `/match` endpoint response to have meaningful values (mappings)
- set up basic d3 visualization
