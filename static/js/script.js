// Main JavaScript file for Eco Volunteers Website

document.addEventListener('DOMContentLoaded', function() {
    // Initialize Bootstrap tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize Bootstrap popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Navbar scrolled effect
    const navbar = document.querySelector('.navbar');
    if (navbar) {
        window.addEventListener('scroll', function() {
            if (window.scrollY > 50) {
                navbar.classList.add('navbar-scrolled');
            } else {
                navbar.classList.remove('navbar-scrolled');
            }
        });
    }

    // Auto-dismiss alerts after 5 seconds
    setTimeout(function() {
        const alerts = document.querySelectorAll('.alert:not(.alert-persistent)');
        alerts.forEach(function(alert) {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);

    // Camp search functionality
    const campSearchInput = document.getElementById('camp-search');
    if (campSearchInput) {
        campSearchInput.addEventListener('input', function() {
            const searchTerm = this.value.toLowerCase();
            const campCards = document.querySelectorAll('.camp-card');
            
            campCards.forEach(function(card) {
                const campName = card.querySelector('.card-title').textContent.toLowerCase();
                const campLocation = card.querySelector('.camp-location').textContent.toLowerCase();
                const campDescription = card.querySelector('.card-text').textContent.toLowerCase();
                
                if (campName.includes(searchTerm) || 
                    campLocation.includes(searchTerm) || 
                    campDescription.includes(searchTerm)) {
                    card.style.display = '';
                } else {
                    card.style.display = 'none';
                }
            });
        });
    }

    // Camp filter functionality
    const campFilterSelect = document.getElementById('camp-filter');
    if (campFilterSelect) {
        campFilterSelect.addEventListener('change', function() {
            const filterValue = this.value;
            const campCards = document.querySelectorAll('.camp-card');
            
            if (filterValue === 'all') {
                campCards.forEach(card => card.style.display = '');
                return;
            }
            
            campCards.forEach(function(card) {
                if (filterValue === 'upcoming' && card.dataset.status === 'upcoming') {
                    card.style.display = '';
                } else if (filterValue === 'past' && card.dataset.status === 'past') {
                    card.style.display = '';
                } else {
                    card.style.display = 'none';
                }
            });
        });
    }

    // Form validation for camp application
    const applicationForm = document.getElementById('camp-application-form');
    if (applicationForm) {
        applicationForm.addEventListener('submit', function(event) {
            if (!applicationForm.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            
            applicationForm.classList.add('was-validated');
        });
    }

    // Date picker enhancements
    const datePickers = document.querySelectorAll('input[type="date"]');
    datePickers.forEach(function(picker) {
        // Set min date to today for future date inputs
        if (picker.classList.contains('future-date')) {
            const today = new Date().toISOString().split('T')[0];
            picker.setAttribute('min', today);
        }
    });

    // Admin dashboard charts setup (if Chart.js is loaded)
    if (typeof Chart !== 'undefined' && document.getElementById('applicationsChart')) {
        setupDashboardCharts();
    }
});

// Function to setup admin dashboard charts
function setupDashboardCharts() {
    // Applications by status chart
    const applicationCtx = document.getElementById('applicationsChart').getContext('2d');
    const applicationsData = JSON.parse(document.getElementById('applicationsChart').dataset.chartData);
    
    new Chart(applicationCtx, {
        type: 'pie',
        data: {
            labels: Object.keys(applicationsData),
            datasets: [{
                data: Object.values(applicationsData),
                backgroundColor: [
                    '#ffc107', // Pending (yellow)
                    '#28a745', // Approved (green)
                    '#dc3545', // Rejected (red)
                    '#17a2b8'  // Waitlisted (blue)
                ],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'bottom',
                }
            }
        }
    });
    
    // Volunteers over time chart
    if (document.getElementById('volunteersChart')) {
        const volunteersCtx = document.getElementById('volunteersChart').getContext('2d');
        const volunteersData = JSON.parse(document.getElementById('volunteersChart').dataset.chartData);
        
        new Chart(volunteersCtx, {
            type: 'line',
            data: {
                labels: volunteersData.labels,
                datasets: [{
                    label: 'New Volunteers',
                    data: volunteersData.data,
                    borderColor: '#4CAF50',
                    backgroundColor: 'rgba(76, 175, 80, 0.1)',
                    borderWidth: 2,
                    tension: 0.1,
                    fill: true
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        display: false
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            precision: 0
                        }
                    }
                }
            }
        });
    }
}

// Function to confirm delete actions
function confirmDelete(formId, itemName) {
    if (confirm(`Are you sure you want to delete ${itemName}? This action cannot be undone.`)) {
        document.getElementById(formId).submit();
    }
    return false;
}

// Function to preview image before upload
function previewImage(input, previewId) {
    if (input.files && input.files[0]) {
        const reader = new FileReader();
        
        reader.onload = function(e) {
            const previewElement = document.getElementById(previewId);
            previewElement.src = e.target.result;
            previewElement.style.display = 'block';
        }
        
        reader.readAsDataURL(input.files[0]);
    }
}
