var counter = 0;

// This should make a Get request by user and show the marketCharts for this user
$( document ).ready(function() {
        // gerenerateAeeGraph();
    enableMarketButton();
    setCurrentDate();
});

function enableMarketButton(){
    $("#aee_button").hide();
    $("#market_button").show();
    $("#marketComparison_button").hide();
}

function enableAeeButton(){
    $("#aee_button").show();
    $("#market_button").hide();
    $("#marketComparison_button").hide();
}

function enableMarketComparisonButton(){
    $("#aee_button").hide();
    $("#market_button").hide();
    $("#marketComparison_button").show();
}

function setCurrentDate(){
    var now = new Date();
    var month = (now.getMonth() + 1);               
    var day = now.getDate();
    if(month < 10) 
        month = "0" + month;
    if(day < 10) 
        day = "0" + day;
    var today = now.getFullYear() + '-' + month + '-' + day;
    $('#startDate').val(today);
    $('#startDate').prop("max",today);
    $('#startDate').prop("min","2014-01-01");

}

function generateContainer(counter,type){
    var graphId = "graph"+counter;
    var chartId = "chart"+counter;
    var head =  d3.select("body").select("#wrapper")
                    .select("#page-wrapper")
                    .select("#container-fluid")
                    .append("div")
                    .attr("class","row")
                    .attr("id",graphId)
                    .append("div")
                    .attr("class","col-lg-12")
                    .append("div")
                    .attr("class","panel panel-default")
                    .style("height","550px")
    if (type == 0){
        var heading = head.append("div")
                    .attr("class","panel-heading")
                    .append("h3")
                    .attr("id",graphId+"-title")
                    .attr("class","panel-title")
                    .text($("#symbol option:selected").text())
                    .append("small")
                    .text($("#type option:selected").text() + " Market History for a year")

        var body = head.append("div")
                    .attr("class","panel-body")
                    .attr("id",chartId)
                    .append("svg")
                    .style("width","100%")
                    .style("padding-bottom","300px")
                    
    }
    if (type == 1){
        var heading = head.append("div")
                    .attr("class","panel-heading")
                    .append("h3")
                    .attr("id",graphId+"-title")
                    .attr("class","panel-title")
                    .text($("#key_1").val())
                    .append("small")
                    .text(" 2000-2015")

        var body = head.append("div")
                    .attr("class","panel-body")
                    .append("svg")
                    .style("display","inline-block")
                    .style("position","relative")
                    .style("width","100%")
                    .style("padding-bottom","600px")
                    .style("vertical-align","top")
                    .style("overflow","hidden")
                    .attr("id",chartId)

    }
    
    

}

function generateAeeGraph(){
    $.get('/_getAEEDATA', 
    { key_1: $("#key_1").val()},
    function (energy_data) {
        console.log(energy_data.result)
        // console.log(counter)
        $("#no_graphs").empty();
        $("#no_graphs").remove();
        generateContainer(counter,1)
        var chartId = '#chart'+counter
        counter+=1;
        var colors = d3.scale.category20();
        var chart;
        nv.addGraph(function() {
            chart = nv.models.stackedAreaChart()
                .useInteractiveGuideline(true)
                .x(function(d) { return d[0] })
                .y(function(d) { return d[1] })
                .controlLabels({stacked: "Stacked"})
                .width(965)
                .height(500)
                .duration(300);
            chart.xAxis.tickFormat(function(d) { return d });
            chart.yAxis.tickFormat(d3.format(',.2f'));
            chart.legend.vers('furious');
            d3.select(chartId)
                .datum(energy_data.result)
                .transition().duration(1000)
                .call(chart)
                .each('start', function() {
                    setTimeout(function() {
                        d3.selectAll(chartId+' *').each(function() {
                            if(this.__transition__)
                                this.__transition__.duration = 1;
                        })
                    }, 0)
                });
            d3.selectAll("g.nv-series")
              

            nv.utils.windowResize(chart.update);
            return chart;
        });
    });
}

function generateMarketHistoryGraph(){
    console.log($("#type").val());
    console.log($("#symbol").val());
    console.log($("#startDate").val());
    $.get('/_getMarketHistoryData', 
    { symbol:    $("#symbol").val(),
      type:      $("#type").val(),
      startDate: $("#startDate").val()},
    function (market_history_data) {
        console.log("entre");
        console.log(market_history_data.result)
        // console.log(counter)
        $("#no_graphs").empty();
        $("#no_graphs").remove();
        generateContainer(counter, 0);
        var chartId = '#chart'+counter;
        location.href = chartId;
        counter+=1;
        var colors = d3.scale.category20();
        var chart;
        nv.addGraph(function() {
            var chart = nv.models.candlestickBarChart()
                .x(function(d) { return d['date'] })
                .y(function(d) { return d['close'] })
                .duration(250)
                .margin({left: 75, bottom: 50});
            // chart sub-models (ie. xAxis, yAxis, etc) when accessed directly, return themselves, not the parent chart, so need to chain separately
            chart.xAxis
                    .axisLabel("Dates")
                    .tickFormat(function(d) {
                        return d3.time.format('%x')(new Date((d)));
                    });
            chart.yAxis
                    .axisLabel($("#symbol").val() +' Stock Price')
                    .tickFormat(function(d,i){ return '$' + d3.format(',.1f')(d); });
            d3.select(chartId+" svg")
                    .datum(market_history_data.result)
                    .transition().duration(500)
                    .call(chart);
            nv.utils.windowResize(chart.update);

            return chart;
        });
    });
}