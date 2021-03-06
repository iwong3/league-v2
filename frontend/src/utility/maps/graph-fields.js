// constants and helper functions for graph field mappings

// get field title given mapping name and field name
export function getFieldTitle(mapping_name, field_name) {
    for (let field in graph_field_mappings[mapping_name]) {
        if (graph_field_mappings[mapping_name][field]["field"] === field_name) {
            return graph_field_mappings[mapping_name][field]["title"];
        }
    }
    return "";
}

export const graph_field_mappings = {
    "match_team_fields": [
        {
            "field": "match_id",
            "title": "Match ID",
            "type": "id"
        },
        {
            "field": "team_id",
            "title": "Team ID",
            "type": "category"
        },
        {
            "field": "win",
            "title": "Win",
            "type": "category"
        },
        {
            "field": "total_kills",
            "title": "Total Kills",
            "type": "continuous"
        },
        {
            "field": "total_deaths",
            "title": "Total Deaths",
            "type": "continuous"
        },
        {
            "field": "total_assists",
            "title": "Total Assists",
            "type": "continuous"
        },
        {
            "field": "total_physical_damage_dealt",
            "title": "Total Physical Damage Dealt",
            "type": "continuous"
        },
        {
            "field": "total_magic_damage_dealt",
            "title": "Total Magic Damage Dealt",
            "type": "continuous"
        },
        {
            "field": "total_true_damage_dealt",
            "title": "Total True Damage Dealt",
            "type": "continuous"
        },
        {
            "field": "total_damage_dealt",
            "title": "Total Damage Dealt",
            "type": "continuous"
        },
        {
            "field": "total_physical_damage_dealt_to_champions",
            "title": "Total Physical Damage Dealt to Champions",
            "type": "continuous"
        },
        {
            "field": "total_magic_damage_dealt_to_champions",
            "title": "Total Magic Damage Dealt to Champions",
            "type": "continuous"
        },
        {
            "field": "total_true_damage_dealt_to_champions",
            "title": "Total True Damage Dealt to Champions",
            "type": "continuous"
        },
        {
            "field": "total_damage_dealt_to_champions",
            "title": "Total Damage Dealt to Champions",
            "type": "continuous"
        },
        {
            "field": "total_physical_damage_taken",
            "title": "Total Physical Damage Taken",
            "type": "continuous"
        },
        {
            "field": "total_magic_damage_taken",
            "title": "Total Magic Damage Taken",
            "type": "continuous"
        },
        {
            "field": "total_true_damage_taken",
            "title": "Total True Damage Taken",
            "type": "continuous"
        },
        {
            "field": "total_damage_taken",
            "title": "Total Damage Taken",
            "type": "continuous"
        },
        {
            "field": "total_damage_self_mitigated",
            "title": "Total Damage Self Mitigated",
            "type": "continuous"
        },
        {
            "field": "total_heal",
            "title": "Total Healing",
            "type": "continuous"
        },
        {
            "field": "total_minions_killed",
            "title": "Total Minions Killed",
            "type": "continuous"
        },
        {
            "field": "total_neutral_minions_killed",
            "title": "Total Neutral Minions Killed",
            "type": "continuous"
        },
        {
            "field": "total_neutral_minions_killed_team_jungle",
            "title": "Total Neutral Minions Killed in Team Jungle",
            "type": "continuous"
        },
        {
            "field": "total_neutral_minions_killed_enemy_jungle",
            "title": "Total Neutral Minions Killed in Enemy Jungle",
            "type": "continuous"
        },
        {
            "field": "total_time_crowd_control_dealt",
            "title": "Total Time CC Dealt",
            "type": "continuous"
        },
        {
            "field": "total_time_ccing_others",
            "title": "Total Time CCing Champions",
            "type": "continuous"
        },
        {
            "field": "total_damage_dealt_to_turrets",
            "title": "Total Damage Dealt to Turrets",
            "type": "continuous"
        },
        {
            "field": "total_damage_dealt_to_objectives",
            "title": "Total Damage Dealt to Objectives",
            "type": "continuous"
        },
        {
            "field": "total_gold_earned",
            "title": "Total Gold Earned",
            "type": "continuous"
        },
        {
            "field": "total_gold_spent",
            "title": "Total Gold Spent",
            "type": "continuous"
        },
        {
            "field": "total_vision_score",
            "title": "Total Vision Score",
            "type": "continuous"
        },
        {
            "field": "total_vision_wards_bought_in_game",
            "title": "Total Vision Wards Bought in Game",
            "type": "continuous"
        },
        {
            "field": "total_wards_killed",
            "title": "Total Wards Killed",
            "type": "continuous"
        },
        {
            "field": "total_wards_placed",
            "title": "Total Wards Placed",
            "type": "continuous"
        },
        {
            "field": "first_blood",
            "title": "First Blood",
            "type": "category"
        },
        {
            "field": "first_baron",
            "title": "First Baron",
            "type": "category"
        },
        {
            "field": "first_dragon",
            "title": "First Dragon",
            "type": "category"
        },
        {
            "field": "first_inhibitor",
            "title": "First Inhibitor",
            "type": "category"
        },
        {
            "field": "first_rift_herald",
            "title": "First Rift Herald",
            "type": "category"
        },
        {
            "field": "first_tower",
            "title": "First Tower",
            "type": "category"
        },
        {
            "field": "baron_kills",
            "title": "Baron Kills",
            "type": "continuous"
        },
        {
            "field": "dragon_kills",
            "title": "Dragon Kills",
            "type": "continuous"
        },
        {
            "field": "inhibitor_kills",
            "title": "Inhibitor Kills",
            "type": "continuous"
        },
        {
            "field": "rift_herald_kills",
            "title": "Rift Herald Kills",
            "type": "continuous"
        },
        {
            "field": "tower_kills",
            "title": "Tower Kills",
            "type": "continuous"
        },
        {
            "field": "champion_ban_1",
            "title": "Ban 1",
            "type": "category"
        },
        {
            "field": "champion_ban_1",
            "title": "Ban 2",
            "type": "category"
        },
        {
            "field": "champion_ban_1",
            "title": "Ban 3",
            "type": "category"
        },
        {
            "field": "champion_ban_1",
            "title": "Ban 4",
            "type": "category"
        },
        {
            "field": "champion_ban_1",
            "title": "Ban 5",
            "type": "category"
        }
    ],
    "match_team_delta_fields": [
        {
            "field": "match_id",
            "title": "Match ID",
            "type": "id"
        },
        {
            "field": "team_id",
            "title": "Team ID",
            "type": "category"
        },
        {
            "field": "win",
            "title": "Win",
            "type": "category"
        },
        {
            "field": "total_kills_delta",
            "title": "Total Kills Delta",
            "type": "continuous"
        },
        {
            "field": "total_deaths_delta",
            "title": "Total Deaths Delta",
            "type": "continuous"
        },
        {
            "field": "total_assists_delta",
            "title": "Total Assists Delta",
            "type": "continuous"
        },
        {
            "field": "total_physical_damage_dealt_delta",
            "title": "Total Physical Damage Dealt Delta",
            "type": "continuous"
        },
        {
            "field": "total_magic_damage_dealt_delta",
            "title": "Total Magic Damage Dealt Delta",
            "type": "continuous"
        },
        {
            "field": "total_true_damage_dealt_delta",
            "title": "Total True Damage Dealt Delta",
            "type": "continuous"
        },
        {
            "field": "total_damage_dealt_delta",
            "title": "Total Damage Dealt Delta",
            "type": "continuous"
        },
        {
            "field": "total_physical_damage_dealt_to_champions_delta",
            "title": "Total Physical Damage Dealt to Champions Delta",
            "type": "continuous"
        },
        {
            "field": "total_magic_damage_dealt_to_champions_delta",
            "title": "Total Magic Damage Dealt to Champions Delta",
            "type": "continuous"
        },
        {
            "field": "total_true_damage_dealt_to_champions_delta",
            "title": "Total True Damage Dealt to Champions Delta",
            "type": "continuous"
        },
        {
            "field": "total_damage_dealt_to_champions_delta",
            "title": "Total Damage Dealt to Champions Delta",
            "type": "continuous"
        },
        {
            "field": "total_physical_damage_taken_delta",
            "title": "Total Physical Damage Taken Delta",
            "type": "continuous"
        },
        {
            "field": "total_magic_damage_taken_delta",
            "title": "Total Magic Damage Taken Delta",
            "type": "continuous"
        },
        {
            "field": "total_true_damage_taken_delta",
            "title": "Total True Damage Taken Delta",
            "type": "continuous"
        },
        {
            "field": "total_damage_taken_delta",
            "title": "Total Damage Taken Delta",
            "type": "continuous"
        },
        {
            "field": "total_damage_self_mitigated_delta",
            "title": "Total Damage Self Mitigated Delta",
            "type": "continuous"
        },
        {
            "field": "total_heal_delta",
            "title": "Total Healing Delta",
            "type": "continuous"
        },
        {
            "field": "total_minions_killed_delta",
            "title": "Total Minions Killed Delta",
            "type": "continuous"
        },
        {
            "field": "total_neutral_minions_killed_delta",
            "title": "Total Neutral Minions Killed Delta",
            "type": "continuous"
        },
        {
            "field": "total_neutral_minions_killed_team_jungle_delta",
            "title": "Total Neutral Minions Killed in Team Jungle Delta",
            "type": "continuous"
        },
        {
            "field": "total_neutral_minions_killed_enemy_jungle_delta",
            "title": "Total Neutral Minions Killed in Enemy Jungle Delta",
            "type": "continuous"
        },
        {
            "field": "total_time_crowd_control_dealt_delta",
            "title": "Total Time CC Dealt Delta",
            "type": "continuous"
        },
        {
            "field": "total_time_ccing_others_delta",
            "title": "Total Time CCing Champions Delta",
            "type": "continuous"
        },
        {
            "field": "total_damage_dealt_to_turrets_delta",
            "title": "Total Damage Dealt to Turrets Delta",
            "type": "continuous"
        },
        {
            "field": "total_damage_dealt_to_objectives_delta",
            "title": "Total Damage Dealt to Objectives Delta",
            "type": "continuous"
        },
        {
            "field": "total_gold_earned_delta",
            "title": "Total Gold Earned Delta",
            "type": "continuous"
        },
        {
            "field": "total_gold_spent_delta",
            "title": "Total Gold Spent Delta",
            "type": "continuous"
        },
        {
            "field": "total_vision_score_delta",
            "title": "Total Vision Score Delta",
            "type": "continuous"
        },
        {
            "field": "total_vision_wards_bought_in_game_delta",
            "title": "Total Vision Wards Bought in Game Delta",
            "type": "continuous"
        },
        {
            "field": "total_wards_killed_delta",
            "title": "Total Wards Killed Delta",
            "type": "continuous"
        },
        {
            "field": "total_wards_placed_delta",
            "title": "Total Wards Placed Delta",
            "type": "continuous"
        },
        {
            "field": "baron_kills_delta",
            "title": "Baron Kills Delta",
            "type": "continuous"
        },
        {
            "field": "dragon_kills_delta",
            "title": "Dragon Kills Delta",
            "type": "continuous"
        },
        {
            "field": "inhibitor_kills_delta",
            "title": "Inhibitor Kills Delta",
            "type": "continuous"
        },
        {
            "field": "rift_herald_kills_delta",
            "title": "Rift Herald Kills Delta",
            "type": "continuous"
        },
        {
            "field": "tower_kills_delta",
            "title": "Tower Kills Delta",
            "type": "continuous"
        }
    ]
}
