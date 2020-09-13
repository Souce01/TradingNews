// removes images that didn't load
$(".article-img")
  .on("error", function (e) {
    $(this).remove();
    e.preventDefault();
  });

// Changes the color an article's title on hover
$(".article")
  .hover(function (e) {
    $(this).find(".article-title").css("color", "#4193c6");
    e.preventDefault();
  }, function (e) {
    $(this).find(".article-title").css("color", "white");
    e.preventDefault();
  });

$("#navbar-search-field").click(function(e) {
  $(this).parent().addClass("search-field-container-show");
  $("#search-field-content").addClass("active")
  e.stopPropagation();
});

$(document).click(function () {
  $("#navbar-search-field-container").removeClass("search-field-container-show");
  $("#search-field-content").removeClass("active");
});

// TODO: makes an api call to get search endpoint
$("#navbar-search-field").on("change input", function (e) {
  if ($(this).val() != ""){
    console.log($(this).val());
    fetch(`http://127.0.0.1:8000/api/searchEndPoint/${$(this).val()}`)
      .then(resp => {
        if (!resp.ok) {
          throw Error(resp.statusText);
        }
        return resp;
      })
      .then(resp => {
        return resp.json();
      })
      .then(data => {
        let content = $('#search-field-content');
        let matches = data['bestMatches'];
        // clears matches
        content.empty();
        
        for (let x of matches){
          content.append(`
            <a href="http://127.0.0.1:8000/company/${x['1. symbol']}" class="search-field-content-element">
              ${x['1. symbol']}
            </a>
          `);
        }
        console.log(matches);
      })
      .catch(err => {
        console.log(err);
      });
  }
  e.preventDefault();
});

