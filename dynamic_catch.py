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
    # 定义字段名
    fields = ["综合", "多核", "单核", "游戏"]

    # 遍历每个字段并提取对应数据
    for field in fields:
        print(f"\n--- {field} 排名 ---")
        field_data = data.get(field, [])
        if not field_data:
            print(f"{field} 数据为空或不存在")
            continue

        for cpu in field_data:
            print(f"proId: {cpu['proId']}, 型号: {cpu['model']}, 得分: {cpu.get('score', '无')}, 排名: {cpu.get('rank', '无')}, 厂商: {'Intel' if cpu.get('firm') == '1' else 'AMD'}")


if __name__ == "__main__":
    # 获取 JSON 数据
    cpu_data = fetch_cpu_data()
    if cpu_data:
        # 解析并打印数据
        parse_and_print_cpu_data(cpu_data)
