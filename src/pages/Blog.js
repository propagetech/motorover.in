/**
 * Blog Page Component
 * Blog listing with categories and SEO optimization
 */

export function initBlogPage() {
  initBlogFilters();
  initBlogPosts();
}

function initBlogFilters() {
  const filterButtons = document.querySelectorAll('.blog-filter');
  filterButtons.forEach(button => {
    button.addEventListener('click', (e) => {
      const category = e.target.dataset.category;
      filterBlogPosts(category);
      
      // Update active state
      filterButtons.forEach(btn => btn.classList.remove('active'));
      e.target.classList.add('active');
    });
  });
}

function filterBlogPosts(category) {
  const posts = document.querySelectorAll('.blog-post');
  posts.forEach(post => {
    if (category === 'all' || post.dataset.category === category) {
      post.style.display = '';
    } else {
      post.style.display = 'none';
    }
  });
}

function initBlogPosts() {
  // Add any blog post specific interactions
  const posts = document.querySelectorAll('.blog-post');
  posts.forEach(post => {
    // Lazy load images
    const images = post.querySelectorAll('img[data-src]');
    images.forEach(img => {
      if ('IntersectionObserver' in window) {
        const observer = new IntersectionObserver((entries) => {
          entries.forEach(entry => {
            if (entry.isIntersecting) {
              img.src = img.dataset.src;
              observer.unobserve(img);
            }
          });
        });
        observer.observe(img);
      } else {
        img.src = img.dataset.src;
      }
    });
  });
}

export default { initBlogPage };
