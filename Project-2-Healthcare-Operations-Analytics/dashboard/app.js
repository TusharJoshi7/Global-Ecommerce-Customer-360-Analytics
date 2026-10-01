document.addEventListener('DOMContentLoaded', async () => {
    try {
        const response = await fetch('data.json');
        const data = await response.json();
        
        // Populate KPIs
        document.getElementById('totalAdmissions').innerText = data.summary.total_admissions.toLocaleString();
        document.getElementById('avgWaitTime').innerText = `${data.summary.avg_wait_time_min} mins`;
        document.getElementById('avgLOS').innerText = `${data.summary.avg_length_of_stay_days} days`;
        document.getElementById('readmissionRate').innerText = `${data.summary.readmission_rate_pct}%`;
        document.getElementById('totalCost').innerText = `$${(data.summary.total_treatment_cost / 1e6).toFixed(2)}M`;
        
        // Chart defaults
        Chart.defaults.color = '#94a3b8';
        Chart.defaults.font.family = "'Plus Jakarta Sans', sans-serif";
        
        // 1. Monthly Admissions Trajectory Chart
        const months = data.monthly_trend.map(d => d.year_month);
        const admissions = data.monthly_trend.map(d => d.admissions);
        const waitTimes = data.monthly_trend.map(d => d.avg_wait);
        
        new Chart(document.getElementById('monthlyTrendChart'), {
            type: 'line',
            data: {
                labels: months,
                datasets: [
                    {
                        label: 'Admissions Volume',
                        data: admissions,
                        borderColor: '#38bdf8',
                        backgroundColor: 'rgba(56, 189, 248, 0.1)',
                        fill: true,
                        tension: 0.3,
                        yAxisID: 'y'
                    },
                    {
                        label: 'Avg Wait Time (Mins)',
                        data: waitTimes,
                        borderColor: '#f97316',
                        borderDash: [5, 5],
                        tension: 0.3,
                        yAxisID: 'y1'
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        grid: { color: '#23314d' },
                        title: { display: true, text: 'Admissions' }
                    },
                    y1: {
                        position: 'right',
                        grid: { drawOnChartArea: false },
                        title: { display: true, text: 'Wait Time (Min)' }
                    },
                    x: { grid: { color: '#23314d' } }
                }
            }
        });
        
        // 2. Triage Breakdown Chart
        const triageLabels = Object.keys(data.triage_distribution);
        const triageValues = Object.values(data.triage_distribution);
        
        new Chart(document.getElementById('triageChart'), {
            type: 'doughnut',
            data: {
                labels: triageLabels,
                datasets: [{
                    data: triageValues,
                    backgroundColor: ['#ef4444', '#f97316', '#eab308', '#38bdf8', '#22c55e']
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { position: 'bottom' }
                }
            }
        });
        
        // 3. Department Wait Times Chart
        const depts = data.department_kpis.map(d => d.department);
        const deptWaits = data.department_kpis.map(d => d.avg_wait_time_min);
        
        new Chart(document.getElementById('deptChart'), {
            type: 'bar',
            data: {
                labels: depts,
                datasets: [{
                    label: 'Avg Wait Time (Min)',
                    data: deptWaits,
                    backgroundColor: '#a855f7',
                    borderRadius: 6
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: { grid: { color: '#23314d' } },
                    x: { grid: { color: '#23314d' } }
                }
            }
        });
        
        // 4. Readmission by Age Chart
        const ageGroups = Object.keys(data.readmission_by_age);
        const readmitRates = Object.values(data.readmission_by_age);
        
        new Chart(document.getElementById('readmitAgeChart'), {
            type: 'bar',
            data: {
                labels: ageGroups,
                datasets: [{
                    label: 'Readmission Rate (%)',
                    data: readmitRates,
                    backgroundColor: '#ef4444',
                    borderRadius: 6
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: { grid: { color: '#23314d' }, ticks: { callback: v => v + '%' } },
                    x: { grid: { color: '#23314d' } }
                }
            }
        });
        
        // 5. Populate Table
        const tbody = document.getElementById('patientTableBody');
        tbody.innerHTML = '';
        data.top_cost_admissions.forEach(p => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td><strong>${p.patient_id}</strong></td>
                <td>${p.age}</td>
                <td>${p.gender}</td>
                <td>${p.department}</td>
                <td>Level ${p.triage_level}</td>
                <td>${p.length_of_stay_days}</td>
                <td>$${p.treatment_cost.toLocaleString()}</td>
                <td><span class="badge-flag ${p.readmission_30d === 1 ? 'badge-yes' : 'badge-no'}">${p.readmission_30d === 1 ? 'Yes (High Risk)' : 'No'}</span></td>
            `;
            tbody.appendChild(tr);
        });
        
    } catch (err) {
        console.error('Error loading dashboard data:', err);
    }
});
