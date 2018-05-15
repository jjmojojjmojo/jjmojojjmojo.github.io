'use strict';

var save_settings = function() {
    localStorage.setItem('highlight-css', $("#choose-highlight-css").val());
    localStorage.setItem('explain-toggle', $("input[name='choose-explain-toggle']:checked").val());
};

var clear_settings = function() {
    var ok = confirm("Are you sure you want to clear all settings?");
    if(ok){
        localStorage.clear();
        $("#choose-highlight-css").val("/theme/css/syntax-solarized-light.css");
        test_css();
        $("input[name='choose-explain-toggle'][value='nothing']").prop("checked", true);
        $("input[name='choose-explain-toggle'][value='open']").prop("checked", false);
        $("input[name='choose-explain-toggle'][value='close']").prop("checked", false);
    }
};

var test_css = function() {
    var url = $("#choose-highlight-css").val();
    $("#highlight-css").attr("href", url);
}

$(document).ready(function() {
    // initial settings are pulled out of localstorage in main.js
    if(highlight_css_url){
        $("#choose-highlight-css").val(highlight_css_url);
    }
    if(explain_toggle){
        $("input[name='choose-explain-toggle'][value='"+explain_toggle+"']").attr("checked", true);
    }
    
    $("#choose-highlight-css").change(function(event){
         test_css();
    });
    
    $("button#save").click(function(){ save_settings(); });
    $("button#clear").click(function(){ clear_settings(); });
});