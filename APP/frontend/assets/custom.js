alert('JavaScript file is loaded');

function initializeScript() {
    function updateLegendVisibility() {
        var layersControl = document.querySelector('.leaflet-control-layers-list');
        var legendContainers = {
            'Landslide Hazard Map': document.querySelector("#landslide-legend-container"),
            'Population Density': document.querySelector("#population-legend-container"),
            'Risk Indicator Buildings': document.querySelector("#risk-indicator-buildings-legend-container"),
            'Risk Indicator Cultural Heritage': document.querySelector("#risk-indicator-cultural-heritage-legend-container"),
            'Risk Indicator Families': document.querySelector("#risk-indicator-families-legend-container"),
            'Risk Indicator Industries and Services': document.querySelector("#risk-indicator-industries-and-services-legend-container"),
            'Risk Indicator Population': document.querySelector("#risk-indicator-population-legend-container"),
            'Risk Indicator Territory': document.querySelector("#risk-indicator-territory-legend-container")
        };

        if (!layersControl) {
            console.error('Layers control not found');
            return;
        }

        for (var layerName in legendContainers) {
            var legendContainer = legendContainers[layerName];
            if (!legendContainer) {
                console.error(`Legend container for ${layerName} not found`);
                continue;
            }

            var layerInput = Array.from(layersControl.querySelectorAll('input'))
                .find(input => input.nextElementSibling && input.nextElementSibling.textContent.trim() === layerName);

            if (layerInput && layerInput.checked) {
                legendContainer.style.display = 'block';
            } else {
                legendContainer.style.display = 'none';
            }
        }
    }

    function waitForElementToDisplay(selector, time) {
        if (document.querySelector(selector) != null) {
            updateLegendVisibility();
            document.querySelector('.leaflet-control-layers-list').addEventListener('change', updateLegendVisibility);
        } else {
            setTimeout(function() {
                waitForElementToDisplay(selector, time);
            }, time);
        }
    }

    waitForElementToDisplay('.leaflet-control-layers-list', 1000);
}

window.onload = function() {
    initializeScript();
}
