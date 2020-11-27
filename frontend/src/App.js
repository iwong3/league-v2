import { Component } from 'react';

import axios from 'axios';
import './App.css';


export default class App extends Component {

    constructor(props) {
        super(props)

        this.state = {
            match_data: []
        }
    }

    componentDidMount() {

        const match_url = "http://localhost:5000/match"
        axios.get(match_url).then(resp => {
            this.setState({
                match_data: resp.data
            })
        })

    }

    renderMatches() {

        let matches = []
        for (let i = 0; i < this.state.match_data.length; i++) {
            matches.push(<div>Champion: {this.state.match_data[i]["champion_name"]}</div>)
            matches.push(<div>Win/Loss: {this.state.match_data[i]["win"]}</div>)
        }
        return (
            <div>{matches}</div>
        )

    }

    render() {
        return (
            <div className="App">
                <h1> Match Data! </h1>
                {this.state.match_data.length ? this.renderMatches() : <none/>}
            </div>
        );
    }

}
