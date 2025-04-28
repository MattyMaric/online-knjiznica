let featuredIndex = 0;
let bestsellerIndex = 0;

function moveFeatured(direction) {
    const items = document.querySelectorAll('#featured-carousel img');
    featuredIndex += direction;

    if (featuredIndex < 0) featuredIndex = items.length - 1;
    if (featuredIndex >= items.length) featuredIndex = 0;

    const carousel = document.getElementById('featured-carousel');
    carousel.style.transform = `translateX(-${featuredIndex * 300}px)`;
}

function moveBestsellers(direction) {
    //const itemsContainer = document.querySelectorAll('#bestsellers-carousel');
    const items = document.querySelectorAll('#bestsellers-carousel .bestseller-item');
    bestsellerIndex += direction;

    if (bestsellerIndex < 0) bestsellerIndex = 0;
    if (bestsellerIndex >= items.length) bestsellerIndex = 0 //items.length - 2;

    const carousel = document.getElementById('bestsellers-carousel');
    const itemWidth = 250 + 20;
    carousel.style.transform = `translateX(-${bestsellerIndex * itemWidth}px)`;
}
