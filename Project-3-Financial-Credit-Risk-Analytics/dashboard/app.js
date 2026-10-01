document.addEventListener('DOMContentLoaded', async () => {
    try {
        const response = await fetch('data.json');
        const data = await response.json();
        
        // Populate KPIs
        document.getElementById('totalFunded').innerText = `$${(data.summary.total_funded_volume / 1e6).toFixed(2)}M`;
        document.getElementById('totalOutstanding').innerText = `$${(data.summary.total_outstanding_balance / 1e6).toFixed(2)}M`;
        document.getElementById('overallDefaultRate').innerText = `${data.summary.overall_default_rate_pct}%`;
        document.getElementById('avgInterestRate').innerText = `${data.summary.avg_interest_rate_pct}%`;
        document.getElementById('avgFico').innerText = data.summary.avg_fico_score;
        
        // Chart Defaults
        Chart.defaults.color = '#9ca3af';
        Chart.defaults.font.family = "'Plus Jakarta Sans', sans-serif";
        
        // 1. Vintage Trend Chart
        const months = data.vintage_trend.map(d => d.issue_year_month);
        const volumes = data.vintage_trend.map(d => d.total_disbursed / 1e3);
        const defaults = data.vintage_trend.map(d => d.default_rate);
        
        new Chart(document.getElementById('vintageTrendChart'), {
            type: 'line',
            data: {
                labels: months,
                datasets: [
                    {
                        label: 'Disbursed Volume ($K)',
                        data: volumes,
                        borderColor: '#3b82f6',
                        backgroundColor: 'rgba(59, 130, 246, 0.1)',
                        fill: true,
                        tension: 0.3,
                        yAxisID: 'y'
                    },
                    {
                        label: 'Default Rate (%)',
                        data: defaults,
                        borderColor: '#ef4444',
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
                    y: { grid: { color: '#1f2937' }, title: { display: true, text: 'Volume ($K)' } },
                    y1: { position: 'right', grid: { drawOnChartArea: false }, title: { display: true, text: 'Default %' } },
                    x: { grid: { color: '#1f2937' } }
                }
            }
        });
        
        // 2. Grade Default Chart
        const grades = Object.keys(data.grade_breakdown);
        const gradeDefaults = grades.map(g => data.grade_breakdown[g].default_rate);
        
        new Chart(document.getElementById('gradeChart'), {
            type: 'bar',
            data: {
                labels: grades.map(g => `Grade ${g}`),
                datasets: [{
                    label: 'Default Rate (%)',
                    data: gradeDefaults,
                    backgroundColor: ['#10b981', '#3b82f6', '#f59e0b', '#8b5cf6', '#ef4444'],
                    borderRadius: 6
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: { grid: { color: '#1f2937' }, ticks: { callback: v => v + '%' } },
                    x: { grid: { color: '#1f2937' } }
                }
            }
        });
        
        // 3. FICO Tier Chart
        const ficoTiers = Object.keys(data.fico_breakdown);
        const ficoDefaults = ficoTiers.map(f => data.fico_breakdown[f].default_rate);
        
        new Chart(document.getElementById('ficoChart'), {
            type: 'bar',
            data: {
                labels: ficoTiers,
                datasets: [{
                    label: 'Default Rate (%)',
                    data: ficoDefaults,
                    backgroundColor: '#8b5cf6',
                    borderRadius: 6
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: { grid: { color: '#1f2937' }, ticks: { callback: v => v + '%' } },
                    x: { grid: { color: '#1f2937' } }
                }
            }
        });
        
        // 4. Populate Table
        const tbody = document.getElementById('loanTableBody');
        tbody.innerHTML = '';
        data.high_risk_loans.forEach(l => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td><strong>${l.loan_id}</strong></td>
                <td>${l.borrower_id}</td>
                <td>Grade ${l.grade}</td>
                <td>$${l.loan_amount.toLocaleString()}</td>
                <td>${l.interest_rate}%</td>
                <td>${l.credit_score}</td>
                <td>${l.dti_ratio}%</td>
                <td><span class="badge-status-tag">${l.loan_status}</span></td>
                <td>$${l.outstanding_balance.toLocaleString()}</td>
            `;
            tbody.appendChild(tr);
        });
        
    } catch (err) {
        console.error('Error loading credit risk data:', err);
    }
});
