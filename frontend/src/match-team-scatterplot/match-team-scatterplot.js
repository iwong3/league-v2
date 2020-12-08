import { Component } from 'react';

import * as d3 from 'd3';

import * as map from '../utility/maps/graph-fields.js';



export default class MatchTeamScatterplot extends Component {

    constructor(props) {
        super(props);

        this.state = {
            match_teams_data: []
        }
    }

    componentDidMount() {
        this.setState({
            match_teams_data: this.props.match_teams_data
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

        const getScatterplotData = (x_axis_field, y_axis_field) => {
            // get scatterplot data & count min/max for scales
            let scatterplot_data = {
                "data": [],
                "min_x": Number.MAX_SAFE_INTEGER,
                "max_x": 0,
                "min_y": Number.MAX_SAFE_INTEGER,
                "max_y": 0
            };
            this.state.match_teams_data.forEach(function(match) {
                // skip matches that aren't summoner's rift
                if (match["map_id"] === 11) {
                    // create and add scatterplot data
                    const data = {
                        "x": match[x_axis_field],
                        "y": match[y_axis_field],
                        "win": "Win" === match["win"] ? 1 : 0
                    }
                    scatterplot_data["data"].push(data);
                    // check for min/max
                    if (match[x_axis_field] < scatterplot_data["min_x"]) {
                        scatterplot_data["min_x"] = match[x_axis_field];
                    } else if (match[x_axis_field] > scatterplot_data["max_x"]) {
                        scatterplot_data["max_x"] = match[x_axis_field];
                    }
                    if (match[y_axis_field] < scatterplot_data["min_y"]) {
                        scatterplot_data["min_y"] = match[y_axis_field];
                    } else if (match[y_axis_field] > scatterplot_data["max_y"]) {
                        scatterplot_data["max_y"] = match[y_axis_field];
                    }
                }
            });

            return scatterplot_data;
        }

        let curr_x = "total_kills";
        let curr_y = "total_deaths"
        let scatterplot_data = getScatterplotData(curr_x, curr_y);
        const min_x = scatterplot_data["min_x"];
        const max_x = scatterplot_data["max_x"];
        const min_y = scatterplot_data["min_y"];
        const max_y = scatterplot_data["max_y"];
        scatterplot_data = scatterplot_data["data"];

        // set up fields
        let fields = []
        const match_team_fields = map.graph_field_mappings["match_team_fields"];
        for (let field in match_team_fields) {
            if (match_team_fields[field]["type"] === "continuous") {
                fields.push(match_team_fields[field]["field"])
            }
        }

        // field selectors
        d3.select("#x-axis-selector")
            .selectAll("x-axis-options")
            .data(fields).enter()
            .append("option")
            .text(function(d) { return map.getFieldTitle(d); })
            .attr("value", function(d) { return d; })
            .property("selected", function(d) { return d === curr_x; });

        d3.select("#y-axis-selector")
            .selectAll("y-axis-options")
            .data(fields).enter()
            .append("option")
            .text(function(d) { return map.getFieldTitle(d); })
            .attr("value", function(d) { return d; })
            .property("selected", function(d) { return d === curr_y; });

        // svg
        let svg = d3.select(".match-team-scatterplot").append("svg")
            .attr("width", svg_width)
            .attr("height", svg_height)
            .style("margin", svg_margin)
            .append("g");

        // scales
        let x_scale = d3.scaleLinear()
            .domain([min_x, max_x])
            .range([margin, width - margin]);

        let y_scale = d3.scaleLinear()
            .domain([min_y, max_y])
            .range([height - margin, margin]);

        // x axis
        const x_axis = d3.axisBottom(x_scale);
        svg.append("g")
            .attr("class", "x axis")
            .attr("transform", "translate(0, " + (height - margin) + ")")
            .call(x_axis);

        let x_axis_title = svg.append("text")
            .attr("class", "label")
            .attr("text-anchor", "middle")
            .attr("x", width / 2)
            .attr("y", height - margin)
            .text(map.getFieldTitle(curr_x));

        // y axis
        const y_axis = d3.axisLeft(y_scale);
        svg.append("g")
            .attr("class", "y axis")
            .attr("transform", "translate(" + (margin) + ", 0)")
            .call(y_axis);

        let y_axis_title = svg.append("text")
            .attr("class", "label")
            .attr("text-anchor", "middle")
            .attr("x", -(height) / 2)
            .attr("y", margin)
            .attr("transform", "rotate(-90)")
            .text(map.getFieldTitle(curr_y));

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
        let dots = svg.selectAll(".dot")
            .data(scatterplot_data).enter()
            .append("circle")
            .attr("class", "dot")
            .attr("r", dot_radius)
            .attr("cx", function(d) {
                return x_scale(d["x"]);
            })
            .attr("cy", function(d) {
                return y_scale(d["y"])
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

        function updateAxis(x_field, y_field) {

            // get updated data
            let scatterplot_data = getScatterplotData(x_field, y_field);
            const min_x = scatterplot_data["min_x"];
            const max_x = scatterplot_data["max_x"];
            const min_y = scatterplot_data["min_y"];
            const max_y = scatterplot_data["max_y"];
            scatterplot_data = scatterplot_data["data"];

            // update scales
            x_scale.domain([min_x, max_x]);
            y_scale.domain([min_y, max_y]);

            // update axis
            const updated_x_axis = d3.axisBottom(x_scale);
            svg.selectAll("g.x.axis").transition().duration(1000).call(updated_x_axis);
            const updated_y_axis = d3.axisLeft(y_scale);
            svg.selectAll("g.y.axis").call(updated_y_axis);


            // update axis titles
            x_axis_title.text(map.getFieldTitle(x_field));
            y_axis_title.text(map.getFieldTitle(y_field));

            // update dots
            dots.data(scatterplot_data)
                .transition()
                .duration(1000)
                .attr("cx", function(d) {
                    return x_scale(d["x"]);
                })
                .attr("cy", function(d) {
                    return y_scale(d["y"]);
                });

        }

        // field selector onchange
        d3.select("#x-axis-selector").on("change", function(d) {
            const selected_x = d3.select(this).property("value");
            curr_x = selected_x;
            updateAxis(selected_x, curr_y)
        });

        d3.select("#y-axis-selector").on("change", function(d) {
            const selected_y = d3.select(this).property("value");
            curr_y = selected_y;
            updateAxis(curr_x, selected_y)
        });

    }

    render() {
        return (
            <div className="match-team-scatterplot">
                <select id="x-axis-selector"></select>
                <select id="y-axis-selector"></select>
            </div>
        );
    }

}
