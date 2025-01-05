
import requests
import json
import re


def fetch_cpu_list_json():
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


def parse_cpu_list(data):
    # 定义字段名
    field_map = {
        "colligate": "综合",
        "multiCore": "多核",
        "singleCore": "单核",
        "game": "游戏"
    }
    unique_proIds = {}

    # 遍历每个字段并提取对应数据
    for field, title in field_map.items():
        print(f"\n--- {title} 排名 ---")
        field_data = data.get(field, [])
        if not field_data:
            print(f"{title} 数据为空或不存在")
            continue

        for cpu in field_data:
            unique_proIds = cpu['proId']
            print(f"proId: {cpu['proId']}, 型号: {cpu['model']}, 得分: {cpu.get('score', '无')}, 排名: {cpu.get('rank', '无')}, 厂商: {'Intel' if cpu.get('firm') == '1' else 'AMD'}")
    return unique_proIds


if __name__ == "__main__":
    cpu_list_data = fetch_cpu_list_json()
    if cpu_list_data:
        unique_proIds = parse_cpu_list(cpu_list_data)
        print(f"\n共有 {len(unique_proIds)} 个 CPU 产品")
