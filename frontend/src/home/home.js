import { Component } from 'react';

import axios from 'axios';

import ChampWinBar from "../champ-win-bar/champ-win-bar";
import MatchTeamScatterplot from "../match-team-scatterplot/match-team-scatterplot"
import DmgScatterplot from "../dmg-scatterplot/dmg-scatterplot";
import './home.css';


export default class Home extends Component {

    constructor(props) {
        super(props);

        this.state = {
            match_participants_data: [],
            match_teams_data: []
        }
    }

    componentDidMount() {
        const match_participants_url = "http://localhost:5000/match/participants?limit=1000";
        const match_teams_url = "http://localhost:5000/match/teams?limit=1000";
        axios.all([
            axios.get(match_participants_url),
            axios.get(match_teams_url)
        ]).then(axios.spread((mp_resp, mt_resp) => {
            this.setState({
                match_participants_data: mp_resp.data["data"],
                match_teams_data: mt_resp.data["data"]
            });
        }));
    }

    render() {
        return (
            <div className="home">
                <h1>league-v2 - league analytics</h1>
                { this.state.match_teams_data.length ? <MatchTeamScatterplot match_teams_data={this.state.match_teams_data}/> : <none/> }
            </div>
        );
    }

}
