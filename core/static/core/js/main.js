$(function() {
    
    /* main-content-tabbed-nav (dashboards) - on click handler */
    function updateMainContent(url) { // fetch url and display on .main-content
        let mainContent = $('.main-content .card-body');
        
        fetch(url)
        .then((data) =>  data.text())
        .then(function(data) {
            /* replace .main-content with retrieved data. */
            mainContent.html(data);
        })
        .catch(function(error) {
            console.log(error);
        });
    }
    
    /* bind events to main content tab menu links */
    const employeesTab = $('#employees-tab');
    
    employeesTab.on('click', function(e) {
        updateMainContent('/employer/employees');
    });
    
});