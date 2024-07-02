<?xml version="1.0" encoding="UTF-8"?>
<StyledLayerDescriptor xmlns="http://www.opengis.net/sld" version="1.0.0" xmlns:gml="http://www.opengis.net/gml" xmlns:sld="http://www.opengis.net/sld" xmlns:ogc="http://www.opengis.net/ogc">
  <UserLayer>
    <sld:LayerFeatureConstraints>
      <sld:FeatureTypeConstraint/>
    </sld:LayerFeatureConstraints>
    <sld:UserStyle>
      <sld:Name>landslide_hazard_map</sld:Name>
      <sld:FeatureTypeStyle>
        <sld:Rule>
          <sld:RasterSymbolizer>
            <sld:ChannelSelection>
              <sld:GrayChannel>
                <sld:SourceChannelName>1</sld:SourceChannelName>
              </sld:GrayChannel>
            </sld:ChannelSelection>
            <sld:ColorMap type="values">
              <sld:ColorMapEntry color="#f3ca4e" quantity="1" label="Moderate P1"/>
              <sld:ColorMapEntry color="#e4681e" quantity="2" label="Medium P2"/>
              <sld:ColorMapEntry color="#e30617" quantity="3" label="High P3"/>
              <sld:ColorMapEntry color="#720002" quantity="4" label="Very high P4"/>
              <sld:ColorMapEntry color="#fefd7e" quantity="5" label="Attention zones AA"/>
            </sld:ColorMap>
            <!-- Removed VendorOption element -->
            <!-- <sld:VendorOption name="brightness">0.505882</sld:VendorOption> -->
          </sld:RasterSymbolizer>
        </sld:Rule>
      </sld:FeatureTypeStyle>
    </sld:UserStyle>
  </UserLayer>
</StyledLayerDescriptor>