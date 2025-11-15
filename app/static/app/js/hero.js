// Hero Carousel functionality - Fixed version
(function() {
  'use strict';
  
  var currentSlide = 0;
  var textSlides = [];
  var imageSlides = [];
  var carouselInterval;
  var isTransitioning = false;
  var initialized = false;
  
  // Initialize slides properly
  function initializeSlides() {
    if (initialized) return;
    
    var textContainer = document.querySelector('.slide-one-item-alt-text');
    var imageContainer = document.querySelector('.slide-one-item-alt');
    
    if (!textContainer || !imageContainer) {
      console.log('Containers not found');
      return;
    }
    
    // Re-query slides to ensure we have the latest
    textSlides = Array.from(document.querySelectorAll('.slide-one-item-alt-text .slide-text'));
    imageSlides = Array.from(document.querySelectorAll('.slide-one-item-alt img'));
    
    if (textSlides.length === 0 || imageSlides.length === 0) {
      console.log('Slides not found - text:', textSlides.length, 'images:', imageSlides.length);
      return;
    }
    
    // Ensure we have matching counts - use the minimum
    var minCount = Math.min(textSlides.length, imageSlides.length);
    if (minCount === 0) {
      console.log('No matching slides found');
      return;
    }
    
    textSlides = textSlides.slice(0, minCount);
    imageSlides = imageSlides.slice(0, minCount);
    
    console.log('Initializing with', minCount, 'slides');
    
    // Set up containers
    textContainer.style.position = 'relative';
    textContainer.style.overflow = 'hidden';
    
    imageContainer.style.position = 'relative';
    imageContainer.style.overflow = 'hidden';
    
    // Temporarily set slides to static to measure heights
    textSlides.forEach((slide) => {
      var originalPosition = slide.style.position;
      slide.style.position = 'static';
      slide.style.visibility = 'hidden';
      slide.style.opacity = '0';
    });
    
    imageSlides.forEach((slide) => {
      var originalPosition = slide.style.position;
      slide.style.position = 'static';
      slide.style.visibility = 'hidden';
      slide.style.opacity = '0';
    });
    
    // Force reflow
    void textContainer.offsetHeight;
    void imageContainer.offsetHeight;
    
    // Calculate max heights
    var maxTextHeight = 0;
    var maxImageHeight = 0;
    
    textSlides.forEach(function(slide) {
      var height = slide.offsetHeight || slide.scrollHeight;
      if (height > maxTextHeight) maxTextHeight = height;
    });
    
    imageSlides.forEach(function(slide) {
      if (slide.complete && slide.naturalHeight) {
        var height = slide.naturalHeight || slide.offsetHeight || 600;
        if (height > maxImageHeight) maxImageHeight = height;
      } else {
        maxImageHeight = Math.max(maxImageHeight, 600);
      }
    });
    
    // Set container heights
    if (maxTextHeight > 0) {
      textContainer.style.height = maxTextHeight + 'px';
      textContainer.style.minHeight = maxTextHeight + 'px';
    } else {
      textContainer.style.minHeight = '300px';
    }
    
    if (maxImageHeight > 0) {
      imageContainer.style.height = maxImageHeight + 'px';
      imageContainer.style.minHeight = maxImageHeight + 'px';
    } else {
      imageContainer.style.minHeight = '600px';
      imageContainer.style.height = '600px';
    }
    
    // Now position all slides absolutely (CSS already does this, but we ensure it)
    textSlides.forEach((slide, i) => {
      slide.style.position = 'absolute';
      slide.style.top = '0';
      slide.style.left = '0';
      slide.style.right = '0';
      slide.style.width = '100%';
      slide.style.transition = 'opacity 1s ease-in-out';
      slide.style.opacity = i === 0 ? '1' : '0';
      slide.style.visibility = 'visible';
      slide.style.pointerEvents = i === 0 ? 'auto' : 'none';
      slide.style.zIndex = i === 0 ? '2' : '1';
      slide.style.display = 'block';
    });
    
    imageSlides.forEach((slide, i) => {
      slide.style.position = 'absolute';
      slide.style.top = '0';
      slide.style.left = '0';
      slide.style.right = '0';
      slide.style.width = '100%';
      slide.style.height = '100%';
      slide.style.transition = 'opacity 1s ease-in-out';
      slide.style.opacity = i === 0 ? '1' : '0';
      slide.style.visibility = 'visible';
      slide.style.pointerEvents = i === 0 ? 'auto' : 'none';
      slide.style.zIndex = i === 0 ? '2' : '1';
      slide.style.display = 'block';
      slide.style.objectFit = 'cover';
    });
    
    initialized = true;
    console.log('Slides initialized successfully');
  }
  
  function showSlide(index) {
    if (isTransitioning || !initialized) return;
    
    // Ensure index is within bounds and loops
    if (index < 0) {
      index = textSlides.length - 1;
    } else if (index >= textSlides.length) {
      index = 0;
    }
    
    // Don't transition to the same slide
    if (index === currentSlide) return;
    
    isTransitioning = true;
    var prevSlide = currentSlide;
    currentSlide = index;
    
    console.log('Transitioning from slide', prevSlide, 'to slide', index);
    
    // Bring new slide to front with higher z-index
    textSlides[index].style.zIndex = '10';
    imageSlides[index].style.zIndex = '10';
    
    // Set new slide opacity to 0 initially (it's already positioned)
    textSlides[index].style.opacity = '0';
    imageSlides[index].style.opacity = '0';
    textSlides[index].style.display = 'block';
    imageSlides[index].style.display = 'block';
    
    // Force a reflow to ensure the opacity change is registered
    void textSlides[index].offsetHeight;
    void imageSlides[index].offsetHeight;
    
    // Fade out previous slide and fade in new slide simultaneously
    requestAnimationFrame(function() {
      // Fade out previous
      if (prevSlide !== index && textSlides[prevSlide]) {
        textSlides[prevSlide].style.opacity = '0';
        imageSlides[prevSlide].style.opacity = '0';
      }
      
      // Fade in new
      textSlides[index].style.opacity = '1';
      imageSlides[index].style.opacity = '1';
      textSlides[index].style.pointerEvents = 'auto';
      imageSlides[index].style.pointerEvents = 'auto';
      
      // After transition completes
      setTimeout(function() {
        // Reset z-index of previous slide
        if (prevSlide !== index && textSlides[prevSlide]) {
          textSlides[prevSlide].style.zIndex = '1';
          imageSlides[prevSlide].style.zIndex = '1';
          textSlides[prevSlide].style.pointerEvents = 'none';
          imageSlides[prevSlide].style.pointerEvents = 'none';
        }
        // Set current slide z-index to normal
        textSlides[index].style.zIndex = '2';
        imageSlides[index].style.zIndex = '2';
        isTransitioning = false;
      }, 1000);
    });
  }

  // Function to start/restart carousel
  function startCarousel() {
    clearInterval(carouselInterval);
    if (textSlides.length > 1 && initialized) {
      console.log('Starting carousel with', textSlides.length, 'slides');
      carouselInterval = setInterval(function() {
        var nextSlide = (currentSlide + 1) % textSlides.length;
        console.log('Auto-advancing to slide', nextSlide);
        showSlide(nextSlide);
      }, 5000);
    }
  }

  // Wait for everything to load
  function initHeroCarousel() {
    if (textSlides.length === 0 || imageSlides.length === 0) {
      setTimeout(initHeroCarousel, 100);
      return;
    }
    
    console.log('Initializing carousel with', textSlides.length, 'text slides and', imageSlides.length, 'image slides');
    
    // Add error handlers for images
    imageSlides.forEach(function(img) {
      img.addEventListener('error', function() {
        console.error('Image failed to load:', img.src);
        // Set a placeholder or default styling
        img.style.backgroundColor = '#f0f0f0';
      });
      img.addEventListener('load', function() {
        console.log('Image loaded:', img.src);
      });
    });
    
    // Wait a bit longer for images to potentially load, then initialize
    setTimeout(function() {
      initializeSlides();
      startCarousel();
      console.log('Carousel initialized and started');
    }, 500);
  }

  // Initialize when DOM is ready
  function startInit() {
    // Re-query slides
    textSlides = Array.from(document.querySelectorAll('.slide-one-item-alt-text .slide-text'));
    imageSlides = Array.from(document.querySelectorAll('.slide-one-item-alt img'));
    
    console.log('startInit - Found', textSlides.length, 'text slides and', imageSlides.length, 'image slides');
    
    if (textSlides.length > 0 && imageSlides.length > 0) {
      initHeroCarousel();
    } else {
      console.log('Slides not found, retrying in 200ms...');
      setTimeout(startInit, 200);
    }
  }
  
  // Multiple initialization attempts
  function tryInit() {
    if (initialized) return;
    
    var textContainer = document.querySelector('.slide-one-item-alt-text');
    var imageContainer = document.querySelector('.slide-one-item-alt');
    
    if (textContainer && imageContainer) {
      startInit();
    } else {
      setTimeout(tryInit, 100);
    }
  }
  
  // Start initialization
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function() {
      setTimeout(tryInit, 100);
    });
  } else {
    setTimeout(tryInit, 100);
  }
  
  // Also try on window load (for images)
  window.addEventListener('load', function() {
    if (!initialized) {
      console.log('Window loaded, retrying initialization...');
      setTimeout(tryInit, 200);
    }
  });
  
  // Retry after a longer delay as fallback
  setTimeout(function() {
    if (!initialized) {
      console.log('Fallback initialization attempt...');
      tryInit();
    }
  }, 2000);
})();

