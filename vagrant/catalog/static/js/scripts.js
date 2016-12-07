(function($){
  $(function(){

  $('.datepicker').pickadate({
    selectMonths: true, // Creates a dropdown to control month
    selectYears: 10, // Creates a dropdown of 15 years to control year
    format: 'd mmmm, yyyy' // format for display
  });

  }); // end of document ready
})(jQuery); // end of jQuery name space