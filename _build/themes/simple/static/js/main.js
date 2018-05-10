'use strict';

var toggle_explain = function(event){
    var button = $(this);
    console.log(button.data());
    var explain = button.parent().parent();
    
    if (button.data().state === false){
        button.data({state: true});
        explain.find("*:not(:first-child)").show();
        button.attr("src", "/theme/icons/book-open.svg");
        button.attr("alt", "Click to hide explanation");
    } else {
        button.data({state: false});
        explain.find("*:not(:first-child)").hide();
        button.attr("src", "/theme/icons/book.svg");
        button.attr("alt", "Click to show explanation");
    }
    
    button.show();
};

var setup_explain_toggle_button = function(index){
    var explain_title = $(this);
    var button = $('<img class="button" src="/theme/icons/book.svg" />');
    button.data({state: false});
    button.click(toggle_explain);
    explain_title.append(button);
};

$(document).ready(function() {
    $(".explanation h1:first-child, "+
      ".explanation h2:first-child, "+
      ".explanation h3:first-child, "+  
      ".explanation h4:first-child, "+
      ".explanation h5:first-child, "+
      ".explanation h6:first-child").each(setup_explain_toggle_button);
});