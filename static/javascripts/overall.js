(function(){
  "use strict"
  var root = this,
      $ = root.jQuery;
  if(typeof root.matrix === 'undefined'){ root.matrix = {} }

  var overall = {
    $el: false,
    points: 7,

    endpoint: function(){
      return "/overall?start_days_ago=14"
    },
    parseResponse: function(data){
      var counts = [],
          clickRate = [],
          stat,
          statsHtml,
          i, _i;
      overall.$el.html(
        '<h1>' + root.matrix.prettyPercent(data.stats[data.stats.length - 1].search_1_click_rate) + '</h1>' +
        '<p>Searches get at least 1 click</p>'
      );
      statsHtml = '';
      for(i=data.stats.length - 1; i >= 0; i--){
        stat = data.stats[i];
        counts.unshift(parseInt(stat.searches_performed, 10));
        clickRate.unshift(parseFloat(stat.search_1_click_rate));
        statsHtml += '<li>' +
          '1-click: ' + root.matrix.prettyPercent(stat.search_1_click_rate) +
          '<br>searches: ' + root.matrix.numberWithCommas(stat.searches_performed) +
        '</li>';
      }
      overall.$statsEl.html(statsHtml);
      if(typeof overall.sparkline === 'undefined'){
        overall.sparkline = root.matrix.sparklineGraph('#overall-click-graph', { data: clickRate, points: overall.points, height: 60, width: overall.$clickGraphEl.width() });
        overall.count_sparkline = root.matrix.sparklineGraph('#overall-count-graph', { data: counts, points: overall.points, height: 60, width: overall.$countGraphEl.width() });
        overall.sparkline.update(
          clickRate,
          "Click rate over the past " + (Math.round(clickRate.length)) + " days"
        );
        overall.count_sparkline.update(
          counts,
          "Searches over the past " + (Math.round(counts.length)) + " days"
        );
      } else {
        overall.sparkline.update(
          clickRate,
          "Click rate over the past " + (Math.round(clickRate.length)) + " days"
        );
        overall.count_sparkline.update(
          counts,
          "Searches over the past " + (Math.round(counts.length)) + " days"
        );
      }

    },
    init: function(){
      overall.$el = $('#overall-count');
      overall.$clickGraphEl = $('#overall-click-graph');
      overall.$countGraphEl = $('#overall-count-graph');
      overall.$statsEl = $('#overall-statistics');
      overall.reload();
      window.setInterval(overall.reload, 20e3);
    },
    reload: function(){
      var endpoint = overall.endpoint();
      $.ajax({ dataType: 'json', url: endpoint, success: overall.parseResponse});
    }
  };
  root.matrix.overall = overall;
}).call(this);
