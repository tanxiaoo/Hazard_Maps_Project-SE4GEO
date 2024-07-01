alert('JavaScript file is loaded');

function initializeScript() {
    console.log('Initializing script...');

    function updateLegendVisibility() {
        var layersControl = document.querySelector('.leaflet-control-layers-list');
        var landslideLegendContainer = document.querySelector("#landslide-legend-container");
        var populationLegendContainer = document.querySelector("#population-legend-container");
        var riskIndicatorBuildingsLegendContainer = document.querySelector("#risk-indicator-buildings-legend-container");
        var riskIndicatorCulturalHeritageLegendContainer = document.querySelector("#risk-indicator-cultural-heritage-legend-container");
        var riskIndicatorFamiliesLegendContainer = document.querySelector("#risk-indicator-families-legend-container");
        var riskIndicatorIndustriesAndServicesLegendContainer = document.querySelector("#risk-indicator-industries-and-services-legend-container");
        var riskIndicatorPopulationLegendContainer = document.querySelector("#risk-indicator-population-legend-container");
        var riskIndicatorTerritoryLegendContainer = document.querySelector("#risk-indicator-territory-legend-container");

        if (!layersControl || !landslideLegendContainer || !populationLegendContainer || !riskIndicatorBuildingsLegendContainer || !riskIndicatorCulturalHeritageLegendContainer || !riskIndicatorFamiliesLegendContainer || !riskIndicatorIndustriesAndServicesLegendContainer || !riskIndicatorPopulationLegendContainer || !riskIndicatorTerritoryLegendContainer) {
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

        var riskIndicatorBuildingsLayerInput = Array.from(layersControl.querySelectorAll('input'))
            .find(function(input) {
                return input.nextElementSibling && input.nextElementSibling.textContent.trim() === 'Risk Indicator Buildings';
            });

        var riskIndicatorCulturalHeritageLayerInput = Array.from(layersControl.querySelectorAll('input'))
            .find(function(input) {
                return input.nextElementSibling && input.nextElementSibling.textContent.trim() === 'Risk Indicator Cultural Heritage';
            });

        var riskIndicatorFamiliesLayerInput = Array.from(layersControl.querySelectorAll('input'))
            .find(function(input) {
                return input.nextElementSibling && input.nextElementSibling.textContent.trim() === 'Risk Indicator Families';
            });

        var riskIndicatorIndustriesAndServicesLayerInput = Array.from(layersControl.querySelectorAll('input'))
            .find(function(input) {
                return input.nextElementSibling && input.nextElementSibling.textContent.trim() === 'Risk Indicator Industries and Services';
            });

        var riskIndicatorPopulationLayerInput = Array.from(layersControl.querySelectorAll('input'))
            .find(function(input) {
                return input.nextElementSibling && input.nextElementSibling.textContent.trim() === 'Risk Indicator Population';
            });

        var riskIndicatorTerritoryLayerInput = Array.from(layersControl.querySelectorAll('input'))
            .find(function(input) {
                return input.nextElementSibling && input.nextElementSibling.textContent.trim() === 'Risk Indicator Territory';
            });

        console.log('landslideLayerInput:', landslideLayerInput);
        console.log('populationLayerInput:', populationLayerInput);
        console.log('riskIndicatorBuildingsLayerInput:', riskIndicatorBuildingsLayerInput);
        console.log('riskIndicatorCulturalHeritageLayerInput:', riskIndicatorCulturalHeritageLayerInput);
        console.log('riskIndicatorFamiliesLayerInput:', riskIndicatorFamiliesLayerInput);
        console.log('riskIndicatorIndustriesAndServicesLayerInput:', riskIndicatorIndustriesAndServicesLayerInput);
        console.log('riskIndicatorPopulationLayerInput:', riskIndicatorPopulationLayerInput);
        console.log('riskIndicatorTerritoryLayerInput:', riskIndicatorTerritoryLayerInput);

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

        if (riskIndicatorBuildingsLayerInput && riskIndicatorBuildingsLayerInput.checked) {
            riskIndicatorBuildingsLegendContainer.style.display = 'block';
            console.log('Risk Indicator Buildings Legend shown');
        } else {
            riskIndicatorBuildingsLegendContainer.style.display = 'none';
            console.log('Risk Indicator Buildings Legend hidden');
        }

        if (riskIndicatorCulturalHeritageLayerInput && riskIndicatorCulturalHeritageLayerInput.checked) {
            riskIndicatorCulturalHeritageLegendContainer.style.display = 'block';
            console.log('Risk Indicator Cultural Heritage Legend shown');
        } else {
            riskIndicatorCulturalHeritageLegendContainer.style.display = 'none';
            console.log('Risk Indicator Cultural Heritage Legend hidden');
        }

        if (riskIndicatorFamiliesLayerInput && riskIndicatorFamiliesLayerInput.checked) {
            riskIndicatorFamiliesLegendContainer.style.display = 'block';
            console.log('Risk Indicator Families Legend shown');
        } else {
            riskIndicatorFamiliesLegendContainer.style.display = 'none';
            console.log('Risk Indicator Families Legend hidden');
        }

        if (riskIndicatorIndustriesAndServicesLayerInput && riskIndicatorIndustriesAndServicesLayerInput.checked) {
            riskIndicatorIndustriesAndServicesLegendContainer.style.display = 'block';
            console.log('Risk Indicator Industries and Services Legend shown');
        } else {
            riskIndicatorIndustriesAndServicesLegendContainer.style.display = 'none';
            console.log('Risk Indicator Industries and Services Legend hidden');
        }

        if (riskIndicatorPopulationLayerInput && riskIndicatorPopulationLayerInput.checked) {
            riskIndicatorPopulationLegendContainer.style.display = 'block';
            console.log('Risk Indicator Population Legend shown');
        } else {
            riskIndicatorPopulationLegendContainer.style.display = 'none';
            console.log('Risk Indicator Population Legend hidden');
        }

        if (riskIndicatorTerritoryLayerInput && riskIndicatorTerritoryLayerInput.checked) {
            riskIndicatorTerritoryLegendContainer.style.display = 'block';
            console.log('Risk Indicator Territory Legend shown');
        } else {
            riskIndicatorTerritoryLegendContainer.style.display = 'none';
            console.log('Risk Indicator Territory Legend hidden');
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
