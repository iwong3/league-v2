import { Component } from 'react';

import axios from 'axios';

import DmgScatterplot from "../dmg-scatterplot/dmg-scatterplot";


export default class Home extends Component {

    constructor(props) {
        super(props);

        this.state = {}
    }

    render() {
        return (
            <div className="home">
                <h1>league-v2 - league analytics</h1>
                <DmgScatterplot/>
            </div>
        );
    }

}
