const toggles = document.querySelectorAll('.theme-checkbox');
const currentTheme = localStorage.getItem('theme');

if (currentTheme === 'dark') {
    document.body.classList.add('dark-mode');
    toggles.forEach(toggle => toggle.checked = true);
}

toggles.forEach(toggle => {
    toggle.addEventListener('change', (e) => {
        if (e.target.checked) {
            document.body.classList.add('dark-mode');
            localStorage.setItem('theme', 'dark');
        } else {
            document.body.classList.remove('dark-mode');
            localStorage.setItem('theme', 'light');
        }
        toggles.forEach(el => el.checked = e.target.checked);
    });
});