import { Component } from 'react';

import * as d3 from 'd3';


export default class CsVsCcScatterplot extends Component {

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
        let scatterplot_data = []
        // count min/max for scales
        let min_cs = Number.MAX_SAFE_INTEGER;
        let max_cs = 0;
        let min_cc = Number.MAX_SAFE_INTEGER;
        let max_cc = 0;
        this.state.match_data.forEach(function(match) {
            // create and add scatterplot data
            const data = {
                "cs": match["neutral_minions_killed"],
                "cc": match["time_ccing_others"],
                "win": match["win"]
            }
            scatterplot_data.push(data);
            // check for min/max
            if (match["neutral_minions_killed"] < min_cs) {
                min_cs = match["neutral_minions_killed"];
            } else if (match["neutral_minions_killed"] > max_cs) {
                max_cs = match["neutral_minions_killed"];
            }
            if (match["time_ccing_others"] < min_cc) {
                min_cc = match["time_ccing_others"];
            } else if (match["time_ccing_others"] > max_cc) {
                max_cc = match["time_ccing_others"];
            }
        });

        // svg
        let svg = d3.select(".cs-vs-cc-scatterplot").append("svg")
            .attr("width", svg_width)
            .attr("height", svg_height)
            .style("margin", svg_margin)
            .append("g");

        // scales
        const x_scale = d3.scaleLinear()
            .domain([min_cs, max_cs])
            .range([margin, width - margin]);

        const y_scale = d3.scaleLinear()
            .domain([min_cc, max_cc])
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
            .text("Neutral Minions Killed (CS)");

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
            .text("Time CCing Others");

        // dot styling
        const dot_radius = 5;
        const dot_radius_hover = 10;
        const dot_win_color = "green";
        const dot_lose_color = "red";

        // dot on hover
        function handleMouseOver(d) {
            // cursor and dot styling
            d3.select(this)
                .style("cursor", "pointer")
                .style("filter", "brightness(1.5)")
                .attr("r", dot_radius_hover);
        }

        function handleMouseOut(d) {
            // cursor and dot styling
            d3.select(this)
                .style("cursor", "none")
                .attr("r", dot_radius);
        }

        // draw dots
        svg.selectAll(".dot")
            .data(scatterplot_data).enter()
            .append("circle")
            .attr("class", "dot")
            .attr("r", dot_radius)
            .attr("cx", function(d) {
                return x_scale(d["cs"]);
            })
            .attr("cy", function(d) {
                return y_scale(d["cc"])
            })
            .attr("fill", function(d) {
                if (1 === d["win"]) {
                    return dot_win_color;
                }
                return dot_lose_color;
            })
            .style("opacity", 0.5)
            .style("transition", "all 0.2s ease-in-out")
            .on("mouseover", function(d) {
                handleMouseOver.apply(this);
            })
            .on("mouseout", function(d) {
                handleMouseOut.apply(this);
            });

    }

    render() {
        return (
            <div className="cs-vs-cc-scatterplot"/>
        );
    }

}
