# league-v2

### VISUALIZATIONS IDEAS
- champions vs. avg win rate
- champions vs. avg win time
- items vs. avg win rate
- items vs. avg win time
- champions vs. avg types of damage dealt
- champions vs. time ccing others
- champions vs. wards placed
- champions vs. runes
- runes vs. avg win rate
- runes vs. avg win time
- first blood vs. avg win rate
- first turret vs. avg win rate
- champions vs. killing sprees
- champions vs. time alive
- scatterplot - dmg dealt vs. dmg taken, dots = green/red, win/loss
- champions vs. kill participation
- team totals

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
- Think about data filtering for all graphs vs. per graph
    - Could allow filtering for all graphs, but also allow per-graph filtering
    - Dynamic graph titles/labels

### IMMEDIATE NEXT STEPS
- create MatchParticipantsScatterplot
- create same scatterplots for team/participants with deltas / means / other cool stats
- create nicer ui for above 2 graphs
    - look up design
    - league colors
    - axis selectors - use list for styling? https://codepen.io/marijoha/pen/zKjvEw
- graphs of deltas (winning teams had 'x' more cs/kda/etc)
    - calculate at backend?
- data issues
    - think of all the different interesting graphs to make and what data you'll need
    - fix db columns
    - fix scripts to populate db
    - run script to populate
    - fix backend endpoints if needed
    - TODO: champ bans fixed & team totals added - need to re-create table and run scripts ONCE data is more set
- think about website purpose & design
    - champion/win graphs
        - a lot of visualizations could be shown in 1 graph w/ user selecting x/y
    - champion page w/ champ stats
    - ML page (win/loss predictor, champ predictor)
    - maybe a homepage with scrollable cool data? then a header at the top to manually explore different features
        - most interesting findings on homepage in a cool, scrollable, presentable format
        - header w/ tabs for manually exploring (graphs, champ stats, ML)
