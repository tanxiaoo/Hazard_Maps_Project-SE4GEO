alert('JavaScript file is loaded');

function initializeScript() {
    console.log('Initializing script...');

    function updateLegendVisibility() {
        var layersControl = document.querySelector('.leaflet-control-layers-list');
        var landslideLegendContainer = document.querySelector("#landslide-legend-container");
        var populationLegendContainer = document.querySelector("#population-legend-container");

        if (!layersControl || !landslideLegendContainer || !populationLegendContainer) {
            console.error('Layers control or legend containers not found');
            return;
        }

        var landslideLayerInput = Array.from(layersControl.querySelectorAll('input'))
            .find(function(input) {
                return input.nextElementSibling && input.nextElementSibling.textContent.trim() === 'Landslide Hazard Map';
            });

        var populationLayerInput = Array.from(layersControl.querySelectorAll('input'))
            .find(function(input) {
                return input.nextElementSibling && input.nextElementSibling.textContent.trim() === 'Population Density';
            });

        console.log('landslideLayerInput:', landslideLayerInput);
        console.log('populationLayerInput:', populationLayerInput);

        if (landslideLayerInput && landslideLayerInput.checked) {
            landslideLegendContainer.style.display = 'block';
            console.log('Landslide Legend shown');
        } else {
            landslideLegendContainer.style.display = 'none';
            console.log('Landslide Legend hidden');
        }

        if (populationLayerInput && populationLayerInput.checked) {
            populationLegendContainer.style.display = 'block';
            console.log('Population Legend shown');
        } else {
            populationLegendContainer.style.display = 'none';
            console.log('Population Legend hidden');
        }
    }

    function waitForElementToDisplay(selector, time) {
        if (document.querySelector(selector) != null) {
            updateLegendVisibility();
            document.querySelector('.leaflet-control-layers-list').addEventListener('change', updateLegendVisibility);
            return;
        } else {
            setTimeout(function() {
                waitForElementToDisplay(selector, time);
            }, time);
        }
    }

    waitForElementToDisplay('.leaflet-control-layers-list', 1000);
}

window.onload = function() {
    console.log('Window loaded');
    initializeScript();
}
