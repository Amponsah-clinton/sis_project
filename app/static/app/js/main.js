    function toggleMenu() {
      const overlay = document.getElementById('sheetOverlay');
      overlay.classList.toggle('open');
    }

    function closeMenu() {
      const overlay = document.getElementById('sheetOverlay');
      overlay.classList.remove('open');
    }

    window.toggleDropdown = function(event) {
      event.preventDefault();
      event.stopPropagation();
      const dropdown = event.currentTarget.closest('.nav-dropdown');
      if (!dropdown) return;
      
      const isActive = dropdown.classList.contains('active');
      
      // Close all other dropdowns
      document.querySelectorAll('.nav-dropdown').forEach(d => {
        d.classList.remove('active');
      });
      
      // Toggle current dropdown
      if (!isActive) {
        dropdown.classList.add('active');
      }
    };

    // Close dropdown when clicking outside
    document.addEventListener('click', function(event) {
      if (!event.target.closest('.nav-dropdown')) {
        document.querySelectorAll('.nav-dropdown').forEach(d => {
          d.classList.remove('active');
        });
      }
    });

    function toggleTheme() {
      const html = document.documentElement;
      const currentTheme = html.getAttribute('data-theme');
      const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
      html.setAttribute('data-theme', newTheme);
      localStorage.setItem('theme', newTheme);
      updateThemeIcon(newTheme);
    }

    function updateThemeIcon(theme) {
      const lightIcon = document.getElementById('lightIcon');
      const darkIcon = document.getElementById('darkIcon');
      if (theme === 'dark') {
        lightIcon.style.display = 'none';
        darkIcon.style.display = 'block';
      } else {
        lightIcon.style.display = 'block';
        darkIcon.style.display = 'none';
      }
    }

    function quickView(event, id) {
      event.stopPropagation();
      alert(`Quick view for article ${id}. This would open a modal or navigate to article details.`);
      // In a real implementation, this would open a modal or navigate to the article page
    }

    // Page Loader Animation
    function initPageLoader() {
      const loadCon = document.getElementById('loadCon');
      const pageLoader = document.querySelector('.page-loader');
      
      if (!loadCon || !pageLoader) return;

      // Check if GSAP is loaded
      if (typeof gsap === 'undefined') {
        // If GSAP isn't loaded, hide loader immediately
        pageLoader.classList.add('hidden');
        return;
      }

      // Show loader container
      loadCon.style.display = 'flex';
      loadCon.style.visibility = 'visible';

      // Create GSAP timeline
      const tl = gsap.timeline({
        onComplete: function() {
          // Hide loader after animation completes
          gsap.to(pageLoader, {
            opacity: 0,
            duration: 0.5,
            ease: "power2.out",
            onComplete: function() {
              pageLoader.style.display = 'none';
              pageLoader.classList.add('hidden');
            }
          });
        }
      });

      tl.to("#loadCon", {
        scale: 1,
        opacity: 1,
        display: "flex",
        duration: 2,
        ease: "elastic.out(1, 0.6)"
      })
      .to("#loadCon #inner1", {
        scale: 1,
        duration: 2,
        ease: "elastic.out(1, 0.6)"
      }, "-=1.5")
      .to("#loadCon #inner1", {
        borderWidth: "1px",
        duration: 1,
        ease: "power4.out"
      }, "-=1.5")
      .to("#loadCon #inner2", {
        width: "60%",
        opacity: "1",
        duration: 1,
        ease: "bounce.out"
      }, "-=1.5")
      .to(".loader-logo", {
        scale: 1,
        opacity: 1,
        duration: 1,
        ease: "power4.out"
      }, "-=1")
      .to("#loadCon", {
        scale: 1.1,
        border: "20px solid rgba(255,255,255,0.1)",
        duration: 1,
        ease: "back.out(1.7)",
        repeat: 2,
        yoyo: true
      }, "-=1");

      // Fallback: Hide loader after maximum time (8 seconds) even if animation fails
      setTimeout(function() {
        if (!pageLoader.classList.contains('hidden')) {
          pageLoader.style.opacity = '0';
          setTimeout(function() {
            pageLoader.style.display = 'none';
            pageLoader.classList.add('hidden');
          }, 500);
        }
      }, 8000);
    }

    // Stats counter animation
    function animateCounter(element, target, duration = 2000) {
      const start = 0;
      const increment = target / (duration / 16);
      let current = start;
      
      const timer = setInterval(() => {
        current += increment;
        if (current >= target) {
          element.textContent = formatNumber(target);
          clearInterval(timer);
        } else {
          element.textContent = formatNumber(Math.floor(current));
        }
      }, 16);
    }

    function formatNumber(num) {
      if (num >= 1000000) {
        return (num / 1000000).toFixed(1) + 'M';
      } else if (num >= 1000) {
        return (num / 1000).toFixed(1) + 'K';
      }
      return Math.floor(num).toString();
    }

    // Articles Carousel functionality
    let articlesCurrentSlide = 0;
    let articlesTotalSlides = 1;
    let articlesCarouselTrack;
    let articlesIndicatorsContainer;
    let articlesAutoPlayInterval;

    function initArticlesCarousel() {
      articlesCarouselTrack = document.getElementById('articlesCarousel');
      articlesIndicatorsContainer = document.getElementById('articlesIndicators');
      
      if (!articlesCarouselTrack || !articlesIndicatorsContainer) return;
      
      const cards = articlesCarouselTrack.querySelectorAll('.article-card');
      articlesTotalSlides = cards.length;
      
      if (articlesTotalSlides === 0) return;
      
      // Calculate how many cards to show per slide based on screen size
      const getCardsPerSlide = () => {
        if (window.innerWidth >= 1024) return 3;
        if (window.innerWidth >= 768) return 2;
        return 1;
      };
      
      let cardsPerSlide = getCardsPerSlide();
      const totalSlides = Math.ceil(articlesTotalSlides / cardsPerSlide);
      
      // Create indicators based on visible slides
      articlesIndicatorsContainer.innerHTML = '';
      for (let i = 0; i < totalSlides; i++) {
        const indicator = document.createElement('button');
        indicator.className = 'carousel-indicator' + (i === 0 ? ' active' : '');
        indicator.setAttribute('onclick', `goToArticlesSlide(${i})`);
        indicator.setAttribute('aria-label', `Go to slide ${i + 1}`);
        articlesIndicatorsContainer.appendChild(indicator);
      }
      
      // Update on resize - use a single handler
      if (!window.articlesCarouselResizeHandler) {
        window.articlesCarouselResizeHandler = function() {
          clearTimeout(window.articlesCarouselResizeTimeout);
          window.articlesCarouselResizeTimeout = setTimeout(() => {
            if (articlesCarouselTrack) {
              articlesCurrentSlide = 0;
              updateArticlesCarousel();
            }
          }, 250);
        };
        window.addEventListener('resize', window.articlesCarouselResizeHandler);
      }
      
      updateArticlesCarousel();
      startArticlesAutoPlay();
      
      // Pause on hover
      const carouselWrapper = articlesCarouselTrack.closest('.articles-carousel-wrapper');
      if (carouselWrapper) {
        carouselWrapper.addEventListener('mouseenter', stopArticlesAutoPlay);
        carouselWrapper.addEventListener('mouseleave', startArticlesAutoPlay);
      }
    }

    function startArticlesAutoPlay() {
      stopArticlesAutoPlay();
      articlesAutoPlayInterval = setInterval(() => {
        if (articlesCarouselTrack) {
          const cards = articlesCarouselTrack.querySelectorAll('.article-card');
          if (cards.length === 0) return;
          
          let cardsPerSlide;
          if (window.innerWidth >= 1024) {
            cardsPerSlide = 3;
          } else if (window.innerWidth >= 768) {
            cardsPerSlide = 2;
          } else {
            cardsPerSlide = 1;
          }
          
          const totalSlides = Math.ceil(cards.length / cardsPerSlide);
          articlesCurrentSlide = (articlesCurrentSlide + 1) % totalSlides;
          updateArticlesCarousel();
        }
      }, 4000); // Auto-slide every 4 seconds
    }

    function stopArticlesAutoPlay() {
      if (articlesAutoPlayInterval) {
        clearInterval(articlesAutoPlayInterval);
        articlesAutoPlayInterval = null;
      }
    }

    function updateArticlesCarousel() {
      if (!articlesCarouselTrack) return;
      
      const cards = articlesCarouselTrack.querySelectorAll('.article-card');
      if (cards.length === 0) return;
      
      // Get card width including gap
      const container = articlesCarouselTrack.parentElement;
      const containerWidth = container.offsetWidth;
      const gap = 24; // 1.5rem = 24px
      
      let cardsPerSlide;
      if (window.innerWidth >= 1024) {
        cardsPerSlide = 3;
      } else if (window.innerWidth >= 768) {
        cardsPerSlide = 2;
      } else {
        cardsPerSlide = 1;
      }
      
      const cardWidth = (containerWidth - (gap * (cardsPerSlide - 1))) / cardsPerSlide;
      const translateX = -(articlesCurrentSlide * (cardWidth + gap));
      
      articlesCarouselTrack.style.transform = `translateX(${translateX}px)`;
      
      // Update indicators
      const totalSlides = Math.ceil(cards.length / cardsPerSlide);
      const indicators = articlesIndicatorsContainer.querySelectorAll('.carousel-indicator');
      indicators.forEach((indicator, index) => {
        if (index === articlesCurrentSlide && index < totalSlides) {
          indicator.classList.add('active');
        } else {
          indicator.classList.remove('active');
        }
      });
    }

    function slideArticles(direction) {
      if (!articlesCarouselTrack) return;
      
      const cards = articlesCarouselTrack.querySelectorAll('.article-card');
      if (cards.length === 0) return;
      
      let cardsPerSlide;
      if (window.innerWidth >= 1024) {
        cardsPerSlide = 3;
      } else if (window.innerWidth >= 768) {
        cardsPerSlide = 2;
      } else {
        cardsPerSlide = 1;
      }
      
      const totalSlides = Math.ceil(cards.length / cardsPerSlide);
      
      if (direction === 'next') {
        articlesCurrentSlide = (articlesCurrentSlide + 1) % totalSlides;
      } else if (direction === 'prev') {
        articlesCurrentSlide = (articlesCurrentSlide - 1 + totalSlides) % totalSlides;
      }
      updateArticlesCarousel();
    }

    function goToArticlesSlide(index) {
      articlesCurrentSlide = index;
      updateArticlesCarousel();
    }

    // Intersection Observer for scroll animations
    function initScrollAnimations() {
      const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
      };

      const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            
            // Animate stats counters
            if (entry.target.classList.contains('stats-section')) {
              const statNumbers = entry.target.querySelectorAll('.stat-number');
              statNumbers.forEach(stat => {
                const target = parseInt(stat.getAttribute('data-target'));
                stat.textContent = '0';
                animateCounter(stat, target);
              });
            }
          }
        });
      }, observerOptions);

      // Observe sections
      const sections = document.querySelectorAll('.stats-section, .featured-section, .members-section, .image-text-section');
      sections.forEach(section => {
        observer.observe(section);
      });
    }

    // Hero Search Dropdown
    function initHeroSearch() {
      const searchTypeBtn = document.getElementById('searchTypeBtn');
      const searchTypeMenu = document.getElementById('searchTypeMenu');
      const searchTypeOptions = document.querySelectorAll('.search-type-option');
      const dropdown = searchTypeBtn?.closest('.search-type-dropdown');

      if (!searchTypeBtn || !searchTypeMenu || !dropdown) return;

      // Toggle dropdown
      searchTypeBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        dropdown.classList.toggle('active');
      });

      // Select option
      searchTypeOptions.forEach(option => {
        option.addEventListener('click', () => {
          const type = option.getAttribute('data-type');
          const text = option.textContent;
          
          // Update button text
          searchTypeBtn.querySelector('span').textContent = text;
          
          // Update active state
          searchTypeOptions.forEach(opt => opt.classList.remove('active'));
          option.classList.add('active');
          
          // Close dropdown
          dropdown.classList.remove('active');
        });
      });

      // Close dropdown when clicking outside
      document.addEventListener('click', (e) => {
        if (!dropdown.contains(e.target)) {
          dropdown.classList.remove('active');
        }
      });

      // Handle search button
      const searchBtn = document.querySelector('.hero-search-btn');
      const searchInput = document.getElementById('heroSearchInput');
      
      if (searchBtn && searchInput) {
        const performSearch = () => {
          const query = searchInput.value.trim();
          const type = document.querySelector('.search-type-option.active')?.getAttribute('data-type') || 'articles';
          
          if (query) {
            // In a real implementation, this would navigate to search results
            console.log(`Searching for ${query} in ${type}`);
            // window.location.href = `/search?q=${encodeURIComponent(query)}&type=${type}`;
          }
        };

        searchBtn.addEventListener('click', performSearch);
        searchInput.addEventListener('keypress', (e) => {
          if (e.key === 'Enter') {
            performSearch();
          }
        });
      }
    }

    // Initialize theme from localStorage
    document.addEventListener('DOMContentLoaded', function() {
      const savedTheme = localStorage.getItem('theme') || 'light';
      document.documentElement.setAttribute('data-theme', savedTheme);
      updateThemeIcon(savedTheme);
      
      // Initialize page loader animation
      // initPageLoader();
      
      // Initialize hero carousel (only if hero carousel exists, otherwise skip)
      // Note: Hero carousel is handled by hero.js
      var heroCarousel = document.querySelector('.slide-one-item-alt-text');
      if (!heroCarousel) {
        initCarousel(); // Only init if it's not the hero carousel
      }
      
      // Initialize articles carousel
      initArticlesCarousel();
      
      // Initialize hero search
      initHeroSearch();
      
      // Initialize scroll animations
      initScrollAnimations();
      
      // Navbar scroll effect
      const header = document.querySelector('header');
      let lastScroll = 0;
      
      window.addEventListener('scroll', function() {
        const currentScroll = window.pageYOffset;
        
        if (currentScroll > 50) {
          header.classList.add('scrolled');
        } else {
          header.classList.remove('scrolled');
        }
        
        lastScroll = currentScroll;
      });
    });

    // Hero Carousel functionality
    let heroCurrentSlide = 0;
    let heroCarouselInterval;
    let heroSlides, heroIndicators, heroTotalSlides;

    function initCarousel() {
      heroSlides = document.querySelectorAll('#hero-carousel .carousel-item');
      heroIndicators = document.querySelectorAll('#hero-carousel .carousel-indicators li');
      heroTotalSlides = heroSlides.length;
      
      if (heroTotalSlides === 0) return;
      
      // Generate indicators
      const indicatorsContainer = document.querySelector('#hero-carousel .carousel-indicators');
      if (indicatorsContainer && heroIndicators.length === 0) {
        indicatorsContainer.innerHTML = '';
        heroSlides.forEach((slide, index) => {
          const li = document.createElement('li');
          if (index === 0) {
            li.classList.add('active');
          }
          li.setAttribute('data-slide-to', index);
          li.onclick = () => goToHeroSlide(index);
          indicatorsContainer.appendChild(li);
        });
        heroIndicators = document.querySelectorAll('#hero-carousel .carousel-indicators li');
      }
      
      updateHeroCarousel();
      startHeroAutoPlay();
      
      // Pause on hover
      const carousel = document.querySelector('#hero-carousel');
      if (carousel) {
        carousel.addEventListener('mouseenter', stopHeroAutoPlay);
        carousel.addEventListener('mouseleave', startHeroAutoPlay);
      }
    }

    function updateHeroCarousel() {
      if (!heroSlides || !heroIndicators) return;
      
      // Update text slides
      heroSlides.forEach((slide, index) => {
        slide.classList.remove('active');
        if (index === heroCurrentSlide) {
          slide.classList.add('active');
        }
      });

      // Update indicators
      heroIndicators.forEach((indicator, index) => {
        indicator.classList.remove('active');
        if (index === heroCurrentSlide) {
          indicator.classList.add('active');
        }
      });

      // Update background images
      const bgSlides = document.querySelectorAll('.hero-bg-slide');
      bgSlides.forEach((bgSlide, index) => {
        bgSlide.classList.remove('active');
        if (index === heroCurrentSlide) {
          bgSlide.classList.add('active');
        }
      });
    }

    function goToHeroSlide(index) {
      if (!heroTotalSlides) return;
      heroCurrentSlide = index;
      updateHeroCarousel();
      resetHeroAutoPlay();
    }

    function heroCarouselNext() {
      if (!heroTotalSlides) return;
      heroCurrentSlide = (heroCurrentSlide + 1) % heroTotalSlides;
      updateHeroCarousel();
      resetHeroAutoPlay();
    }

    function heroCarouselPrev() {
      if (!heroTotalSlides) return;
      heroCurrentSlide = (heroCurrentSlide - 1 + heroTotalSlides) % heroTotalSlides;
      updateHeroCarousel();
      resetHeroAutoPlay();
    }

    function startHeroAutoPlay() {
      stopHeroAutoPlay();
      heroCarouselInterval = setInterval(heroCarouselNext, 3000); // Change every 3 seconds
    }

    function stopHeroAutoPlay() {
      if (heroCarouselInterval) {
        clearInterval(heroCarouselInterval);
      }
    }

    function resetHeroAutoPlay() {
      stopHeroAutoPlay();
      startHeroAutoPlay();
    }

    // Keyboard navigation
    document.addEventListener('keydown', function(e) {
      const hero = document.querySelector('#hero');
      if (!hero) return;
      
      const rect = hero.getBoundingClientRect();
      if (rect.top < window.innerHeight && rect.bottom > 0) {
        if (e.key === 'ArrowLeft') {
          e.preventDefault();
          heroCarouselPrev();
        } else if (e.key === 'ArrowRight') {
          e.preventDefault();
          heroCarouselNext();
        }
      }
    });
