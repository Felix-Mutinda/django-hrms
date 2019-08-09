$(function() {
    
    /* main-tabbed-nav (dashboards) - on click handler */
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
    
    /* activate the current nav-tab */
    function activateTab() {
        $('.main-tabbed-nav .nav .nav-item .nav-link').removeClass('active');
        $(this).addClass('active');
    }    
    
    /* bind events to main content tab menu links */
    const employeesTab = $('#employees-tab');
    const assetsTab = $('#assets-tab');
    const notificationsTab = $('#notifications-tab');
    const profileTab = $('#profile-tab');
    
    employeesTab.on('click', function(e) {
        activateTab();
        updateMainContent('/employer/employees');
    });
    
    assetsTab.on('click', function(e) {
        activateTab();
        updateMainContent('/employer/assets');
    });
    
    notificationsTab.on('click', function(e) {
        activateTab();
        updateMainContent('/employer/notifications');
    });
    
    profileTab.on('click', function(e) {
        activateTab();
        updateMainContent('/employer/profile');
    });
    
    /* display employees list on employer dashboard by default */
    updateMainContent('/employer/employees');
    
});





