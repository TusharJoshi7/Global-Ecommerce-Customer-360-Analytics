let dashboardData = null;
let trendChart = null;
let segmentChart = null;
let regionChart = null;
let categoryChart = null;

document.addEventListener("DOMContentLoaded", () => {
  // Try fetching data.json from relative path or dashboard subfolder
  const jsonPath = window.location.pathname.endsWith("/dashboard/") || window.location.pathname.endsWith("/dashboard/index.html")
    ? "data.json"
    : "dashboard/data.json";

  fetch(jsonPath)
    .catch(() => fetch("data.json"))
    .then(res => res.json())
    .then(data => {
      dashboardData = data;
      renderKPIs(data.kpis);
      initCharts(data);
      renderTable(data.top_customers);
    })
    .catch(err => {
      console.error("Error loading dashboard data:", err);
    });
});

function renderKPIs(kpis) {
  document.getElementById("kpi-revenue").innerText = `$${kpis.total_revenue.toLocaleString()}`;
  document.getElementById("kpi-orders").innerText = kpis.total_orders.toLocaleString();
  document.getElementById("kpi-customers").innerText = kpis.total_customers.toLocaleString();
  document.getElementById("kpi-aov").innerText = `$${kpis.aov.toFixed(2)}`;
  document.getElementById("kpi-clv").innerText = `$${kpis.avg_clv.toFixed(2)}`;
  document.getElementById("kpi-churn").innerText = `${kpis.churn_rate_pct}%`;
}

function initCharts(data) {
  // 1. Monthly Revenue Trend Chart
  const trendCtx = document.getElementById("chart-trend").getContext("2d");
  const labels = data.monthly_trends.map(d => d.year_month);
  const revenues = data.monthly_trends.map(d => d.revenue);

  trendChart = new Chart(trendCtx, {
    type: "line",
    data: {
      labels: labels,
      datasets: [{
        label: "Monthly Revenue ($)",
        data: revenues,
        borderColor: "#38bdf8",
        backgroundColor: "rgba(56, 189, 248, 0.1)",
        fill: true,
        tension: 0.3,
        borderWidth: 2,
        pointRadius: 4,
        pointBackgroundColor: "#38bdf8"
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { labels: { color: "#f8fafc" } }
      },
      scales: {
        x: { ticks: { color: "#94a3b8" }, grid: { color: "rgba(255,255,255,0.05)" } },
        y: { ticks: { color: "#94a3b8" }, grid: { color: "rgba(255,255,255,0.05)" } }
      }
    }
  });

  // 2. Customer RFM Segment Chart
  const segCtx = document.getElementById("chart-segments").getContext("2d");
  const segLabels = Object.keys(data.customer_segments);
  const segValues = Object.values(data.customer_segments);

  segmentChart = new Chart(segCtx, {
    type: "doughnut",
    data: {
      labels: segLabels,
      datasets: [{
        data: segValues,
        backgroundColor: [
          "#34d399", "#38bdf8", "#818cf8", "#fbbf24", "#f43f5e", "#a78bfa", "#64748b"
        ],
        borderWidth: 0
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { position: "right", labels: { color: "#f8fafc", font: { size: 11 } } }
      }
    }
  });

  // 3. Regional Revenue Breakdown Chart
  const regCtx = document.getElementById("chart-regions").getContext("2d");
  const regLabels = Object.keys(data.regional_revenue);
  const regValues = Object.values(data.regional_revenue);

  regionChart = new Chart(regCtx, {
    type: "bar",
    data: {
      labels: regLabels,
      datasets: [{
        label: "Revenue ($)",
        data: regValues,
        backgroundColor: "#818cf8",
        borderRadius: 6
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: { legend: { display: false } },
      scales: {
        x: { ticks: { color: "#94a3b8" }, grid: { display: false } },
        y: { ticks: { color: "#94a3b8" }, grid: { color: "rgba(255,255,255,0.05)" } }
      }
    }
  });

  // 4. Product Category Revenue Chart
  const catCtx = document.getElementById("chart-categories").getContext("2d");
  const catLabels = Object.keys(data.category_revenue);
  const catValues = Object.values(data.category_revenue);

  categoryChart = new Chart(catCtx, {
    type: "bar",
    data: {
      labels: catLabels,
      datasets: [{
        label: "Category Revenue ($)",
        data: catValues,
        backgroundColor: "#34d399",
        borderRadius: 6
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      indexAxis: 'y',
      plugins: { legend: { display: false } },
      scales: {
        x: { ticks: { color: "#94a3b8" }, grid: { color: "rgba(255,255,255,0.05)" } },
        y: { ticks: { color: "#94a3b8" }, grid: { display: false } }
      }
    }
  });
}

function renderTable(topCustomers) {
  const tbody = document.getElementById("table-body");
  tbody.innerHTML = "";

  topCustomers.forEach(cust => {
    let tagClass = "tag-loyal";
    if (cust.Customer_Segment.includes("Champions")) tagClass = "tag-champions";
    else if (cust.Customer_Segment.includes("Potential")) tagClass = "tag-potential";
    else if (cust.Customer_Segment.includes("At Risk")) tagClass = "tag-atrisk";
    else if (cust.Customer_Segment.includes("Lost")) tagClass = "tag-lost";

    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td><strong>${cust.customer_id}</strong></td>
      <td>${cust.region}</td>
      <td>${cust.frequency} orders</td>
      <td>$${cust.monetary.toLocaleString(undefined, {minimumFractionDigits: 2})}</td>
      <td><span class="tag ${tagClass}">${cust.Customer_Segment}</span></td>
    `;
    tbody.appendChild(tr);
  });
}
