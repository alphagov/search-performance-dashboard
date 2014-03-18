(function(){
  "use strict"
  var root = this,
      $ = root.jQuery;
  if(typeof root.matrix === 'undefined'){ root.matrix = {} }

  function htmlEncode(value){
    return $('<div/>').text(value).html();
  }

  var search = {
    $el: false,

    endpoint: function(){
      return "/poor_searches?start_days_ago=14"
    },
    parseResponse: function(data){
      var i, _i, s, searchesHtml;
      searchesHtml = '';
      for (i = 0, _i = data.searches.length; i < _i; i++) {
        s = data.searches[i];
        searchesHtml += '<li class="tile">'
          + '<a href="/clicks?q=' + escape(s.norm_search) + '">'
          + htmlEncode(s.norm_search)
          + '</a>'
          + '&nbsp;<span>('
          + root.matrix.numberWithCommas(Math.floor(s.missed))
          + ')</span>'
          + '</li>';
      }
      search.$el.html(searchesHtml);
    },
    init: function(){
      search.$el = $('.poor_searches #content');
      search.reload();
      window.setInterval(search.reload, 60e3);
    },
    reload: function(){
      var endpoint = search.endpoint();
      $.ajax({ dataType: 'json', url: endpoint, success: search.parseResponse});
    }
  };

  root.matrix.search = search;
}).call(this);
