$(".article-img")
  .on('error', function() {
    $(this).remove()
  })

$(".article")
  .hover(function (){
    $(this).find(".article-title").css("color", "#4193c6")
  }, function(){
    $(this).find(".article-title").css("color", "white")
  })

