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
          missed = [],
          stat,
          statsHtml,
          i, _i,
          formatRow;
      overall.$el.html(
        '<h1>' + root.matrix.prettyPercent(data.stats[data.stats.length - 1].search_1_click_rate) + '</h1>' +
        '<p>Searches get at least 1 click</p>'
      );
      statsHtml = '';
      for(i=data.stats.length - 1; i >= 0; i--){
        stat = data.stats[i];
        counts.unshift(parseInt(stat.searches_performed, 10));
        clickRate.unshift(parseFloat(stat.search_1_click_rate));
        missed.unshift(
          parseInt(stat.missed_clicks || '0', 10) / parseInt(stat.searches_performed, 10)
        );
      }

      formatRow = function(label, num, rate){
        var result = '<li><label>' + label + ':</label>';
        if (typeof num != 'undefined') {
          result += '<em>' + root.matrix.numberWithCommas(Math.floor(num)) + '</em> ';
        }
        if (typeof rate != 'undefined') {
          result += '<span>(' + root.matrix.prettyPercent(rate) + ')</span>';
        }
        return result;
      };
      stat = data.stats[data.stats.length - 4];
      statsHtml += formatRow('searches', stat.searches_performed, stat.searches_performed_rate);
      statsHtml += formatRow('total&nbsp;clicks', stat.total_clicks);
      statsHtml += formatRow('missed&nbsp;clicks', stat.missed_clicks);
      statsHtml += formatRow('1-click', stat.search_1_click, stat.search_1_click_rate);
      statsHtml += formatRow('refinements', stat.refinements, stat.refinements_rate);
      statsHtml += formatRow('abandons', stat.search_abandons, stat.search_abandons_rate);
      statsHtml += formatRow('exits', stat.search_exits, stat.search_exits_rate);
      overall.$statsEl.html(statsHtml);
      if(typeof overall.sparkline === 'undefined'){
        overall.sparkline = root.matrix.sparklineGraph('#overall-click-graph', { data: clickRate, points: overall.points, height: 60, xpadding: 60, width: overall.$clickGraphEl.width() });
        overall.count_sparkline = root.matrix.sparklineGraph('#overall-count-graph', { data: counts, points: overall.points, height: 60, xpadding: 60, width: overall.$countGraphEl.width() });
        overall.missed_clicks_sparkline = root.matrix.sparklineGraph('#overall-missed-clicks-graph', { data: missed, points: overall.points, height: 60, xpadding: 60, width: overall.$missedClicksGraphEl.width() });
        overall.sparkline.update(
          clickRate,
          "Click rate over the past " + (Math.round(clickRate.length)) + " days",
          matrix.prettyPercent(clickRate[clickRate.length - 1])
        );
        overall.count_sparkline.update(
          counts,
          "Searches over the past " + (Math.round(counts.length)) + " days",
          root.matrix.numberWithCommas(counts[counts.length - 1])
        );
        overall.missed_clicks_sparkline.update(
          missed,
          "Estimated missed clicks per day over the past " + (Math.round(missed.length)) + " days",
          matrix.prettyPercent(missed[missed.length - 1])
        );
      } else {
        overall.sparkline.update(
          clickRate,
          "Click rate over the past " + (Math.round(clickRate.length)) + " days",
          matrix.prettyPercent(clickRate[clickRate.length - 1])
        );
        overall.count_sparkline.update(
          counts,
          "Searches over the past " + (Math.round(counts.length)) + " days",
          root.matrix.numberWithCommas(counts[counts.length - 1])
        );
        overall.missed_clicks_sparkline.update(
          missed,
          "Estimated missed clicks per day over the past " + (Math.round(missed.length)) + " days",
          matrix.prettyPercent(missed[missed.length - 1])
        );
      }

    },
    init: function(){
      overall.$el = $('#overall-count');
      overall.$clickGraphEl = $('#overall-click-graph');
      overall.$countGraphEl = $('#overall-count-graph');
      overall.$missedClicksGraphEl = $('#overall-missed-clicks-graph');
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
