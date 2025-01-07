import url_parse as up
import save_data as sd
from dash import Dash, dcc, html, dash_table
import pandas as pd
import plotly.express as px


def dash_init():
    
    """
    初始化 Dash 应用程序并设置包含各种可视化的布局。
    返回：
        app (Dash): Dash 应用程序实例。
        df (DataFrame): 包含 CPU 数据的 DataFrame。
    布局包括：
        - 标题头。
        - 显示 CPU 数据的数据表。
        - 显示 CPU 综合排名的柱状图。
        - 比较单核、多核和游戏排名的散点图。
    数据处理：
        - 获取 CPU 列表和 JSON 格式的数据。
        - 解析和处理 CPU 数据。
        - 确保数据类型正确，并用 0 替换 NaN 值。
        - 创建 DataFrame 的副本，并为可视化目的替换特定排名。
    """

    app = Dash(__name__)

    cpu_list_json = up.fetch_cpu_list_json()
    if cpu_list_json:
        cpu_data, proId = up.parse_cpu_list(cpu_list_json)
        cpu_data_json = up.fetch_cpu_data_json(proId)
        df = up.show_cpu_data(cpu_data, cpu_data_json)

    # 确保数据类型正确，并用填充值替代 NaN
    df["单核排名"] = pd.to_numeric(df["单核排名"], errors="coerce").fillna(0)
    df["多核排名"] = pd.to_numeric(df["多核排名"], errors="coerce").fillna(0)
    df["游戏排名"] = pd.to_numeric(df["游戏排名"], errors="coerce").fillna(0)
    df["综合排名"] = pd.to_numeric(df["综合排名"], errors="coerce").fillna(0)
    df["评分"] = pd.to_numeric(df["评分"], errors="coerce").fillna(0)

    replaced_df = df.copy()
    replaced_df['多核排名'] = replaced_df['多核排名'].replace(0, 999)
    replaced_df['单核排名'] = replaced_df['单核排名'].replace(0, 999)
    replaced_df['游戏排名'] = replaced_df['游戏排名'].replace(0, 999)

    app.layout = html.Div([
        html.H1("CPU 数据可视化仪表盘", style={"textAlign": "center"}),

        # 数据表格
        html.H2("CPU 数据表"),
        dash_table.DataTable(
            id='cpu-table',
            columns=[{"name": i, "id": i} for i in df.columns],
            data=df.to_dict('records'),
            style_table={'overflowX': 'auto'},
            style_cell={'textAlign': 'left'},
        ),

        # 图表1：综合排名柱状图
        html.H2("综合排名"),
        dcc.Graph(
            id="colligate-bar",
            figure=px.bar(
                df,
                x="评分",
                y="产品名称",
                title="CPU 综合排名",
                orientation="h",
                height=600
            ).update_xaxes(range=[0, df['评分'].max()]).update_yaxes(autorange='reversed')
        ),

        # 图表2：单核、多核、游戏排名散点图
        html.H2("单核、多核、游戏排名对比"),
        dcc.Graph(
            id="ranking-scatter",
            figure=px.scatter(
                replaced_df,
                x="单核排名",
                y="多核排名",
                size=40 - replaced_df["游戏排名"].replace(999, 35),
                color="厂商",
                hover_name="产品名称",
                title="单核 vs 多核排名",
            ).update_xaxes(range=[150, 0]).update_yaxes(range=[150, 0])
        )
    ])

    return app, df

if __name__ == '__main__':
    app, df = dash_init()
    sd.save_as_excel(df)
    sd.matplotlib_analysis(df)
    app.run_server(debug=True)
