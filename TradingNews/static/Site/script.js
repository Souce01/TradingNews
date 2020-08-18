$(".article-img")
  .on('error', function() {
    $(this).remove()
  })