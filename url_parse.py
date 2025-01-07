
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
    """
    从指定的 URL 获取 CPU 列表的 JSON 数据。

    该函数向 URL "https://cpu.zol.com.cn/router.php" 发送带有特定参数和头部的 GET 请求。
    它期望一个 JSONP 响应并从中提取 JSON 数据。

    返回:
        dict: 如果请求成功且 JSON 数据提取成功，则返回包含 JSON 数据的字典。
        None: 如果请求失败或无法提取 JSON 数据。

    异常:
        None

    示例:
    >>> cpu_list = fetch_cpu_list_json()
    >>> if cpu_list:
    >>>     print(cpu_list)
    """
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
    """
    解析 CPU 数据列表并按 CPU ID 组织数据。
    
    参数:
        data (dict): 包含按字段分类的 CPU 数据的字典，例如 "colligate", "multiCore", 
                     "singleCore", 和 "game"。每个字段映射到一个字典列表，每个字典
                     代表一个 CPU，包含 'proId', 'model', 'firm', 'rank' 等键。
    
    返回:
        tuple: 包含以下内容的元组:
            - cpu_data (dict): 一个字典，每个键是 CPU ID (proId)，值是另一个字典，
                               包含 'proId', 'model', 'firm', 和 'rankings' 键。
                               'rankings' 键映射到另一个字典，标题为键，排名为值。
            - unique_proIds (set): 数据中找到的唯一 CPU ID (proId) 集合。
    """
    field_map = {
        "colligate": "综合",
        "multiCore": "多核",
        "singleCore": "单核",
        "game": "游戏"
    }
    cpu_data = {}
    unique_proIds = set()

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
                    "rankings": {}
                }
            cpu_data[proId]["rankings"][title] = cpu.get("rank", "无")
            unique_proIds.add(cpu['proId'])
            # print(f"proId: {cpu['proId']}, 型号: {cpu['model']}, 得分: {cpu.get('score', '无')}, 排名: {cpu.get('rank', '无')}, 厂商: {'Intel' if cpu.get('firm') == '1' else 'AMD'}")
    return cpu_data, unique_proIds


def fetch_cpu_data_json(product_ids):
    """
    获取指定产品 ID 列表的 CPU 数据（JSON 格式）。
    
    参数:
        product_ids (list): 需要获取 CPU 数据的产品 ID 列表。
    
    返回:
        list: 包含 CPU 数据的字典列表（JSON 格式）。
    
    异常:
        requests.exceptions.RequestException: 如果 HTTP 请求有问题。
    
    示例:
        product_ids = [12345, 67890]
        cpu_data = fetch_cpu_data_json(product_ids)
        print(cpu_data)
    """
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
    """
    展示CPU的详细信息

    参数:
    cpu_data (dict): 包含CPU详细信息的字典，键为产品ID，值为包含厂商和排名信息的字典。
    cpu_data_json (list): 包含CPU JSON数据的列表，每个元素为一个CPU的JSON对象。

    返回:
    pandas.DataFrame: 包含CPU详细信息的数据框，按综合排名升序排序。

    数据框列:
    - 产品名称: CPU的产品名称
    - 系列: CPU的系列
    - 核心代号: CPU的核心代号
    - 主频: CPU的主频
    - 核心/线程: CPU的核心和线程数
    - 功耗: CPU的功耗
    - 集成显卡: CPU的集成显卡信息
    - 评分: CPU的评分
    - 价格: CPU的价格
    - 厂商: CPU的厂商 (Intel 或 AMD)
    - 单核排名: CPU的单核性能排名
    - 多核排名: CPU的多核性能排名
    - 游戏排名: CPU的游戏性能排名
    - 综合排名: CPU的综合性能排名
    """
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
    """
    解析给定URL中的商品名称和价格。

    参数:
        url (str): 要解析的网页URL。

    返回:
        None: 此函数将商品名称和价格打印到控制台。

    异常:
        requests.exceptions.RequestException: 如果HTTP请求有问题。

    示例:
        url_parse_goods('http://example.com/products')

    该函数执行以下步骤:
    1. 发送GET请求到提供的URL。
    2. 如果请求成功（状态码200），使用BeautifulSoup解析HTML内容。
    3. 查找所有<p>标签并遍历它们以提取商品名称和价格。
    4. 将商品名称和价格打印到控制台。
    5. 如果请求失败，打印响应的状态码。
    """ 
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


def find_pages(count, url="https://detail.zol.com.cn/cpu"):
    """
    参数:
        count (int): 要查找的页数。
        url (str, optional): 基础URL。默认为 "https://detail.zol.com.cn/cpu"。

    返回:
        None
    """

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
