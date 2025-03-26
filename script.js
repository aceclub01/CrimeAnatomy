document.addEventListener("DOMContentLoaded", function() {
    const checkboxes = document.querySelectorAll('.statement-checkbox');
    const overallCheckedCountElement = document.getElementById('overall-checked-count');
    const overallBarometerFill = document.getElementById('overall-barometer-fill');

    const updateOverallBarometer = () => {
        const totalCheckboxes = checkboxes.length;
        const checkedCheckboxes = document.querySelectorAll('.statement-checkbox:checked').length;
        
        overallCheckedCountElement.textContent = `${checkedCheckboxes} / ${totalCheckboxes}`;
        
        const percentage = (checkedCheckboxes / totalCheckboxes) * 100;
        overallBarometerFill.style.width = percentage + '%';

        if (percentage < 33) {
            overallBarometerFill.style.backgroundColor = "#4caf50"; // Green
        } else if (percentage < 66) {
            overallBarometerFill.style.backgroundColor = "#ffeb3b"; // Yellow
        } else {
            overallBarometerFill.style.backgroundColor = "#f44336"; // Red
        }
    };

    checkboxes.forEach(checkbox => {
        checkbox.addEventListener('change', updateOverallBarometer);
    });

    updateOverallBarometer();

    // Function to update individual segment barometers
    const updateSegmentBarometer = (segment) => {
        const segmentCheckboxes = segment.querySelectorAll('.segment-checkbox');
        const segmentCheckedCount = segment.querySelectorAll('.segment-checkbox:checked').length;
        const segmentBarometerCount = segment.querySelector('.segment-checked-count');
        const segmentBarometerFill = segment.querySelector('.segment-barometer-fill');

        segmentBarometerCount.textContent = `${segmentCheckedCount} / ${segmentCheckboxes.length}`;

        const percentage = (segmentCheckedCount / segmentCheckboxes.length) * 100;
        segmentBarometerFill.style.width = percentage + '%';

        if (percentage < 33) {
            segmentBarometerFill.style.backgroundColor = "#4caf50"; // Green
        } else if (percentage < 66) {
            segmentBarometerFill.style.backgroundColor = "#ffeb3b"; // Yellow
        } else {
            segmentBarometerFill.style.backgroundColor = "#f44336"; // Red
        }
    };

    // Attach event listeners to segment checkboxes
    document.querySelectorAll('.body-section').forEach(segment => {
        const segmentCheckboxes = segment.querySelectorAll('.segment-checkbox');
        segmentCheckboxes.forEach(checkbox => {
            checkbox.addEventListener('change', () => updateSegmentBarometer(segment));
        });

        // Initial update for each segment
        updateSegmentBarometer(segment);
    });

    // Collapse/Expand functionality
    document.querySelectorAll('.collapse-btn').forEach(function(button) {
        button.addEventListener('click', function() {
            let content = this.nextElementSibling;

            if (content.style.display === 'none' || content.style.display === '') {
                content.style.display = 'block';
            } else {
                content.style.display = 'none';
            }
        });
    });
});
