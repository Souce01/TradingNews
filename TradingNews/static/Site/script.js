// removes images that didn't load
$(".article-img")
  .on("error", function (e) {
    $(this).remove();
    e.preventDefault();
  })

// Changes the color an article's title on hover
$(".article")
  .hover(function (e) {
    $(this).find(".article-title").css("color", "#4193c6");
    e.preventDefault();
  }, function (e) {
    $(this).find(".article-title").css("color", "white");
    e.preventDefault();
  })

// makes an api call to get search endpoint
$("#search-field").change(function (e) {

  e.preventDefault();
});
