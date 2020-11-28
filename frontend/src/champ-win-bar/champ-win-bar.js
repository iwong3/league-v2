import { Component } from 'react';

import * as d3 from "d3";


export default class ChampWinBar extends Component {

    constructor(props) {
        super(props);

        this.state = {
            match_data: []
        }
    }

    componentDidMount() {
        this.setState({
            match_data: this.props.match_data
        }, function(d) {
            this.renderBarGraph();
        });
    }

    renderBarGraph() {

        // constants
        const width = window.innerWidth * 0.8;
        const height = window.innerHeight * 0.8;
        const margin = 40;
        const svg_width = width + "px";
        const svg_height = height + "px";
        const svg_margin = margin + "px";

        // get bar graph data
        let champion_win_data = {};
        this.state.match_data.forEach(function(match) {
            // skip matches that aren't summoner's rift
            if (match["map_id"] === 11) {
                const champ_name = match["champion_name"];
                // new champ
                if (!(champ_name in champion_win_data)) {
                    champion_win_data[champ_name] = {
                        "champ": champ_name,
                        "win_count": 0,
                        "game_count": 0
                    }
                }
                // update win/game count
                if (match["win"]) {
                    champion_win_data[champ_name]["win_count"] += 1;
                }
                champion_win_data[champ_name]["game_count"] += 1;
            }
        });

        // min/max win rates for scales
        let min_win_rate = 1;
        let max_win_rate = 0;
        // update bar graph data with champion win rates
        for (let key in champion_win_data) {
            const win_rate = champion_win_data[key]["win_count"] / champion_win_data[key]["game_count"];
            champion_win_data[key]["win_rate"] = win_rate;
            if (win_rate < min_win_rate) {
                min_win_rate = win_rate;
            }
            if (win_rate > max_win_rate) {
                max_win_rate = win_rate;
            }
        }

        // sort bar graph data by champ win rate desc
        // also grab champ names for x_scale domain
        let champ_names = [];
        let sorted_champ_win_data = [];
        Object.keys(champion_win_data).sort(function(a, b) {
            return champion_win_data[b]["win_rate"] - champion_win_data[a]["win_rate"];
        }).forEach(function(champ) {
            sorted_champ_win_data.push(champion_win_data[champ]);
            champ_names.push(champion_win_data[champ]["champ"]);
        });

        // svg
        let svg = d3.select(".champ-win-bar").append("svg")
            .attr("width", svg_width)
            .attr("height", svg_height)
            .style("margin", svg_margin)
            .append("g");

        // scales
        const x_scale = d3.scaleBand()
            .domain(champ_names)
            .range([margin, width - margin])
            .padding(0.2);

        const y_scale = d3.scaleLinear()
            .domain([min_win_rate, max_win_rate])
            .range([height - margin, margin]);

        // x-axis
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
            .text("Champion");

        // y-axis
        const y_axis = d3.axisLeft(y_scale)
            .tickFormat(function(d) {
                return (d.toFixed(4) * 100) + "%";
            });
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
            .text("Win Rate (%)");

        // bars
        svg.selectAll(".bar")
            .data(sorted_champ_win_data).enter()
            .append("rect")
            .attr("class", "bar")
            .attr("x", function(d) {
                return x_scale(d["champ"]);
            })
            .attr("y", function(d) {
                return y_scale(d["win_rate"]);
            })
            .attr("width", x_scale.bandwidth())
            .attr("height", function(d) {
                return height - y_scale(d["win_rate"]) - margin;
            })
            .attr("transform", "translate(0, 1)")
            .attr("fill", "#ff9da7")
            .style("opacity", 0.9);

    }

    render() {
        return (
            <div className="champ-win-bar"/>
        );
    }

}
