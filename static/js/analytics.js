// Example data for visualization
const ageData = [10, 20, 30, 40, 15]; // Age groups
const genderData = [60, 40]; // Male/Female distribution
const appointmentTrendsData = [5, 10, 15, 20, 25]; // Appointments over time

// Age Distribution Chart
const ageCtx = document.getElementById('ageChart').getContext('2d');
new Chart(ageCtx, {
    type: 'bar',
    data: {
        labels: ['0-18', '19-35', '36-50', '51-65', '65+'],
        datasets: [{
            label: 'Age Distribution',
            data: ageData,
            backgroundColor: 'rgba(75, 192, 192, 0.6)',
            borderColor: 'rgba(75, 192, 192, 1)',
            borderWidth: 1
        }]
    },
    options: {
        responsive: true,
        scales: {
            y: { beginAtZero: true }
        }
    }
});

// Gender Distribution Chart
const genderCtx = document.getElementById('genderChart').getContext('2d');
new Chart(genderCtx, {
    type: 'pie',
    data: {
        labels: ['Male', 'Female'],
        datasets: [{
            label: 'Gender Distribution',
            data: genderData,
            backgroundColor: ['#4caf50', '#2196f3']
        }]
    },
    options: {
        responsive: true
    }
});

// Appointment Trends Chart
const trendsCtx = document.getElementById('appointmentTrendsChart').getContext('2d');
new Chart(trendsCtx, {
    type: 'line',
    data: {
        labels: ['Week 1', 'Week 2', 'Week 3', 'Week 4', 'Week 5'],
        datasets: [{
            label: 'Appointment Trends',
            data: appointmentTrendsData,
            borderColor: 'rgba(255, 99, 132, 1)',
            borderWidth: 2,
            fill: false
        }]
    },
    options: {
        responsive: true,
        scales: {
            y: { beginAtZero: true }
        }
    }
});
