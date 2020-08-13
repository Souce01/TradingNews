$('.chev').on('click', function(ev) {
  ev.preventDefault();
  $(this).toggleClass('chevron--down chevron--up');
  
  // There's probably a better way to do this
  $(this).parent().parent().children('p').toggleClass('article-description-show article-description');
})