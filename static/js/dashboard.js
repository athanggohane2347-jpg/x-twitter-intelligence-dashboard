(function () {
    const data = window.dashboardData || {};

    function chartColors() {
        return {
            blue: "#2563eb",
            cyan: "#0ea5e9",
            green: "#16a34a",
            red: "#dc2626",
            amber: "#f59e0b",
            grid: "rgba(148, 163, 184, 0.24)",
        };
    }

    function createSentimentPie() {
        const element = document.getElementById("sentimentPie");
        if (!element) return;

        const colors = chartColors();
        new Chart(element, {
            type: "doughnut",
            data: {
                labels: ["Positive", "Negative", "Neutral"],
                datasets: [{
                    data: data.sentimentCounts || [0, 0, 0],
                    backgroundColor: [colors.green, colors.red, colors.amber],
                    borderWidth: 0,
                }],
            },
            options: {
                responsive: true,
                cutout: "68%",
                plugins: {
                    legend: {
                        position: "bottom",
                    },
                },
            },
        });
    }

    function createSentimentLine() {
        const element = document.getElementById("sentimentLine");
        if (!element) return;

        const colors = chartColors();
        const scores = data.sentimentScores || [];

        new Chart(element, {
            type: "line",
            data: {
                labels: scores.map((_, index) => `Post ${index + 1}`),
                datasets: [{
                    label: "Sentiment Score",
                    data: scores,
                    borderColor: colors.blue,
                    backgroundColor: "rgba(37, 99, 235, 0.16)",
                    tension: 0.42,
                    fill: true,
                    pointRadius: 4,
                }],
            },
            options: {
                responsive: true,
                scales: {
                    y: {
                        min: -1,
                        max: 1,
                        grid: { color: colors.grid },
                    },
                    x: {
                        grid: { display: false },
                    },
                },
            },
        });
    }

    function createHashtagChart() {
        const element = document.getElementById("hashtagChart");
        if (!element) return;

        const colors = chartColors();
        const hashtags = data.hashtags || [];

        new Chart(element, {
            type: "bar",
            data: {
                labels: hashtags.map((item) => item.tag),
                datasets: [{
                    label: "Mentions",
                    data: hashtags.map((item) => item.count),
                    backgroundColor: colors.cyan,
                    borderRadius: 10,
                }],
            },
            options: {
                responsive: true,
                plugins: {
                    legend: { display: false },
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: { precision: 0 },
                        grid: { color: colors.grid },
                    },
                    x: {
                        grid: { display: false },
                    },
                },
            },
        });
    }

    createSentimentPie();
    createSentimentLine();
    createHashtagChart();
})();
