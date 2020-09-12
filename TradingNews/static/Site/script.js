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

// TODO: makes an api call to get search endpoint
$("#navbar-search-field").on("change input", function (e) {
  if ($(this).val() != ""){
    console.log($(this).val());
  }
  e.preventDefault();
});

