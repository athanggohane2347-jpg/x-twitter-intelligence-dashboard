(function () {
    const root = document.documentElement;
    const savedTheme = localStorage.getItem("theme") || "light";
    root.setAttribute("data-theme", savedTheme);

    function toggleTheme() {
        const nextTheme = root.getAttribute("data-theme") === "dark" ? "light" : "dark";
        root.setAttribute("data-theme", nextTheme);
        localStorage.setItem("theme", nextTheme);
    }

    document.addEventListener("click", function (event) {
        const button = event.target.closest("#themeToggle");
        if (button) {
            toggleTheme();
        }
    });
})();
