'use strict';
var explain_toggle = localStorage.getItem('explain-toggle');
var highlight_css_url = localStorage.getItem("highlight-css");

var last_explain_id = 0;

var show_explain = function(button){
    var explain = button.parent().parent();
    
    button.data({
        state: true,
    });
    explain.find("*:not(:first-child)").show();
    button.attr("src", "/theme/icons/book-open.svg");
    button.attr("alt", "Click to hide explanation");
    localStorage.setItem('explain-state-'+button.data().id, true);
};

var hide_explain = function(button){
    var explain = button.parent().parent();
    
    button.data({state: false});
    explain.find("*:not(:first-child)").hide();
    button.attr("src", "/theme/icons/book.svg");
    button.attr("alt", "Click to show explanation");
    
    localStorage.setItem('explain-state-'+button.data().id, false);
};

var toggle_explain = function(event){
    var button = $(this);
    
    console.log(button.data());
    var explain = button.parent().parent();
    
    if (button.data().state === false){
        show_explain(button);
    } else {
        hide_explain(button);
    }
};

var setup_explain_toggle_button = function(index){
    var explain_title = $(this);
    var button = $('<img class="button" src="/theme/icons/book.svg" />');
    explain_title.append(button);
    
    button.data({
        state: false,
        id: last_explain_id++
    });
    
    button.click(toggle_explain);
    
    var previous_state = localStorage.getItem('explain-state-'+button.data().id);
    console.log("Previous state: "+previous_state);
    console.log("Toggle: "+explain_toggle);
    switch (explain_toggle) {
        case 'open': show_explain(button);
                     break;
        case 'close': hide_explain(button);
                      break;
        default: 
            if(previous_state !== null){
                console.log("Prev State: "+previous_state);
                if (previous_state == "true"){
                    console.log("Showing");
                    show_explain(button);
                } else {
                    console.log("Hiding");
                    hide_explain(button);
                }
            }
            break;
    }
    
    button.show();
};

$(document).ready(function() {
    $(".explanation h1:first-child, "+
      ".explanation h2:first-child, "+
      ".explanation h3:first-child, "+  
      ".explanation h4:first-child, "+
      ".explanation h5:first-child, "+
      ".explanation h6:first-child").each(setup_explain_toggle_button);
      
    if(highlight_css_url){
        $("#highlight-css").attr("href", highlight_css_url);
    }
});