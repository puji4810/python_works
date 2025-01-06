
import requests
import json
import re
from bs4 import BeautifulSoup
import pandas as pd

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Referer": "https://cpu.zol.com.cn/",  # 来源页面
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Connection": "keep-alive",
}


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
    cpu_data = {}
    unique_proIds = set()

    # 遍历每个字段并提取对应数据
    for field, title in field_map.items():
        # print(f"\n--- {title} 排名 ---")
        field_data = data.get(field, [])
        if not field_data:
            print(f"{title} 数据为空或不存在")
            continue

        for cpu in field_data:
            proId = cpu['proId']
            if proId not in cpu_data:
                cpu_data[proId] = {
                    "proId": proId,
                    "model": cpu['model'],
                    "firm": cpu.get('firm', "未知厂商"),
                    "rankings": {}  # 用于存储每个分类的排名
                }
            # 记录当前字段的排名
            cpu_data[proId]["rankings"][title] = cpu.get("rank", "无")
            unique_proIds.add(cpu['proId'])
            # print(f"proId: {cpu['proId']}, 型号: {cpu['model']}, 得分: {cpu.get('score', '无')}, 排名: {cpu.get('rank', '无')}, 厂商: {'Intel' if cpu.get('firm') == '1' else 'AMD'}")
    return cpu_data, unique_proIds


def fetch_cpu_data_json(product_ids):
    base_url = "https://cpu.zol.com.cn/router.php"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    cpu_data_list_json = []

    for pro_id in product_ids:
        params = {
            "c": "Tianti_Cpu",
            "a": "GetProInfo",
            "proId": pro_id,
            "type": "undefined",
            "callback": "$.renderItemfunction"
        }
        response = requests.get(base_url, headers=headers, params=params)
        if response.status_code == 200:
            jsonp_text = response.text
            match = re.search(r"\$\.\w+\((.*)\)", jsonp_text)
            if match:
                json_data = json.loads(match.group(1))
                cpu_data_list_json.append(json_data)
        else:
            print(f"请求失败，状态码：{response.status_code}")

    return cpu_data_list_json


def show_cpu_data(cpu_data, cpu_data_json):
    data_list = []
    for cpu_json in cpu_data_json:
        # 从 param 提取基本信息
        param = cpu_json.get("param", {})
        proId = param.get("proId", "未知产品 ID")
        product_name = param.get("model", "未知产品")
        series = param.get("series", "未知系列")
        core = param.get("core", "未知核心")
        frequency = param.get("frequency", "未知主频")
        core_thread = param.get("coreThread", "未知核心/线程")
        tdp = param.get("tdp", "未知功耗")
        graphics = param.get("graphics", "未知集成显卡")
        score = param.get("score", "未知评分")

        # 从 jd 提取价格
        jd = cpu_json.get("jd", {})
        price = jd.get("price", "价格未知")

        this_cpu = cpu_data.get(proId, {})
        if this_cpu:
            firm = "Intel" if this_cpu.get("firm") == "1" else "AMD"
            rankings = this_cpu.get("rankings", {})
            single_rank = rankings.get("单核", "无")
            multi_rank = rankings.get("多核", "无")
            game_rank = rankings.get("游戏", "无")
            colligate_rank = rankings.get("综合", "无")

            # 保存到 data_list
            data_list.append({
                "产品名称": product_name,
                "系列": series,
                "核心代号": core,
                "主频": frequency,
                "核心/线程": core_thread,
                "功耗": tdp,
                "集成显卡": graphics,
                "评分": score,
                "价格": price,
                "厂商": firm,
                "单核排名": single_rank,
                "多核排名": multi_rank,
                "游戏排名": game_rank,
                "综合排名": colligate_rank
            })
    df = pd.DataFrame(data_list)
    df['综合排名'] = pd.to_numeric(df['综合排名'], errors='coerce')
    df = df.sort_values(by='综合排名', ascending=True)
    return df


def url_parse_goods(url):
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        products = []
        items = soup.find_all('p')
        for item in items:
            name_tag = item.find('a', title=True)
            if name_tag:
                name = name_tag['title']
                price_tag = item.find_next_sibling('p')
                if price_tag and price_tag.find('em', class_='price'):
                    price = price_tag.find('em', class_='price').text.strip()
                    if price != '价格面议':
                        products.append({"商品名称": name, "价格": price})
        for product in products:
            print(f"商品名称: {product['商品名称']}, 价格: {product['价格']}")
    else:
        print("请求失败，状态码：", response.status_code)


def find_page(count, url="https://detail.zol.com.cn/cpu"):
    if count != 0:
        url = f"{url}/{count}.html"
    url_parse_goods(url)


def find_pages(count, url="https://detail.zol.com.cn/cpu"):
    for i in range(0, count):
        print("page", i + 1)
        if i != 0:
            url = f"{url}/{i + 1}.html"
        url_parse_goods(url)


if __name__ == '__main__':
    # find_pages(10)
    proId = []
    cpu_list_json = fetch_cpu_list_json()
    if cpu_list_json:
        cpu_data, proId = parse_cpu_list(cpu_list_json)

    cpu_data_json = fetch_cpu_data_json(proId)
    show_cpu_data(cpu_data, cpu_data_json)
