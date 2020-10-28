$("#navbar-search-field").click(function(e) {
  $(this).parent().addClass("search-field-container-show");
  $("#search-field-content").addClass("active")
  e.stopPropagation();
});

$(document).click(function () {
  $("#navbar-search-field-container").removeClass("search-field-container-show");
  $("#search-field-content").removeClass("active");
});


// input: none
// output: none
// description: event handlers that makes a call to the back-end everytime the input changes. 
//   adds elements of the response to the best matches list under the navbar
$("#navbar-search-field").on("change input", function (e) {
  if ($(this).val() != ""){
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
        console.log(matches);
        // clears matches
        content.empty();
        
        for (let x of matches){
          if(x['3. type'] == "Equity"){
            content.append(`
            <a href="http://127.0.0.1:8000/company/${x['1. symbol']}" class="search-field-content-element">
              <div class="search-element-symbol">${x['1. symbol']}</div>
              <div class="search-element-name">${x['2. name']}</div>
              <div class="search-element-type">${x['3. type']}</div>
            </a>
          `);
          }
        }
      })
      .catch(err => {
        console.log(err);
      });
  }
  e.preventDefault();
});

