// Hero Carousel functionality from Clone
document.addEventListener('DOMContentLoaded', function() {
  // Carousel functionality - ensuring all slides work properly
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
    
    if (!textContainer || !imageContainer || textSlides.length === 0 || imageSlides.length === 0) {
      return;
    }
    
    // Set up containers
    textContainer.style.position = 'relative';
    textContainer.style.overflow = 'hidden';
    
    imageContainer.style.position = 'relative';
    imageContainer.style.overflow = 'hidden';
    
    // First, reset all slides to measure heights properly
    textSlides.forEach((slide, i) => {
      slide.style.position = 'static';
      slide.style.display = 'block';
      slide.style.opacity = '1';
      slide.style.visibility = 'visible';
    });
    
    imageSlides.forEach((slide, i) => {
      slide.style.position = 'static';
      slide.style.display = 'block';
      slide.style.opacity = '1';
      slide.style.visibility = 'visible';
    });
    
    // Force reflow
    void textContainer.offsetHeight;
    void imageContainer.offsetHeight;
    
    // Calculate max heights
    var maxTextHeight = 0;
    var maxImageHeight = 0;
    
    textSlides.forEach(function(slide) {
      var height = slide.offsetHeight;
      if (height > maxTextHeight) maxTextHeight = height;
    });
    
    imageSlides.forEach(function(slide) {
      // Wait for image to load if needed
      if (slide.complete) {
        var height = slide.offsetHeight || slide.naturalHeight || slide.clientHeight || 600;
        if (height > maxImageHeight) maxImageHeight = height;
      } else {
        // If image not loaded, use a default height
        maxImageHeight = Math.max(maxImageHeight, 600);
      }
    });
    
    // Set container heights - ensure minimum heights
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
    
    // Now position all slides absolutely
    textSlides.forEach((slide, i) => {
      slide.style.position = 'absolute';
      slide.style.top = '0';
      slide.style.left = '0';
      slide.style.right = '0';
      slide.style.width = '100%';
      slide.style.transition = 'opacity 0.5s ease-in-out';
      slide.style.opacity = i === 0 ? '1' : '0';
      slide.style.visibility = i === 0 ? 'visible' : 'visible';
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
      slide.style.transition = 'opacity 0.5s ease-in-out';
      slide.style.opacity = i === 0 ? '1' : '0';
      slide.style.visibility = 'visible';
      slide.style.pointerEvents = i === 0 ? 'auto' : 'none';
      slide.style.zIndex = i === 0 ? '2' : '1';
      slide.style.display = 'block';
    });
    
    initialized = true;
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
      }, 500);
    });
  }

  // Function to start/restart carousel
  function startCarousel() {
    clearInterval(carouselInterval);
    console.log('Hero carousel: startCarousel called', {
      textSlides: textSlides.length,
      imageSlides: imageSlides.length,
      initialized: initialized
    });
    
    if (textSlides.length > 1 && initialized && textSlides.length === imageSlides.length) {
      console.log('Hero carousel: Starting auto-play interval');
      carouselInterval = setInterval(function() {
        if (!isTransitioning) {
          var nextSlide = (currentSlide + 1) % textSlides.length;
          console.log('Hero carousel: Moving to slide', nextSlide);
          showSlide(nextSlide);
        } else {
          console.log('Hero carousel: Skipping - transition in progress');
        }
      }, 1500);
    } else {
      console.warn('Hero carousel: Cannot start - conditions not met', {
        hasMultipleSlides: textSlides.length > 1,
        initialized: initialized,
        slidesMatch: textSlides.length === imageSlides.length
      });
    }
  }

  // Wait for everything to load
  function initCarousel() {
    if (textSlides.length === 0 || imageSlides.length === 0) {
      setTimeout(initCarousel, 100);
      return;
    }
    
    // Convert NodeLists to Arrays for easier manipulation
    textSlides = Array.from(textSlides);
    imageSlides = Array.from(imageSlides);
    
    // Make sure we have matching number of slides
    if (textSlides.length !== imageSlides.length) {
      console.warn('Hero carousel: Number of text slides (' + textSlides.length + ') does not match number of image slides (' + imageSlides.length + ')');
      // Use the minimum count
      var minCount = Math.min(textSlides.length, imageSlides.length);
      textSlides = textSlides.slice(0, minCount);
      imageSlides = imageSlides.slice(0, minCount);
    }
    
    console.log('Hero carousel: Processed slides', {
      textSlides: textSlides.length,
      imageSlides: imageSlides.length
    });
    
    // Add error handlers for images
    imageSlides.forEach(function(img) {
      img.addEventListener('error', function() {
        img.style.backgroundColor = '#f0f0f0';
      });
    });
    
    // Wait a bit longer for images to potentially load, then initialize
    setTimeout(function() {
      console.log('Hero carousel: Initializing slides...', {
        textSlides: textSlides.length,
        imageSlides: imageSlides.length
      });
      initializeSlides();
      console.log('Hero carousel: Slides initialized, starting carousel...', {
        initialized: initialized,
        textSlides: textSlides.length,
        imageSlides: imageSlides.length
      });
      if (textSlides.length > 1 && textSlides.length === imageSlides.length) {
        startCarousel();
      } else {
        console.warn('Hero carousel: Cannot start - need at least 2 matching slides', {
          textSlides: textSlides.length,
          imageSlides: imageSlides.length
        });
      }
    }, 500);
  }

  // Initialize when DOM is ready
  function startInit() {
    // Re-query slides in case they weren't found initially
    textSlides = document.querySelectorAll('.slide-one-item-alt-text .slide-text');
    imageSlides = document.querySelectorAll('.slide-one-item-alt img');
    
    console.log('Hero carousel: Looking for slides', {
      textSlides: textSlides.length,
      imageSlides: imageSlides.length,
      textContainer: !!document.querySelector('.slide-one-item-alt-text'),
      imageContainer: !!document.querySelector('.slide-one-item-alt')
    });
    
    if (textSlides.length > 0 && imageSlides.length > 0) {
      console.log('Hero carousel: Found slides, initializing...');
      initCarousel();
    } else {
      // Try again after a short delay, but limit retries
      if (typeof startInit.retries === 'undefined') {
        startInit.retries = 0;
      }
      startInit.retries++;
      if (startInit.retries < 20) { // Try for up to 4 seconds (20 * 200ms)
        setTimeout(startInit, 200);
      } else {
        console.warn('Hero carousel: Could not find slides after multiple attempts', {
          textSlides: textSlides.length,
          imageSlides: imageSlides.length
        });
      }
    }
  }
  
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function() {
      setTimeout(startInit, 100);
    });
  } else {
    setTimeout(startInit, 100);
  }
  
  // Also try on window load
  window.addEventListener('load', function() {
    if (!initialized) {
      setTimeout(startInit, 100);
    }
  });
});

