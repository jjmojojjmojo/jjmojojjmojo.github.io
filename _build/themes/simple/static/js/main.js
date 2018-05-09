'use strict';

var toggle_explain = function(event){
    var button = $(this);
    console.log(button.data());
    var explain = button.parent();
    
    if (button.data().state === false){
        button.data({state: true});
        explain.find("div").show();
        button.attr("src", "/theme/icons/book-open.svg");
        button.attr("alt", "Click to hide explanation");
    } else {
        button.data({state: false});
        explain.find("div").hide();
        button.attr("src", "/theme/icons/book.svg");
        button.attr("alt", "Click to show explanation");
    }
};

var setup_explain_toggle_button = function(index){
    var explain = $(this);
    var button = $('<img class="button" src="/theme/icons/book.svg" />');
    button.data({state: false});
    button.click(toggle_explain);
    explain.append(button);
};

$(document).ready(function() {
    $(".explanation").each(setup_explain_toggle_button);
});