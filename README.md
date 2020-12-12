# league-v2

This app currently provides the following functionality:
    - scatterplots for in-game stats such as kda, damage taken/given, cs, vision score, etc.
        - at the team, team delta, participant levels
    - basic random forest classifier to predict champion based on in-game total stats (and per10 stats)

### NEXT STEPS
- graph ideas
    - participants scatterplot
    - participants per 10 scatterplot
- graph functionality
    - mean/mode/other cool stats
- graph ui
    - axis selectors - use list for styling? https://codepen.io/marijoha/pen/zKjvEw
    - league colors
- champ predict algo in ui
    - items
        - make it order agnostic
            - keep items as separate array indexes, add an extra index that has all items. ie. [1, 2, 3, 4, 0, 0, 0, [1, 2, 3, 4]]
            - maybe add a constant for those type of categorical items? need a way to find the index of subarray w/ all items - used in partition_classes
        - disregard 0s
            - best_split() - if data type is item and value is 0, can skip
    - add more game stats for attributes
    - create one for aram
- think about website purpose & design
    - champion/win graphs
        - a lot of visualizations could be shown in 1 graph w/ user selecting x/y
    - champion page w/ champ stats
    - ML page (win/loss predictor, champ predictor)
    - maybe a homepage with scrollable cool data? then a header at the top to manually explore different features
        - most interesting findings on homepage in a cool, scrollable, presentable format
        - header w/ tabs for manually exploring (graphs, champ stats, ML)
