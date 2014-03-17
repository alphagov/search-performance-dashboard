(function(){
  "use strict"
  var root = this,
      $ = root.jQuery;
  if(typeof root.matrix === 'undefined'){ root.matrix = {} }

  var search = {
    terms: [],
    newTerms: [],
    $el: false,
    nextRefresh: 0,

    endpoint: function(profileId){
      return "/realtime?"
        + "ids=ga:"+ profileId +"&"
        + "metrics=ga:activeVisitors&"
        + "dimensions=ga:pageTitle,ga:pagePath&"
        + "filters="+ encodeURIComponent("ga:pagePath==/search") +"&"
        + "sort=-ga:activeVisitors&"
        + "max-results=10000";
    },
    displayResults: function(){
      var term = search.newTerms.pop();
      if(term){
        search.$el.prepend('<li>'+$('<div>').text(term).html()+'</li>');
        search.$el.find('li:gt(20)').remove();
        root.setTimeout(search.displayResults, (search.nextRefresh - Date.now())/search.newTerms.length);
      } else {
        root.setTimeout(search.displayResults, 5e3);
      }
    },
    init: function(){
      search.$el = $('#search');

      search.reload();
      search.displayResults();
      window.setInterval(search.reload, 60e3);
    },
    reload: function(){
      var endpoint = search.endpoint(root.matrix.settings.profileId);

      search.nextRefresh = Date.now() + 60e3;
      $.ajax({ dataType: 'json', url: endpoint, success: search.parseResponse});
    }
  };

  root.matrix.search = search;
}).call(this);
