<?xml version="1.0" encoding="UTF-8"?>
<StyledLayerDescriptor xmlns="http://www.opengis.net/sld" xmlns:gml="http://www.opengis.net/gml" xmlns:ogc="http://www.opengis.net/ogc" version="1.0.0" xmlns:sld="http://www.opengis.net/sld">
  <UserLayer>
    <sld:LayerFeatureConstraints>
      <sld:FeatureTypeConstraint/>
    </sld:LayerFeatureConstraints>
    <sld:UserStyle>
      <sld:Name>ita_ppp_2020</sld:Name>
      <sld:FeatureTypeStyle>
        <sld:Rule>
          <sld:RasterSymbolizer>
            <sld:ChannelSelection>
              <sld:GrayChannel>
                <sld:SourceChannelName>1</sld:SourceChannelName>
              </sld:GrayChannel>
            </sld:ChannelSelection>
            <sld:ColorMap type="intervals">
              <sld:ColorMapEntry color="#fcfbfd" label="&lt;= 0.0000" quantity="0"/>
              <sld:ColorMapEntry color="#dcdbec" label="0.0000 - 0.0008" quantity="0.00075574362911833004"/>
              <sld:ColorMapEntry color="#a39fcb" label="0.0008 - 0.0128" quantity="0.0128476416950116"/>
              <sld:ColorMapEntry color="#6a51a3" label="0.0128 - 0.1255" quantity="0.12545344243364301"/>
              <sld:ColorMapEntry color="#3f007d" label="> 0.1255" quantity="1000000"/>
            </sld:ColorMap>
          </sld:RasterSymbolizer>
        </sld:Rule>
      </sld:FeatureTypeStyle>
    </sld:UserStyle>
  </UserLayer>
</StyledLayerDescriptor>