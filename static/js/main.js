document.addEventListener('DOMContentLoaded', function() {
    const menuToggle = document.getElementById('menu-toggle');
    const sidebar = document.getElementById('sidebar');
    const sidebarConnectBtn = document.querySelector('.sidebar-connect-btn');

    // Function to toggle sidebar visibility
    function toggleSidebar() {
        sidebar.classList.toggle('active');
    }

    // Toggle sidebar when menu toggle button is clicked
    menuToggle.addEventListener('click', function(event) {
        event.stopPropagation(); // Prevents click from propagating to document click listener
        toggleSidebar();
    });

    // Toggle sidebar when "Let's Connect" button in sidebar is clicked
    sidebarConnectBtn.addEventListener('click', function(event) {
        event.stopPropagation(); // Prevents click from propagating to document click listener
        toggleSidebar();
    });

    // Close sidebar when clicking anywhere outside of it
    document.addEventListener('click', function(event) {
        if (!sidebar.contains(event.target) && event.target !== menuToggle) {
            sidebar.classList.remove('active');
        }
    });

    // Prevent clicks within the sidebar from closing it
    sidebar.addEventListener('click', function(event) {
        event.stopPropagation(); // Prevents click from propagating to document click listener
    });
});



document.getElementById("menu-toggle").addEventListener("click", function() {
    document.getElementById("sidebar").classList.toggle("active");
});
