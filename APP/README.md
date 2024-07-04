## V1.0.0 Update suggestions

1. **update leaflet_map function in figures.py**

    Try using the Folium tool to create maps to achieve the same functionality instead of dash_leaflet. You can find related code hints in the Slides_notebooks folder under practice_5_data_plotting on webeep:

    ```sh
plot polygons and make a chloropeth map according to an attribute
m = folium.Map(location=[45.46, 9.19], zoom_start=11, tiles='CartoDB positron')
folium.TileLayer('OpenStreetMap', name='OpenStreetMap', attr='OpenStreetMap').add_to(m)
folium.GeoJson(milan).add_to(m)
folium.Choropleth(
    geo_data= milan.to_json(),
    data=milan,
    columns=[milan.index,'AREA'],
    key_on='feature.id',
    fill_color='YlGn',
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name='Area',
    name='Milano Zones'
).add_to(m)
folium.LayerControl().add_to(m)
m
    ```

2. **Simplifying Italy's Risk Indicator Mapping with Folium**

Add a new parameter `risk_indicator_gdf` to the `leaflet_map` function. `risk_indicator_gdf` is data that has already been prepared in the dashboard. This data contains risk indicators for various regions in Italy, such as population and buildings. The current method involves storing this data locally, styling it using QGIS, then publishing it on GeoServer, and finally fetching the map using dash_leaflet. 

Try using the Folium module to achieve the same functionality directly using the new parameter `risk_indicator_gdf` to create the map. This way, the use of GeoServer can be avoided, simplifying the user's workflow.

3. **Adding Dropdown for Color Styles**

    If you can successfully use Folium to draw the Risk Indicator Map, try adding a new dropdown component. The dropdown content will be different color styles (e.g., fill_color='YlGn' parameter). This way, users can personalize the color used in the Risk Indicator Map.
 
4. **Enhancing User Interaction with Folium: Highlighting Boundaries and Displaying Risk Indices on Click**

    Use the Folium module to add more interactive features for users. For example, when a user clicks on a relevant area on the map, the boundary of that area will be highlighted, and a popup will display information such as the landslide risk index for that area.

