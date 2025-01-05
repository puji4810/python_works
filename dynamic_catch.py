import requests
import json
import re


def fetch_cpu_data():
    url = "https://cpu.zol.com.cn/router.php"
    params = {
        "c": "Tianti_Cpu",
        "a": "GetList",
        "callback": "$.getAllList"
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        # 提取 JSON 数据
        jsonp_text = response.text
        match = re.search(r"\$\.\w+\((.*)\)", jsonp_text)  # 提取括号中的 JSON 数据
        if match:
            json_data = json.loads(match.group(1))  # 转换为字典
            return json_data
        else:
            print("未能提取 JSON 数据")
            return None
    else:
        print(f"请求失败，状态码: {response.status_code}")
        return None


def parse_and_print_cpu_data(data):
    # 解析综合性能数据
    colligate = data.get("colligate", [])
    print("综合性能排名：")
    for cpu in colligate:
        print(
            f"排名: {cpu['rank']}, 型号: {cpu['model']}, 得分: {cpu['score']}, 厂商: {'Intel' if cpu['firm'] == '1' else 'AMD'}")
    print("\n")

    # 解析多核性能数据
    multi_core = data.get("multiCore", [])
    print("多核性能排名：")
    for cpu in multi_core:
        print(f"排名: {cpu['rank']}, 型号: {cpu['model']}, 得分: {cpu['score']}")
    print("\n")

    # 解析单核性能数据
    single_core = data.get("singleCore", [])
    print("单核性能排名：")
    for cpu in single_core:
        print(f"排名: {cpu['rank']}, 型号: {cpu['model']}, 得分: {cpu['score']}")
    print("\n")

    # 解析游戏性能数据
    game = data.get("game", [])
    print("游戏性能排名：")
    for cpu in game:
        print(f"排名: {cpu['rank']}, 型号: {cpu['model']}, 得分: {cpu['score']}")
    print("\n")


if __name__ == "__main__":
    # 获取 JSON 数据
    cpu_data = fetch_cpu_data()
    if cpu_data:
        # 解析并打印数据
        parse_and_print_cpu_data(cpu_data)
