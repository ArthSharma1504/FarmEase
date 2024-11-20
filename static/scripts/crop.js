// Fetch data from JSON file and populate the crop pricing table
fetch('/static/data/crop_pricing.json')
    .then(response => response.json())
    .then(data => {
        console.log('Fetched data:', data);  // Log the data to inspect its structure

        const pricingTableBody = document.querySelector('#pricing-table tbody');
        
        // Extract prices for plotting
        const cropData = {};
        const labels = ["2019-20", "2020-21", "2021-22", "2022-23", "2023-24", "2024-25"];
        data.data.forEach(row => {
            const crop = row[2]; // Extract commodity (e.g., "Paddy")
            const prices = row.slice(4); // Extract prices for each year
            
            if (!cropData[crop]) {
                cropData[crop] = [];
            }
            cropData[crop].push(prices);
            
            // Add rows to the table
            const tableRow = document.createElement('tr');
            row.forEach(cell => {
                const tableCell = document.createElement('td');
                tableCell.textContent = cell;
                tableRow.appendChild(tableCell);
            });
            pricingTableBody.appendChild(tableRow);
        });

        // Plot graph for a specific crop (e.g., "Paddy")
        const selectedCrop = "Paddy";  // You can make this dynamic based on user selection
        const prices = cropData[selectedCrop][0]; // Assuming only one variety of this crop

        // Create chart with Chart.js
        const ctx = document.getElementById('price-chart').getContext('2d');
        const priceChart = new Chart(ctx, {
            type: 'line', // Line chart
            data: {
                labels: labels, // Years
                datasets: [{
                    label: `${selectedCrop} Price (₹ per Quintal)`, // Label for the line
                    data: prices, // Price data for each year
                    fill: false,
                    borderColor: 'rgba(75, 192, 192, 1)', // Line color
                    tension: 0.1
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: false
                    }
                }
            }
        });
    })
    .catch(error => {
        console.error('Error fetching crop pricing data:', error);
    });
