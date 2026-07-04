// MetaGuard — admin dashboard with live polling
(function () {
  const POLL_MS = 3000;

  const palette = {
    toxic: "rgba(255, 107, 107, 0.85)",
    phish: "rgba(244, 208, 63, 0.85)",
    grid:  "rgba(255,255,255,0.06)",
    text:  "#94a3b8",
  };

  Chart.defaults.color = palette.text;
  Chart.defaults.borderColor = palette.grid;

  let timeChart = null;
  let typeChart = null;

  function escapeHtml(s) {
    return String(s ?? "")
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  function flashIfChanged(el, newValue) {
    if (!el) return;
    const oldValue = el.textContent.trim();
    const newText = String(newValue);
    if (oldValue !== newText) {
      el.textContent = newText;
      el.classList.remove("flash");
      void el.offsetWidth;        // restart animation
      el.classList.add("flash");
    }
  }

  function updateCards(cards) {
    if (!cards) return;
    document.querySelectorAll("[data-stat]").forEach((el) => {
      const key = el.dataset.stat;
      if (key in cards) flashIfChanged(el, cards[key]);
    });
  }

  function renderRecentThreats(rows) {
    const tbody = document.getElementById("recent-threats-body");
    if (!tbody) return;

    if (!rows || rows.length === 0) {
      tbody.innerHTML =
        '<tr><td colspan="5" class="text-secondary text-center py-4">' +
        "No threats detected yet — the metaverse is calm." +
        "</td></tr>";
      return;
    }

    tbody.innerHTML = rows.map((t) => `
      <tr>
        <td class="text-secondary">${escapeHtml(t.when)}</td>
        <td><strong>${escapeHtml(t.username)}</strong></td>
        <td><span class="threat-type-${escapeHtml(t.type)}">${escapeHtml(t.type)}</span></td>
        <td>${Number(t.score).toFixed(2)}</td>
        <td class="text-truncate" style="max-width: 420px;">${escapeHtml(t.payload)}</td>
      </tr>
    `).join("");
  }

  function buildTimeChart(data) {
    const el = document.getElementById("threats-time-chart");
    if (!el) return null;
    return new Chart(el, {
      type: "line",
      data: {
        labels: data.labels,
        datasets: [
          {
            label: "Toxicity",
            data: data.toxicity,
            borderColor: palette.toxic,
            backgroundColor: palette.toxic,
            tension: 0.3,
            fill: false,
          },
          {
            label: "Phishing",
            data: data.phishing,
            borderColor: palette.phish,
            backgroundColor: palette.phish,
            tension: 0.3,
            fill: false,
          },
        ],
      },
      options: {
        responsive: true,
        animation: { duration: 400 },
        plugins: { legend: { position: "bottom" } },
        scales: {
          x: { grid: { color: palette.grid } },
          y: { grid: { color: palette.grid }, beginAtZero: true, ticks: { precision: 0 } },
        },
      },
    });
  }

  function buildTypeChart(data) {
    const el = document.getElementById("threats-type-chart");
    if (!el) return null;
    return new Chart(el, {
      type: "doughnut",
      data: {
        labels: ["Toxicity", "Phishing"],
        datasets: [{
          data: [data.type_counts.toxicity, data.type_counts.phishing],
          backgroundColor: [palette.toxic, palette.phish],
          borderColor: "#0d1320",
          borderWidth: 2,
        }],
      },
      options: {
        animation: { duration: 400 },
        plugins: { legend: { position: "bottom" } },
      },
    });
  }

  function updateCharts(data) {
    if (timeChart) {
      timeChart.data.labels = data.labels;
      timeChart.data.datasets[0].data = data.toxicity;
      timeChart.data.datasets[1].data = data.phishing;
      timeChart.update("none");
    }
    if (typeChart) {
      typeChart.data.datasets[0].data = [
        data.type_counts.toxicity,
        data.type_counts.phishing,
      ];
      typeChart.update("none");
    }
  }

  function setStatus(ok, time) {
    const el = document.getElementById("last-updated");
    if (!el) return;
    if (ok) {
      el.textContent = "· updated " + time;
      el.classList.remove("text-danger");
    } else {
      el.textContent = "· offline (will retry)";
      el.classList.add("text-danger");
    }
  }

  async function tick() {
    try {
      const r = await fetch("/admin/api/stats", { cache: "no-store" });
      if (!r.ok) throw new Error("http " + r.status);
      const data = await r.json();
      updateCards(data.cards);
      updateCharts(data);
      renderRecentThreats(data.recent);
      setStatus(true, data.server_time || "");
    } catch (e) {
      setStatus(false);
    }
  }

  async function init() {
    try {
      const r = await fetch("/admin/api/stats", { cache: "no-store" });
      const data = await r.json();
      timeChart = buildTimeChart(data);
      typeChart = buildTypeChart(data);
      updateCards(data.cards);
      renderRecentThreats(data.recent);
      setStatus(true, data.server_time || "");
    } catch (e) {
      setStatus(false);
    }
    setInterval(tick, POLL_MS);
  }

  init();
})();
