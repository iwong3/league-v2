import { Component } from 'react';

import axios from 'axios';
import * as d3 from "d3";


export default class DmgScatterplot extends Component {

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

    renderScatterplot() {

        // get total_damage_dealt_to_champions
        // get total_damage_taken
        // get win

    }



}
