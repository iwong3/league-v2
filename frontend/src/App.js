import { Component } from 'react';

import axios from 'axios';
import './App.css';


export default class App extends Component {

    constructor(props) {
        super(props)

        this.state = {
            match_history_data: []
        }
    }

    componentDidMount() {

        const match_history_url = "http://localhost:5000/match-history"
        axios.get(match_history_url).then(resp => {
            this.setState({
                match_history_data: resp.data
            })
        })

    }

    renderMatchHistory = () => {

        let match_history = []
        for (let i = 0; i < this.state.match_history_data.length; i++) {
            match_history.push(<div>Champion: {this.state.match_history_data[i]["champion_name"]}</div>)
            match_history.push(<div>Played At: {this.state.match_history_data[i]["date"]}</div>)
        }
        return (
            <div>{match_history}</div>
        )

    }

    render() {
        return (
            <div className="App">
                <h1> Match History! </h1>
                {this.state.match_history_data.length ? this.renderMatchHistory() : <none/>}
            </div>
        );
    }

}
