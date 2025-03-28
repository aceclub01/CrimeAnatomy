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
    const allCheckboxes = document.querySelectorAll('.statement-checkbox');
    
    // Initial update
    updateAllBarometers();
    
    // Event listeners
    allCheckboxes.forEach(checkbox => {
        checkbox.addEventListener('change', updateAllBarometers);
    });
    
    function updateAllBarometers() {
        // Update section barometers
        document.querySelectorAll('.slide').forEach((slide, index) => {
            const checkboxes = slide.querySelectorAll('.statement-checkbox');
            const checked = slide.querySelectorAll('.statement-checkbox:checked').length;
            const percentage = Math.round((checked / checkboxes.length) * 100);
            
            const fill = document.getElementById(`section-barometer-${index+1}`);
            const value = document.getElementById(`section-value-${index+1}`);
            const label = document.getElementById(`section-risk-label-${index+1}`);
            
            fill.style.width = `${percentage}%`;
            value.textContent = `${percentage}%`;
            updateRiskVisuals(fill, label, percentage);
        });
        
        // Update overall barometer
        const totalChecked = document.querySelectorAll('.statement-checkbox:checked').length;
        const totalCheckboxes = allCheckboxes.length;
        const overallPercentage = Math.round((totalChecked / totalCheckboxes.length) * 100);
        
        const overallFill = document.getElementById('overall-barometer-fill');
        const overallValue = document.getElementById('overall-value');
        const overallLabel = document.getElementById('overall-risk-label');
        
        overallFill.style.width = `${overallPercentage}%`;
        overallValue.textContent = `${overallPercentage}%`;
        updateRiskVisuals(overallFill, overallLabel, overallPercentage);
    }
    
    function updateRiskVisuals(fillElement, labelElement, percentage) {
        if (percentage < 33) {
            fillElement.style.backgroundColor = '#4CAF50';
            labelElement.textContent = 'Low Risk';
            labelElement.className = 'risk-label risk-low';
        } else if (percentage < 66) {
            fillElement.style.backgroundColor = '#FFC107';
            labelElement.textContent = 'Medium Risk';
            labelElement.className = 'risk-label risk-medium';
        } else {
            fillElement.style.backgroundColor = '#F44336';
            labelElement.textContent = 'High Risk';
            labelElement.className = 'risk-label risk-high';
        }
    }
}

function initCollapseButtons() {
    document.querySelectorAll('.collapse-btn').forEach(btn => {
        const targetId = btn.getAttribute('data-target');
        const target = document.getElementById(targetId);
        
        // Initialize state
        target.style.display = 'none';
        btn.textContent = btn.textContent.replace('Hide', 'Show');
        
        btn.addEventListener('click', function() {
            const isHidden = target.style.display === 'none';
            target.style.display = isHidden ? 'block' : 'none';
            this.textContent = isHidden ? 
                this.textContent.replace('Show', 'Hide') : 
                this.textContent.replace('Hide', 'Show');
        });
    });
}

function initImageZoom() {
    document.querySelectorAll('.image-card img').forEach(img => {
        img.addEventListener('click', function() {
            if (document.body.classList.contains('touch-device')) {
                this.classList.toggle('zoomed');
                document.body.style.overflow = this.classList.contains('zoomed') ? 'hidden' : '';
            }
        });
    });
}