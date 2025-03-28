document.addEventListener('DOMContentLoaded', function() {
    // Initialize barometers
    updateAllBarometers();
    
    // Set up checkbox event listeners
    document.querySelectorAll('.statement-checkbox').forEach(checkbox => {
        checkbox.addEventListener('change', function() {
            updateAllBarometers();
            // Add tactile feedback on mobile
            this.parentElement.classList.add('checkbox-tap');
            setTimeout(() => {
                this.parentElement.classList.remove('checkbox-tap');
            }, 200);
        });
    });
    
    // Collapse button functionality
    document.querySelectorAll('.collapse-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const content = this.nextElementSibling;
            const isHidden = content.style.display === 'none';
            content.style.display = isHidden ? 'block' : 'none';
            this.textContent = isHidden ? 'Hide Content' : 'Show Content';
        });
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
            
            // Update colors and labels
            updateRiskVisuals(fill, label, percentage);
        });
        
        // Update overall barometer
        const allCheckboxes = document.querySelectorAll('.statement-checkbox');
        const allChecked = document.querySelectorAll('.statement-checkbox:checked').length;
        const overallPercentage = Math.round((allChecked / allCheckboxes.length) * 100);
        
        const overallFill = document.getElementById('overall-barometer-fill');
        const overallValue = document.getElementById('overall-value');
        const overallLabel = document.getElementById('overall-risk-label');
        
        overallFill.style.width = `${overallPercentage}%`;
        overallValue.textContent = `${overallPercentage}%`;
        updateRiskVisuals(overallFill, overallLabel, overallPercentage);
    }
    
    function updateRiskVisuals(fillElement, labelElement, percentage) {
        // Update colors based on risk level
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
    
    // Initialize all content sections as visible
    document.querySelectorAll('.content-list').forEach(list => {
        list.style.display = 'block';
    });
});