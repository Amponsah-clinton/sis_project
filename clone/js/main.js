// Simple vanilla JS for basic functionality
document.addEventListener('DOMContentLoaded', function() {
  // Hide loader
  setTimeout(function() {
    var overlayer = document.getElementById('overlayer');
    var loader = document.querySelector('.loader');
    if (overlayer) overlayer.style.display = 'none';
    if (loader) loader.style.display = 'none';
  }, 1000);

  // Smooth scroll for anchor links
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
      e.preventDefault();
      var target = document.querySelector(this.getAttribute('href'));
      if (target) {
        target.scrollIntoView({
          behavior: 'smooth',
          block: 'start'
        });
      }
    });
  });


  // Counter animation
  function animateCounter(element, target) {
    var current = 0;
    var increment = target / 100;
    var timer = setInterval(function() {
      current += increment;
      if (current >= target) {
        element.textContent = Math.floor(target);
        clearInterval(timer);
      } else {
        element.textContent = Math.floor(current);
      }
    }, 20);
  }

  // Observe counter elements
  var counterObserver = new IntersectionObserver(function(entries) {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        var numberEl = entry.target.querySelector('.number');
        if (numberEl && !numberEl.classList.contains('animated')) {
          numberEl.classList.add('animated');
          var target = parseInt(numberEl.getAttribute('data-number'));
          animateCounter(numberEl, target);
        }
      }
    });
  }, { threshold: 0.5 });

  document.querySelectorAll('.counter').forEach(counter => {
    counterObserver.observe(counter);
  });


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
      slide.style.transition = 'opacity 1s ease-in-out';
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
      slide.style.transition = 'opacity 1s ease-in-out';
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
  function initCarousel() {
    if (textSlides.length === 0 || imageSlides.length === 0) {
      setTimeout(initCarousel, 100);
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
    // Re-query slides in case they weren't found initially
    textSlides = document.querySelectorAll('.slide-one-item-alt-text .slide-text');
    imageSlides = document.querySelectorAll('.slide-one-item-alt img');
    
    console.log('Found', textSlides.length, 'text slides and', imageSlides.length, 'image slides');
    
    if (textSlides.length > 0 && imageSlides.length > 0) {
      initCarousel();
    } else {
      console.log('Slides not found, retrying...');
      setTimeout(startInit, 200);
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

