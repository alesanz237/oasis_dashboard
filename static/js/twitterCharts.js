
$( document ).ready(function() {
    // generateTweetsCountChart();

    $.get('/_getPositiveWords', 
        function (positive_words) {
            console.log("Entre a positive words");
            console.log(positive_words.result[0]);
            console.log(positive_words.result[1]);
            Morris.Donut({
                element: 'positive-tweets',
                data: positive_words.result,
                resize: true,
                colors: [
                    '#0000ff',
                    '#0000e5',
                    '#1919ff',
                    '#0000cc',
                    '#3232ff',
                    '#0000b2',
                    '#4c4cff',
                    '#6666ff',
                    '#7f7fff',
                    '#9999ff',     
                ],
            });
        });

    // generateNegativeWordsChart();
});


// function generateTweetsCountChart(){
    // $.get('/_getTweetsCount', 
    //     function (tweets_count) {
    //         var data = [{
    //             label: "Positive Tweets",
    //             data: tweets_count.result[0],
    //             color: '#337AB8'
    //         }, {
    //             label: "Negative Tweets",
    //             data: tweets_count.result[1],
    //             color: '#ff0000'
    //         }];

    //         var plotObj = $.plot($("#flot-pie-chart"), data, {
    //             series: {
    //                 pie: {
    //                     show: true
    //                 }
    //             },
    //             grid: {
    //                 hoverable: true,
    //             },
    //             tooltip: true,
    //             tooltipOpts: {
    //                 content: "%p.0%, %s", // show percentages, rounding to 2 decimal places
    //                 shifts: {
    //                     x: 20,
    //                     y: 0
    //                 },
    //                 defaultTheme: true
    //             }
    //         });
    //     });
// }



