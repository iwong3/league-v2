import { Component } from 'react';

import axios from 'axios';

import ChampWinBar from "../champ-win-bar/champ-win-bar";
import DmgScatterplot from "../dmg-scatterplot/dmg-scatterplot";
import './home.css';


export default class Home extends Component {

    constructor(props) {
        super(props);

        this.state = {
            match_data: []
        }
    }

    componentDidMount() {
        const match_url = "http://localhost:5000/match";
        axios.get(match_url).then(resp => {
            this.setState({
                match_data: resp.data
            });
        });
    }

    render() {
        return (
            <div className="home">
                <h1>league-v2 - league analytics</h1>
                { this.state.match_data.length ? <DmgScatterplot match_data={this.state.match_data}/> : <none/> }
                { this.state.match_data.length ? <ChampWinBar match_data={this.state.match_data}/> : <none/> }
            </div>
        );
    }

}
