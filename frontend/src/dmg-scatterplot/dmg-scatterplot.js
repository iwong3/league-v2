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
        }).then(resp => {
            this.renderScatterplot();
        });
    }

    renderScatterplot() {

        // constants
        const width = window.innerWidth * 0.8;
        const height = window.innerHeight * 0.8;
        const margin = 40;
        const svg_width = width + "px";
        const svg_height = height + "px";
        const svg_margin = margin + "px";

        // get scatterplot data
        let dmg_scatterplot_data = []
        // count min/max for scales
        let min_dmg_dealt = Number.MAX_SAFE_INTEGER;
        let max_dmg_dealt = 0;
        let min_dmg_taken = Number.MAX_SAFE_INTEGER;
        let max_dmg_taken = 0;
        this.state.match_data.forEach(function(match) {
            // create and add scatterplot data
            const data = {
                "dmg_dealt": match["total_damage_dealt"],
                "dmg_taken": match["total_damage_taken"],
                "win": match["win"]
            }
            dmg_scatterplot_data.push(data);
            // check for min/max
            if (match["total_damage_dealt"] < min_dmg_dealt) {
                min_dmg_dealt = match["total_damage_dealt"];
            } else if (match["total_damage_dealt"] > max_dmg_dealt) {
                max_dmg_dealt = match["total_damage_dealt"];
            }
            if (match["total_damage_taken"] < min_dmg_taken) {
                min_dmg_taken = match["total_damage_taken"];
            } else if (match["total_damage_taken"] > max_dmg_taken) {
                max_dmg_taken = match["total_damage_taken"];
            }
        });

        // svg
        let svg = d3.select(".dmg-scatterplot").append("svg")
            .attr("width", svg_width)
            .attr("height", svg_height)
            .style("margin", svg_margin)
            .append("g");

        // scales
        const x_scale = d3.scaleLinear()
            .domain([min_dmg_dealt, max_dmg_dealt])
            .range([margin, width - margin]);

        const y_scale = d3.scaleLinear()
            .domain([min_dmg_taken, max_dmg_taken])
            .range([height - margin, margin]);

        // x axis
        const x_axis = d3.axisBottom(x_scale);
        svg.append("g")
            .attr("class", "x axis")
            .attr("transform", "translate(0, " + (height - margin) + ")")
            .call(x_axis);

        svg.append("text")
            .attr("class", "label")
            .attr("text-anchor", "middle")
            .attr("x", width / 2)
            .attr("y", height - margin)
            .text("Damage Dealt to Champions");

        // y axis
        const y_axis = d3.axisLeft(y_scale);
        svg.append("g")
            .attr("class", "y axis")
            .attr("transform", "translate(" + (margin) + ", 0)")
            .call(y_axis);

        svg.append("text")
            .append("class", "label")
            .attr("text-anchor", "middle")
            .attr("x", -(height) / 2)
            .attr("y", margin)
            .attr("transform", "rotate(-90)")
            .text("Damage Taken");

        // dot styling
        const dot_radius = 5;
        const dot_win_color = "green";
        const dot_lose_color = "red";

        // draw dots
        svg.selectAll(".dot")
            .data(dmg_scatterplot_data).enter()
            .append("circle")
            .attr("class", "dot")
            .attr("r", dot_radius)
            .attr("cx", function(d) {
                return x_scale(d["dmg_dealt"]);
            })
            .attr("cy", function(d) {
                return y_scale(d["dmg_taken"])
            })
            .attr("fill", function(d) {
                if (1 === d["win"]) {
                    return dot_win_color;
                }
                return dot_lose_color;
            })
            .style("opacity", 0.5);

    }

    render() {
        return (
            <div className="dmg-scatterplot">
            </div>
        );
    }

}
