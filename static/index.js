

document.addEventListener("DOMContentLoaded", function() {
    // Select all elements with the 'fade-in-section' class
    const sections = document.querySelectorAll('.fade-in-section');

    // Function to check if an element is in the viewport
    function isInViewport(element) {
        const rect = element.getBoundingClientRect();
        return (
            rect.top <= (window.innerHeight || document.documentElement.clientHeight) &&
            rect.bottom >= 0
        );
    }

    // Function to add 'visible' class when the section comes into view
    function checkScroll() {
        sections.forEach(section => {
            if (isInViewport(section)) {
                section.classList.add('visible');
            }
        });
    }

    // Listen to scroll event
    window.addEventListener('scroll', checkScroll);

    // Initial check in case the section is already in view
    checkScroll();
});