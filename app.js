/* مهنتي – Main JavaScript */

document.addEventListener('DOMContentLoaded', () => {

  /* ===== NAVBAR SCROLL ===== */
  const navbar = document.getElementById('navbar');
  if (navbar) {
    const handleScroll = () => {
      navbar.classList.toggle('scrolled', window.scrollY > 50);
    };
    window.addEventListener('scroll', handleScroll, { passive: true });
  }

  /* ===== HAMBURGER MENU ===== */
  const hamburger = document.getElementById('hamburger');
  const navLinks = document.getElementById('nav-links');
  if (hamburger && navLinks) {
    hamburger.addEventListener('click', () => {
      navLinks.classList.toggle('open');
    });
    // Close on link click
    navLinks.querySelectorAll('a').forEach(a => {
      a.addEventListener('click', () => navLinks.classList.remove('open'));
    });
  }

  /* ===== SMOOTH SCROLL ===== */
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', e => {
      const target = document.querySelector(anchor.getAttribute('href'));
      if (target) {
        e.preventDefault();
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    });
  });

  /* ===== ANIMATED COUNTERS ===== */
  const statNums = document.querySelectorAll('.stat-num[data-target]');
  const animateCounter = (el) => {
    const target = parseInt(el.dataset.target);
    const duration = 2000;
    const step = target / (duration / 16);
    let current = 0;
    const timer = setInterval(() => {
      current += step;
      if (current >= target) { current = target; clearInterval(timer); }
      el.textContent = Math.floor(current).toLocaleString('ar');
    }, 16);
  };

  if (statNums.length) {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(e => {
        if (e.isIntersecting) {
          animateCounter(e.target);
          observer.unobserve(e.target);
        }
      });
    }, { threshold: 0.5 });
    statNums.forEach(el => observer.observe(el));
  }

  /* ===== FEATURE CARDS FADE IN ===== */
  const featureCards = document.querySelectorAll('.feature-card');
  if (featureCards.length) {
    const cardObserver = new IntersectionObserver((entries) => {
      entries.forEach(e => {
        if (e.isIntersecting) {
          const delay = parseInt(e.target.dataset.delay || 0);
          setTimeout(() => e.target.classList.add('visible'), delay);
          cardObserver.unobserve(e.target);
        }
      });
    }, { threshold: 0.1 });
    featureCards.forEach(card => cardObserver.observe(card));
  }

  /* ===== HOW IT WORKS TABS ===== */
  const tabs = document.querySelectorAll('.tab');
  const stepsContents = document.querySelectorAll('.steps-content');
  tabs.forEach(tab => {
    tab.addEventListener('click', () => {
      tabs.forEach(t => t.classList.remove('active'));
      tab.classList.add('active');
      const target = tab.dataset.tab;
      stepsContents.forEach(sc => {
        sc.classList.toggle('hidden', sc.id !== `steps-${target}`);
      });
    });
  });

  /* ===== TESTIMONIAL SLIDER ===== */
  const testimonialCards = document.querySelectorAll('.testimonial-card');
  const dots = document.querySelectorAll('.dot');
  let currentSlide = 0;
  let sliderInterval;

  const goToSlide = (idx) => {
    testimonialCards.forEach((c, i) => {
      c.classList.toggle('active', i === idx);
    });
    dots.forEach((d, i) => {
      d.classList.toggle('active', i === idx);
    });
    currentSlide = idx;
  };

  const startSlider = () => {
    sliderInterval = setInterval(() => {
      goToSlide((currentSlide + 1) % testimonialCards.length);
    }, 4500);
  };

  if (testimonialCards.length) {
    dots.forEach((dot, i) => {
      dot.addEventListener('click', () => {
        clearInterval(sliderInterval);
        goToSlide(i);
        startSlider();
      });
    });
    startSlider();
  }

  /* ===== NAVBAR ACTIVE LINK ON SCROLL ===== */
  const sections = document.querySelectorAll('section[id]');
  if (sections.length) {
    const sectionObserver = new IntersectionObserver((entries) => {
      entries.forEach(e => {
        if (e.isIntersecting) {
          const id = e.target.id;
          document.querySelectorAll('.nav-links a').forEach(a => {
            a.style.color = '';
            if (a.getAttribute('href') === `#${id}`) {
              a.style.color = 'var(--primary)';
            }
          });
        }
      });
    }, { threshold: 0.4, rootMargin: '-80px 0px -40px 0px' });
    sections.forEach(s => sectionObserver.observe(s));
  }

  /* ===== HERO PARALLAX ===== */
  const heroShapes = document.querySelectorAll('.shape');
  if (heroShapes.length) {
    window.addEventListener('mousemove', (e) => {
      const x = (e.clientX / window.innerWidth - 0.5) * 20;
      const y = (e.clientY / window.innerHeight - 0.5) * 20;
      heroShapes.forEach((shape, i) => {
        const factor = (i + 1) * 0.4;
        shape.style.transform = `translate(${x * factor}px, ${y * factor}px)`;
      });
    }, { passive: true });
  }

});
