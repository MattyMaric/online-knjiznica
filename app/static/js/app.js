let featuredIndex = 0;
let bestsellerIndex = 0;

function moveFeatured(direction) {
    const items = document.querySelectorAll('#featured-carousel .featured-item');
    const visible = 3;
    const max = Math.min(items.length, 6); // max 6 knjiga
    if (max <= visible) return; // nema pomaka ako je 3 ili manje

    featuredIndex += direction;
    if (featuredIndex < 0) featuredIndex = max - visible;
    if (featuredIndex > max - visible) featuredIndex = 0;

    const carousel = document.getElementById('featured-carousel');
    const itemWidth = items[0].offsetWidth + 15; // 15px gap
    carousel.style.transform = `translateX(-${featuredIndex * itemWidth}px)`;
}

function moveBestsellers(direction) {
    const items = document.querySelectorAll('#bestsellers-carousel .bestseller-item');
    const visible = 3;
    const max = Math.min(items.length, 6);
    if (max <= visible) return;

    bestsellerIndex += direction;
    if (bestsellerIndex < 0) bestsellerIndex = max - visible;
    if (bestsellerIndex > max - visible) bestsellerIndex = 0;

    const carousel = document.getElementById('bestsellers-carousel');
    const itemWidth = items[0].offsetWidth + 15; // 15px gap
    carousel.style.transform = `translateX(-${bestsellerIndex * itemWidth}px)`;
}

// Reset on resize
window.addEventListener('resize', () => {
    moveFeatured(0);
    moveBestsellers(0);
});
