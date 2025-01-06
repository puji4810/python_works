import url_parse as up
from dash import Dash, dcc, html, dash_table
import pandas as pd
import plotly.express as px

# 创建 Dash 应用
app = Dash(__name__)

# 运行之前生成的 DataFrame
cpu_list_json = up.fetch_cpu_list_json()
if cpu_list_json:
    cpu_data, proId = up.parse_cpu_list(cpu_list_json)
    cpu_data_json = up.fetch_cpu_data_json(proId)
    df = up.show_cpu_data(cpu_data, cpu_data_json)  # 获取数据框

# 确保数据类型正确，并用填充值替代 NaN
df["单核排名"] = pd.to_numeric(df["单核排名"], errors="coerce").fillna(0)  # NaN 替换为 0
df["多核排名"] = pd.to_numeric(df["多核排名"], errors="coerce").fillna(0)  # NaN 替换为 0
df["游戏排名"] = pd.to_numeric(df["游戏排名"], errors="coerce").fillna(0)  # NaN 替换为 0
df["综合排名"] = pd.to_numeric(df["综合排名"], errors="coerce").fillna(0)  # NaN 替换为 0
df["评分"] = pd.to_numeric(df["评分"], errors="coerce").fillna(0)  # NaN 替换为 0

replaced_df = df.copy()
replaced_df['多核排名'] = replaced_df['多核排名'].replace(0, 999)
replaced_df['单核排名'] = replaced_df['单核排名'].replace(0, 999)
replaced_df['游戏排名'] = replaced_df['游戏排名'].replace(0, 999)

# 构建 Dash 布局
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
        ).update_xaxes(range=[0, df['评分'].max()]).update_yaxes(autorange='reversed')  # 修改横轴范围
    ),

    # 图表2：单核、多核、游戏排名散点图
    html.H2("单核、多核、游戏排名对比"),
    dcc.Graph(
        id="ranking-scatter",
        figure=px.scatter(
            replaced_df,
            x="单核排名",
            y="多核排名",
            # 将 size 列中的 0 替换为最小点大小
            size=40 - replaced_df["游戏排名"].replace(999, 35),
            color="厂商",
            hover_name="产品名称",
            title="单核 vs 多核排名",
        ).update_xaxes(range=[150, 0]).update_yaxes(range=[150, 0])
    )
])

# 运行应用
if __name__ == '__main__':
    app.run_server(debug=True)
