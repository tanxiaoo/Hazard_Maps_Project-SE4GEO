import numpy as np
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
import dash_leaflet as dl
from dash import dcc, html, Dash, Input, Output

from dash import html


def create_context_data_display(data):
    keys_to_exclude = ['Population at risk of Landslides', 'Population at risk of Floods']
    # 确保数据是单个值而不是 Series，并保留到整数
    data = {key: (int(value.tolist()[0]) if isinstance(value, pd.Series) else int(value)) for key, value in data.items()
            if key not in keys_to_exclude}

    # 数据项
    data_items = list(data.items())

    # 颜色参数
    color = 'rgba(128, 0, 128, 0.2)'  # 透明的紫色

    return html.Div([

        # 外层div，左右分布
        html.Div([
            # 第一个div，宽度40%，高度100%，使用flex-grow填充高度
            html.Div([
                html.Span(f"{data_items[0][1]:,} km²", style={'font-size': '18px', 'font-weight': 'bold','color':'white'}),
                html.P(data_items[0][0].replace(' (km²)', ''), style={'font-size': '14px','color':'white'}),
            ], style={'width': '40%', 'display': 'flex', 'flex-direction': 'column', 'justify-content': 'center',
                      'background-color': color, 'flex-grow': '1', 'text-align': 'center', 'padding': '10px'}),

            # 右侧包含三个div的容器，宽度60%
            html.Div([
                # 第二个div，宽度100%，高度33.33%，里面均匀水平分布三个子div
                html.Div([
                    html.Div([
                        html.Span(f"{data_items[1][1]:,}", style={'font-size': '18px', 'font-weight': 'bold'}),
                        html.P(data_items[1][0], style={'font-size': '14px'}),
                    ], style={'flex': '1', 'padding': '10px', 'text-align': 'center', 'background-color': color}),
                    html.Div([
                        html.Span(f"{data_items[2][1]:,}", style={'font-size': '18px', 'font-weight': 'bold'}),
                        html.P(data_items[2][0], style={'font-size': '14px'}),
                    ], style={'flex': '1', 'padding': '10px', 'text-align': 'center', 'background-color': color}),
                    html.Div([
                        html.Span(f"{data_items[3][1]:,}", style={'font-size': '18px', 'font-weight': 'bold'}),
                        html.P(data_items[3][0], style={'font-size': '14px'}),
                    ], style={'flex': '1', 'padding': '10px', 'text-align': 'center', 'background-color': color}),
                ], style={'width': '100%', 'height': '33.33%', 'display': 'flex', 'box-sizing': 'border-box', 'gap': '5px'}),

                # 第三个div，宽度100%，高度33.33%，里面水平分布两个子div
                html.Div([
                    html.Div([
                        html.Span(f"{data_items[4][1]:,}", style={'font-size': '18px', 'font-weight': 'bold'}),
                        html.P(data_items[4][0], style={'font-size': '14px'}),
                    ], style={'flex': '1', 'padding': '10px', 'text-align': 'center', 'background-color': color}),
                    html.Div([
                        html.Span(f"{data_items[5][1]:,}", style={'font-size': '18px', 'font-weight': 'bold'}),
                        html.P(data_items[5][0], style={'font-size': '14px'}),
                    ], style={'flex': '1', 'padding': '10px', 'text-align': 'center', 'background-color': color}),
                ], style={'width': '100%', 'height': '33.33%', 'display': 'flex', 'box-sizing': 'border-box', 'gap': '5px'}),

                # 第四个div，宽度100%，高度33.33%，里面均匀水平分布三个子div
                html.Div([
                    html.Div([
                        html.Span(f"{data_items[6][1]}%", style={'font-size': '18px', 'font-weight': 'bold'}),
                        html.P(data_items[6][0].replace('%', ''), style={'font-size': '14px'}),
                    ], style={'flex': '1', 'padding': '10px', 'text-align': 'center', 'background-color': color}),
                    html.Div([
                        html.Span(f"{data_items[7][1]}%", style={'font-size': '18px', 'font-weight': 'bold'}),
                        html.P(data_items[7][0].replace('%', ''), style={'font-size': '14px'}),
                    ], style={'flex': '1', 'padding': '10px', 'text-align': 'center', 'background-color': color}),
                    html.Div([
                        html.Span(f"{data_items[8][1]}%", style={'font-size': '18px', 'font-weight': 'bold'}),
                        html.P(data_items[8][0].replace('%', ''), style={'font-size': '14px'}),
                    ], style={'flex': '1', 'padding': '10px', 'text-align': 'center', 'background-color': color}),
                ], style={'width': '100%', 'height': '33.33%', 'display': 'flex', 'box-sizing': 'border-box', 'gap': '5px'}),

            ], style={'width': '60%', 'display': 'flex', 'flex-direction': 'column',
                      'justify-content': 'space-between', 'gap': '5px'}),

        ], style={'display': 'flex', 'height': '100%', 'gap': '5px'}),

    ], style={'max-width': '100%'})







def create_stacked_bar_chart(landslides_df):
    fig = go.Figure()

    # landslides_df = pd.concat([landslides_df.head(5), landslides_df.tail(1)])
    landslides_df = landslides_df.head(5)

    categories = landslides_df['Category'].unique()

    columns = landslides_df.columns.tolist()[1:]  # 排除'Category'列

    # 定义颜色序列，匹配参考图
    colors = ['#FF4500', '#FF6347', '#FFD700', '#ADFF2F', '#32CD32']

    def extract_values_percent(cell):
        value, percent = cell.split(' (')
        return float(value), float(percent.rstrip('%)'))

    for i, category in enumerate(categories):
        cat_data = landslides_df[landslides_df['Category'] == category].iloc[0]
        cell_values = [cat_data[col] for col in columns]  # 获取每个单元格的原始值
        y_values = [extract_values_percent(cat_data[col])[1] for col in columns]  # 仅使用百分数值
        fig.add_trace(go.Bar(
            y=columns,  # 将原来的 x 改为 y
            x=y_values,  # 将原来的 y 改为 x
            name=category,
            marker_color=colors[i % len(colors)],  # 使用颜色序列
            text=[f"{percent}%" for percent in y_values],  # 显示百分比
            textposition='auto',
            orientation='h', # 设置为水平条形图
            hovertemplate = '<b>%{y}</b><br>%{customdata}',  # 显示列名、百分比和原始值
            customdata = cell_values,  # 添加原始值到 hover 数据
        ))

    fig.update_layout(
        barmode='stack',
        yaxis=dict(
            categoryorder='category ascending',
            tickmode='array',
            tickvals=columns,
            ticktext=['<b>{}</b>'.format(col) for col in columns],  # 加粗标签并转换成HTML
            tickangle=0,  # 确保标签是水平的
            automargin=True,
            tickfont=dict(size=12),  # 设置字体大小
            side='left',
            anchor='free',
            position=1, # 调整这个值可以精确控制标签的左右位置
            color='#fff',
        ),
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=-0.2,
            xanchor='center',
            x=0.5,
            traceorder = 'normal',
    ),
        margin=dict(l=0, r=0, t=0, b=100),  # 调整边距
        plot_bgcolor='rgba(0,0,0,0)',  # 设置图表背景颜色透明
        paper_bgcolor='rgba(0,0,0,0)',  # 设置纸张背景颜色透明
    )

    fig.update_traces(
        texttemplate='%{text}',  # 使用百分比作为标签
        textposition='inside',  # 标签在条形内部
    )

    return fig


def get_Choropleth(df, geo_data, arg, marker_opacity,
                   marker_line_width, marker_line_color, fig=None):
    if fig is None:
        fig = go.Figure()

    fig.add_trace(
        go.Choroplethmapbox(
            geojson=geo_data,
            locations=df['id'],  # 使用 'id' 列
            featureidkey="properties.id",
            colorscale=arg['colorscale'],
            z=arg['z_vec'],
            zmin=arg['min_value'],
            zmax=arg['max_value'],
            text=arg['text_vec'],
            hoverinfo="text",
            marker_opacity=marker_opacity,
            marker_line_width=marker_line_width,
            marker_line_color=marker_line_color,
            colorbar_title=arg['title'],
        )
    )
    return fig

def leaflet_map(region, regions_geo_data, highlight_geojson):
    # 获取区域的配置
    cfg = plotly_config.get(region, plotly_config['Italy'])

    # 高亮区域的样式
    highlight_style = {
        'fillColor': 'red',
        'color': 'red',
        'weight': 3,
        'dashArray': '5, 5',
        'fillOpacity': 0.2
    }

    # 确保 highlight_geojson 是有效的 FeatureCollection
    if not highlight_geojson or 'features' not in highlight_geojson or not highlight_geojson['features']:
        highlight_geojson = {'type': 'FeatureCollection', 'features': []}

    # 全局 GeoJSON 图层的样式
    geojson_style = {
        'fillColor': '#32CD32',  # 填充颜色
        'color': '#32CD32',  # 边界颜色
        'weight': 1,  # 边界宽度
        'fillOpacity': 0.01  # 填充透明度
    }

    # WMS 图层的图例 URL
    landslide_legend_url = "http://localhost:8080/geoserver/se4g24/wms?REQUEST=GetLegendGraphic&FORMAT=image/png&WIDTH=20&HEIGHT=20&LAYER=se4g24:landslide_hazard_map"
    population_legend_url = "http://localhost:8080/geoserver/se4g24/wms?REQUEST=GetLegendGraphic&FORMAT=image/png&WIDTH=20&HEIGHT=20&LAYER=se4g24:ita_ppp_2020"

    # 生成地图
    leaflet_map = dl.Map(center=cfg['centre'], zoom=cfg['zoom'], children=[
        dl.LayersControl(collapsed=True, children=[
            dl.BaseLayer(dl.TileLayer(url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"), name="OpenStreetMap", checked=True),
            dl.BaseLayer(dl.TileLayer(url="https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png"), name="Carto Positron"),
            dl.BaseLayer(dl.TileLayer(url="https://server.arcgisonline.com/ArcGIS/rest/services/World_Topo_Map/MapServer/tile/{z}/{y}/{x}"), name="Esri Topographic"),
            dl.BaseLayer(dl.TileLayer(url="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}"), name="Esri World Imagery"),
            dl.Overlay(dl.WMSTileLayer(
                url="http://localhost:8080/geoserver/se4g24/wms",
                layers="se4g24:landslide_hazard_map",
                format="image/png",
                transparent=True,
                version="1.1.0",
                attribution="GeoServer WMS",
                id="landslide-layer"
            ), name="Landslide Hazard Map", checked=True),
            dl.Overlay(dl.WMSTileLayer(
                url="http://localhost:8080/geoserver/se4g24/wms",
                layers="se4g24:ita_ppp_2020",
                format="image/png",
                transparent=True,
                version="1.1.0",
                attribution="GeoServer WMS",
                id="population-layer"
            ), name="Population Density", checked=True),
            dl.Overlay(
                dl.GeoJSON(data=regions_geo_data, id='geojson-layer', options=dict(style=geojson_style)),
                name="Regions", checked=True
            ),
            dl.Overlay(
                dl.GeoJSON(data=highlight_geojson, id='highlight-layer', options=dict(style=highlight_style)),
                name="Selected Region", checked=True
            ),
        ])
    ], style={'width': '100%', 'height': '100%'})

    # 返回包含地图的 Div
    return html.Div([
        leaflet_map,
        html.Img(id="landslide-legend-container", src=landslide_legend_url, style={
            'position': 'absolute',
            'bottom': '10px',
            'left': '10px',
            'background': 'white',
            'border': '1px solid black',
            'padding': '5px',
            'z-index': '1000',
            'display': 'block'
        }),
        html.Img(id="population-legend-container", src=population_legend_url, style={
            'position': 'absolute',
            'bottom': '10px',
            'left': '10px',
            'background': 'white',
            'border': '1px solid black',
            'padding': '5px',
            'z-index': '1000',
            'display': 'block'
        }),
    ], style={'position': 'relative', 'height': '100%'})





plotly_config = {
    'Italy': {'centre': [41.8719, 12.5674], 'maxp': 99, 'zoom': 5},
    'Piemonte': {'centre': [45.0703, 7.6869], 'maxp': 99, 'zoom': 6.5},
    'Valle d\'Aosta': {'centre': [45.7372, 7.3170], 'maxp': 99, 'zoom': 8},
    'Lombardia': {'centre': [45.4668, 9.1905], 'maxp': 99, 'zoom': 6.5},
    'Trentino-Alto Adige': {'centre': [46.06787, 11.12108], 'maxp': 99, 'zoom': 6.8},  # Updated value
    'Veneto': {'centre': [45.4342, 12.3384], 'maxp': 99, 'zoom': 7},
    'Friuli Venezia Giulia': {'centre': [45.6500, 13.7700], 'maxp': 99, 'zoom': 8},
    'Liguria': {'centre': [44.4056, 8.9463], 'maxp': 99, 'zoom': 7},
    'Emilia-Romagna': {'centre': [44.4949, 11.3426], 'maxp': 99, 'zoom': 6.8},
    'Toscana': {'centre': [43.7696, 11.2558], 'maxp': 99, 'zoom': 7},
    'Umbria': {'centre': [43.1122, 12.3888], 'maxp': 99, 'zoom': 7},
    'Marche': {'centre': [43.6167, 13.5167], 'maxp': 99, 'zoom': 7},
    'Lazio': {'centre': [41.9028, 12.4964], 'maxp': 99, 'zoom': 7},
    'Abruzzo': {'centre': [42.3512, 13.3984], 'maxp': 99, 'zoom': 7},
    'Molise': {'centre': [41.5603, 14.6684], 'maxp': 99, 'zoom': 7},
    'Campania': {'centre': [40.8396, 14.2521], 'maxp': 99, 'zoom': 7},
    'Puglia': {'centre': [41.1258, 16.8666], 'maxp': 99, 'zoom': 7},
    'Basilicata': {'centre': [40.6395, 15.8055], 'maxp': 99, 'zoom': 7},
    'Calabria': {'centre': [39.3088, 16.3464], 'maxp': 99, 'zoom': 7},
    'Sicilia': {'centre': [37.6000, 14.0154], 'maxp': 99, 'zoom': 7},
    'Sardegna': {'centre': [40.1209, 9.0129], 'maxp': 99, 'zoom': 7}
}

