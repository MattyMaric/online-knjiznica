let zanrCarouselIndex = 0;

function moveZanrCarousel(direction) {
    // Get all carousel items
    const carouselItems = document.querySelectorAll('#carouselZanr .carousel-item');
    zanrCarouselIndex += direction;

    // Handle edge cases for infinite carousel
    if (zanrCarouselIndex < 0) zanrCarouselIndex = carouselItems.length - 1;
    if (zanrCarouselIndex >= carouselItems.length) zanrCarouselIndex = 0;

    // Remove 'active' class from all items and add to current index
    carouselItems.forEach(item => item.classList.remove('active'));
    carouselItems[zanrCarouselIndex].classList.add('active');
}

// Initialize carousel functionality
document.addEventListener('DOMContentLoaded', function() {
    // Add event listeners to carousel control buttons
    const prevButton = document.querySelector('#carouselZanr .carousel-control-prev');
    const nextButton = document.querySelector('#carouselZanr .carousel-control-next');
    
    if (prevButton && nextButton) {
        prevButton.addEventListener('click', function() {
            moveZanrCarousel(-1);
        });
        
        nextButton.addEventListener('click', function() {
            moveZanrCarousel(1);
        });
    }
    
    // Optional: Auto-rotate carousel
    setInterval(() => moveZanrCarousel(1), 5000);
});
