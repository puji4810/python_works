import matplotlib.pyplot as plt
import pandas as pd


def save_as_excel(df):
    """
    将给定的 DataFrame 保存为 Excel 文件。
    参数:
    df (pandas.DataFrame): 要保存的 DataFrame。
    返回:
    无
    副作用:
    将 DataFrame 保存到当前工作目录中的名为 'cpu_data.xlsx' 的文件。
    打印一条消息，指示数据已保存。
    """

    df.to_excel("cpu_data.xlsx", index=False)
    print("数据已保存为 Excel 文件")


def matplotlib_analysis(df):
    """
    生成并保存两个基于提供的 DataFrame 的图表。
    参数:
    df (pandas.DataFrame): 包含以下列的 DataFrame:
        - "评分": 用于直方图的评分。
        - "单核排名": 用于散点图的单核排名。
        - "多核排名": 用于散点图的多核排名。
        - "游戏排名": 用于散点图的游戏排名。
    该函数创建并保存以下图表:
    1. "评分" 列的直方图，保存为 "ranking_hist.png"。
    2. "单核排名" 对 "多核排名" 的散点图，"游戏排名" 作为颜色标度，保存为 "ranking_scatter.png"。
    两个图表都使用特定字体作为标题和标签，并包含网格线以提高可读性。
    """

    plt.figure(figsize=(10, 6))
    plt.hist(df["评分"], bins=20, color='skyblue', edgecolor='black')
    plt.title("CPU 评分分布直方图")
    plt.xlabel("评分")
    plt.ylabel("数量")
    plt.grid(axis='y', linestyle='--', alpha=0.8)
    plt.savefig("ranking_hist.png")
    print("评分直方图已保存")

    plt.figure(figsize=(10, 6))
    scatter = plt.scatter(df["单核排名"], df["多核排名"], c=df["游戏排名"],
                          cmap="coolwarm", alpha=0.8)
    plt.title("CPU 单核、多核、游戏排名散点图")
    plt.xlabel("单核排名")
    plt.ylabel("多核排名")
    colorbar = plt.colorbar(scatter)
    colorbar.set_label("游戏排名")
    plt.grid(True, linestyle='--', alpha=0.8)
    plt.savefig("ranking_scatter.png")
    print("单核、多核、游戏排名散点图已保存")


if __name__ == '__main__':

    # 测试
    data = {
        "评分": [80, 90, 70, 85, 95, 65, 75],
        "单核排名": [1, 2, 3, 4, 5, 6, 7],
        "多核排名": [7, 6, 5, 4, 3, 2, 1],
        "游戏排名": [70, 75, 65, 80, 85, 90, 95]
    }

    df = pd.DataFrame(data)

    save_as_excel(df)
    matplotlib_analysis(df)
