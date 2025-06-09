document.addEventListener('DOMContentLoaded', function() {
    // Load navbar
    const navbarContainer = document.getElementById('navbar-container');
    if (navbarContainer) {
        fetch('/components/navbar.html')
            .then(response => response.text())
            .then(data => {
                navbarContainer.innerHTML = data;
                
                // Initialize mobile menu toggle after navbar is loaded
                document.querySelector('.mobile-menu').addEventListener('click', function() {
                    document.querySelector('.nav-links').classList.toggle('show');
                });
                
                // Set active navigation link based on current page
                setActiveNavLink();
                
                // Mobile dropdown handling
                const dropdownToggle = document.querySelector('.dropdown-toggle');
                if (dropdownToggle && window.innerWidth < 768) {
                    dropdownToggle.addEventListener('click', function(e) {
                        e.preventDefault();
                        this.nextElementSibling.classList.toggle('show');
                    });
                }
            })
            .catch(error => console.error('Error loading navbar:', error));
    }
    
    // Load footer
    const footerContainer = document.getElementById('footer-container');
    if (footerContainer) {
        fetch('/components/footer.html')
            .then(response => response.text())
            .then(data => {
                footerContainer.innerHTML = data;
            })
            .catch(error => console.error('Error loading footer:', error));
    }
    
    // Function to set active navigation link based on current page
    function setActiveNavLink() {
        // Wait for navbar to load
        setTimeout(() => {
            const currentPage = window.location.pathname;
            const navLinks = document.querySelectorAll('.nav-links a');
            
            navLinks.forEach(link => {
                if (!link.classList.contains('dropdown-toggle')) {
                    link.classList.remove('active');
                    
                    // Match the href with current path
                    if (currentPage.includes(link.getAttribute('href').replace('#', ''))) {
                        link.classList.add('active');
                    }
                    
                    // Special case for homepage
                    if (currentPage === '/' && link.textContent.trim() === 'Home') {
                        link.classList.add('active');
                    }
                    
                    // Special case for žanr page
                    if (currentPage.includes('zanr') && link.parentElement.classList.contains('dropdown')) {
                        link.classList.add('active');
                    }
                }
            });
        }, 100);
    }
});
