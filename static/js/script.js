// Initialize mobile touch interactions
document.addEventListener('DOMContentLoaded', function() {
    // Touch feedback for buttons
    const addTapFeedback = (element) => {
        element.addEventListener('touchstart', () => {
            element.classList.add('tap-active');
        });
        element.addEventListener('touchend', () => {
            element.classList.remove('tap-active');
        });
    };

    // Collapse functionality
    document.querySelectorAll('.collapse-btn').forEach(btn => {
        addTapFeedback(btn);
        btn.addEventListener('click', function() {
            const content = this.nextElementSibling;
            const isHidden = content.style.display === 'none';
            content.style.display = isHidden ? 'block' : 'none';
            this.textContent = isHidden ? 'Hide Content' : 'Show Content';
        });
    });

    // Quick exit button
    const quickExit = document.getElementById('quick-exit');
    if (quickExit) {
        addTapFeedback(quickExit);
        quickExit.addEventListener('click', () => {
            window.location.href = 'https://www.google.com';
        });
    }

    // Checkbox and barometer logic
    document.querySelectorAll('.statement-checkbox').forEach(checkbox => {
        checkbox.addEventListener('change', function() {
            updateBarometer(this.closest('.slide'));
        });
    });

    function updateBarometer(slide) {
        const checked = slide.querySelectorAll('.statement-checkbox:checked').length;
        const total = slide.querySelectorAll('.statement-checkbox').length;
        const percentage = (checked / total) * 100;
        
        slide.querySelector('.segment-barometer-fill').style.width = `${percentage}%`;
        slide.querySelector('.segment-checked-count').textContent = `${checked} / ${total}`;
        
        // Update main barometer
        const allChecked = document.querySelectorAll('.statement-checkbox:checked').length;
        const allTotal = document.querySelectorAll('.statement-checkbox').length;
        document.getElementById('overall-barometer-fill').style.width = `${(allChecked/allTotal)*100}%`;
        document.getElementById('overall-checked-count').textContent = `${allChecked} / ${allTotal}`;
    }
});

// Service Worker Registration
if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        navigator.serviceWorker.register('/service-worker.js')
            .then(registration => {
                console.log('SW registered:', registration);
            })
            .catch(registrationError => {
                console.log('SW registration failed:', registrationError);
            });
    });
}