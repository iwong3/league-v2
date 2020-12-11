import { Component } from 'react';

import * as d3 from 'd3';
import d3tip from 'd3-tip';

import './match-team-deltas-scatterplot.css';
import * as map from '../utility/maps/graph-fields.js';



export default class MatchTeamDeltasScatterplot extends Component {

    constructor(props) {
        super(props);

        this.state = {
            match_team_deltas_data: []
        }
    }

    componentDidMount() {
        this.setState({
            match_team_deltas_data: this.props.match_team_deltas_data
        }, function(d) {
            this.renderScatterplot();
        });
    }

    renderScatterplot() {

        /* constants */

        // dimensions
        const width = window.innerWidth * 0.8;
        const height = window.innerHeight * 0.8;
        const margin_left = window.innerWidth * 0.05;
        const margin_top = window.innerHeight * 0.05;
        const svg_width = width + "px";
        const svg_height = height + "px";
        const svg_margin_left = margin_left + "px";
        const svg_margin_top = margin_top + "px";
        const x_axis_title_height = window.innerHeight * 0.05;
        const y_axis_title_height = window.innerHeight * 0.05;
        // formatters & mappings
        const tick_format = d3.format(".2s");
        const field_mapping_name = "match_team_delta_fields";
        // dots
        const dot_radius = "0.5em";
        const dot_radius_hover = "1em";
        const dot_win_color = "#06C693";
        const dot_win_color_brighter = "#06C693";
        const dot_lose_color = "#EF476F";
        const dot_lose_color_brighter = "#EF476F";
        const dot_opacity = 0.65
        // animation
        const transition_duration = 1000;

        /* helper functions */

        // get scatterplot data based on selected axis fields
        // called whenever new dropdown option is selected
        const getScatterplotData = (x_axis_field, y_axis_field) => {
            let scatterplot_data = {
                "data": [],
                "min_x": Number.MAX_SAFE_INTEGER,
                "max_x": 0,
                "min_y": Number.MAX_SAFE_INTEGER,
                "max_y": 0
            };

            this.state.match_team_deltas_data.forEach(function(match) {
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
            });

            return scatterplot_data;
        }

        // get dot color based on win
        function getDotColor(data) {
            if (1 === data["win"]) {
                return dot_win_color;
            }
            return dot_lose_color;
        }

        // get dot hover color based on win
        function getDotHoverColor(data) {
            if (1 === data["win"]) {
                return dot_win_color_brighter;
            }
            return dot_lose_color_brighter;
        }

        /* start creating svg */

        // get scatterplot data & count min/max for scales
        let curr_x = "total_kills_delta";
        let curr_y = "total_deaths_delta"
        let scatterplot_data = getScatterplotData(curr_x, curr_y);
        const min_x = scatterplot_data["min_x"];
        const max_x = scatterplot_data["max_x"];
        const min_y = scatterplot_data["min_y"];
        const max_y = scatterplot_data["max_y"];
        scatterplot_data = scatterplot_data["data"];

        // set up selectable fields
        let fields = []
        const match_team_deltas_fields = map.graph_field_mappings[field_mapping_name];
        for (let field in match_team_deltas_fields) {
            if (match_team_deltas_fields[field]["type"] === "continuous") {
                fields.push(match_team_deltas_fields[field]["field"])
            }
        }

        // field selectors
        d3.select("#x-axis-selector")
            .selectAll("x-axis-options")
            .data(fields).enter()
            .append("option")
            .text(function(d) { return map.getFieldTitle(field_mapping_name, d); })
            .attr("value", function(d) { return d; })
            .property("selected", function(d) { return d === curr_x; });

        d3.select("#y-axis-selector")
            .selectAll("y-axis-options")
            .data(fields).enter()
            .append("option")
            .text(function(d) { return map.getFieldTitle(field_mapping_name, d); })
            .attr("value", function(d) { return d; })
            .property("selected", function(d) { return d === curr_y; });

        // svg
        let svg = d3.select("#match-team-deltas-scatterplot-body").append("svg")
            .attr("width", svg_width)
            .attr("height", svg_height)
            .style("margin", svg_margin_top + " " + svg_margin_left)
            .append("g");

        // scales
        let x_scale = d3.scaleLinear()
            .domain([min_x, max_x])
            .range([2 * y_axis_title_height, width - (2 * y_axis_title_height)]);

        let y_scale = d3.scaleLinear()
            .domain([min_y, max_y])
            .range([height - (2 * x_axis_title_height), x_axis_title_height]);

        // x axis
        const x_axis_int_ticks = x_scale.ticks()
            .filter(tick => Number.isInteger(tick));
        const x_axis = d3.axisBottom(x_scale)
            .tickFormat(tick_format)
            .tickValues(x_axis_int_ticks);
        svg.append("g")
            .attr("class", "x axis")
            .attr("transform", "translate(0, " + (height - (2 * x_axis_title_height)) + ")")
            .call(x_axis);

        let x_axis_title = svg.append("text")
            .attr("class", "axis title")
            .attr("text-anchor", "middle")
            .attr("x", width / 2)
            .attr("y", height - x_axis_title_height)
            .style("fill", "white")
            .text(map.getFieldTitle(field_mapping_name, curr_x));

        // y axis
        const y_axis_int_ticks = y_scale.ticks()
            .filter(tick => Number.isInteger(tick));
        const y_axis = d3.axisLeft(y_scale)
            .tickFormat(tick_format)
            .tickValues(y_axis_int_ticks);
        svg.append("g")
            .attr("class", "y axis")
            .attr("transform", "translate(" + (2 * y_axis_title_height) + ", 0)")
            .call(y_axis);

        let y_axis_title = svg.append("text")
            .attr("class", "axis title")
            .attr("text-anchor", "middle")
            .attr("x", -(height) / 2)
            .attr("y", y_axis_title_height)
            .attr("transform", "rotate(-90)")
            .style("fill", "white")
            .text(map.getFieldTitle(field_mapping_name, curr_y));

        // dot hover tooltip
        let tooltip = d3tip()
            .html(function(d) {
                return (`
                    <div class="match-team-deltas-scatterplot-tooltip">
                        <p>${map.getFieldTitle(field_mapping_name, curr_x) + ": " + d["x"]}</p>
                        <p>${map.getFieldTitle(field_mapping_name, curr_y) + ": " + d["y"]}</p>
                    </div>
                `)
            });
        svg.call(tooltip);

        // dot on hover
        function handleMouseOver(d) {
            // cursor and dot styling
            d3.select(this)
                .attr("r", dot_radius_hover)
                .style("cursor", "pointer")
                .style("fill", getDotHoverColor(d))
                .style("box-shadow", "20px 20px #ffffff");
            // tooltip
            tooltip.show(d, this)
                .style("left", x_scale(d["x"]) + (2 * y_axis_title_height) + "px")
                .style("top", y_scale(d["y"]) + (1.5 * x_axis_title_height) + "px")
                .style("transition", "opacity 0.2s ease-in-out");
        }

        function handleMouseOut(d) {
            // cursor and dot styling
            d3.select(this)
                .attr("r", dot_radius)
                .style("cursor", "none")
                .style("fill", getDotColor(d));
            // tooltip
            tooltip.hide(d, this);
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
                return y_scale(d["y"]);
            })
            .attr("fill", function(d) {
                return getDotColor(d);
            })
            .style("opacity", dot_opacity)
            .style("transition", "all 0.2s linear")
            .on("mouseover", function(event, d) {
                handleMouseOver.apply(this, [d]);
            })
            .on("mouseout", function(event, d) {
                handleMouseOut.apply(this, [d]);
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
            const updated_x_axis_int_ticks = x_scale.ticks()
                .filter(tick => Number.isInteger(tick));
            const updated_x_axis = d3.axisBottom(x_scale)
                .tickFormat(tick_format)
                .tickValues(updated_x_axis_int_ticks);
            svg.selectAll("g.x.axis")
                .transition().duration(transition_duration)
                .call(updated_x_axis);

            const updated_y_axis_int_ticks = y_scale.ticks()
                .filter(tick => Number.isInteger(tick));
            const updated_y_axis = d3.axisLeft(y_scale)
                .tickFormat(tick_format)
                .tickValues(updated_y_axis_int_ticks);
            svg.selectAll("g.y.axis")
                .transition().duration(transition_duration)
                .call(updated_y_axis);

            // update axis titles
            x_axis_title.text(map.getFieldTitle(field_mapping_name, x_field));
            y_axis_title.text(map.getFieldTitle(field_mapping_name, y_field));

            // update dots
            dots.data(scatterplot_data)
                .transition().duration(transition_duration)
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
            <div id="match-team-deltas-scatterplot">
                <div id="match-team-deltas-scatterplot-menu">
                    <select id="x-axis-selector"></select>
                    <select id="y-axis-selector"></select>
                </div>
                <div id="match-team-deltas-scatterplot-body"></div>
            </div>
        );
    }

}
