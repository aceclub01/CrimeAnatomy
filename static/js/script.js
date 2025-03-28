document.addEventListener('DOMContentLoaded', function() {
    // Initialize all components
    initBarometers();
    initCollapseButtons();
    initImageZoom();
    
    // Touch device detection
    const isTouchDevice = 'ontouchstart' in window;
    if (isTouchDevice) {
        document.body.classList.add('touch-device');
    }
});

function initBarometers() {
    // [Previous barometer code here]
}

function initCollapseButtons() {
    document.querySelectorAll('.collapse-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const targetId = this.getAttribute('data-target');
            const target = document.getElementById(targetId);
            const isHidden = target.style.display === 'none';
            
            target.style.display = isHidden ? 'block' : 'none';
            this.textContent = isHidden ? 
                this.textContent.replace('Show', 'Hide') : 
                this.textContent.replace('Hide', 'Show');
            
            // Smooth animation
            target.style.overflow = 'hidden';
            target.style.transition = 'max-height 0.3s ease, opacity 0.3s ease';
            target.style.maxHeight = isHidden ? '1000px' : '0';
            target.style.opacity = isHidden ? '1' : '0';
            
            setTimeout(() => {
                target.style.overflow = '';
                target.style.transition = '';
            }, 300);
        });
    });
}

function initImageZoom() {
    document.querySelectorAll('.image-card img').forEach(img => {
        // Click/tap to enlarge
        img.addEventListener('click', function() {
            if (document.body.classList.contains('touch-device')) {
                this.classList.toggle('zoomed');
                document.body.style.overflow = this.classList.contains('zoomed') ? 'hidden' : '';
            }
        });
        
        // Prevent accidental zooms on mobile
        img.addEventListener('touchstart', function(e) {
            if (e.touches.length > 1) {
                e.preventDefault();
            }
        }, { passive: false });
    });
}