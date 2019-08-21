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
    const employerEmployeesTab = $('#employer-employees-tab');
    const employerAssetsTab = $('#employer-assets-tab');
    const employerNotificationsTab = $('#employer-notifications-tab');
    const employerProfileTab = $('#employer-profile-tab');
    
    const employeeAssignedAssetsTab = $('#employee-assigned-assets-tab');
    const employeeProfileTab = $('#employee-profile-tab');
    
    employerEmployeesTab.on('click', function(e) {
        activateTab();
        updateMainContent('/employer/employees');
    });
    
    employerAssetsTab.on('click', function(e) {
        activateTab();
        updateMainContent('/employer/assets');
    });
    
    employerNotificationsTab.on('click', function(e) {
        activateTab();
        updateMainContent('/employer/notifications');
    });
    
    employerProfileTab.on('click', function(e) {
        activateTab();
        updateMainContent('/employer/profile');
    });
    
    employeeAssignedAssetsTab.on('click', function(e) {
        activateTab();
        updateMainContent('/employee/assigned-assets');
    });
    
    employeeProfileTab.on('click', function(e) {
        activateTab();
        updateMainContent('/employee/profile');
    });
    
    /* display employee/employer dashboard by default */
    if ($(location).attr('pathname') == '/employer/dashboard/') {
        updateMainContent('/employer/employees');
    } else if ($(location).attr('pathname') == '/employee/dashboard/') { 
        updateMainContent('/employee/assigned-assets');
    }
    
    
    
});





