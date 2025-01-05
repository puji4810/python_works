import requests
from bs4 import BeautifulSoup
from selenium import webdriver

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Referer": "https://cpu.zol.com.cn/",  # 来源页面
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Connection": "keep-alive",
}


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


def url_parse_info(url='https://cpu.zol.com.cn/soc/'):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Referer": "https://cpu.zol.com.cn/",
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        items = soup.find_all('div', class_='tianti-detail')

        products_info_list = []

        for item in items:
            product_info = {}

            # 综合排名
            rank = item.find('p', class_='number')
            product_info['rank'] = rank.text.strip() if rank else None

            # 评分
            score = item.find('span', class_='number-percentage',
                              string=lambda x: x and '评分' in x)
            product_info['评分'] = score.text.strip().replace(
                '评分', '') if score else None

            # CPU系列
            cpu_series_item = item.find(
                'div', class_='item', string=lambda x: x and 'CPU系列' in x)
            if cpu_series_item:
                cpu_series = cpu_series_item.find_next(
                    'span', class_='content').text.strip()
                product_info['CPU系列'] = cpu_series
            else:
                product_info['CPU系列'] = None

            # 核心/线程
            core_num_item = item.find(
                'div', class_='item', string=lambda x: x and '核心/线程' in x)
            if core_num_item:
                core_num = core_num_item.find_next(
                    'span', class_='content').text.strip()
                product_info['核心/线程'] = core_num
            else:
                product_info['核心/线程'] = None

            # 功耗
            tdp_item = item.find('div', class_='item',
                                 string=lambda x: x and '热功耗设计' in x)
            if tdp_item:
                tdp = tdp_item.find_next('span', class_='content').text.strip()
                product_info['功耗'] = tdp
            else:
                product_info['功耗'] = None

            # 核显
            igpu_item = item.find('div', class_='item',
                                  string=lambda x: x and '集成显卡' in x)
            if igpu_item:
                igpu = igpu_item.find_next(
                    'span', class_='content').text.strip()
                product_info['核显'] = igpu
            else:
                product_info['核显'] = None

            # 价格
            price_item = item.find('a', class_='jd price')
            product_info['价格'] = price_item.text.strip(
            ) if price_item else None

            products_info_list.append(product_info)

        for product_info in products_info_list:
            print(product_info)
    else:
        print("请求失败，状态码：", response.status_code)


def scrape_dynamic_cpu_info():

    print("111111111111")
    # 设置 WebDriver
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # 无头模式
    driver = webdriver.Chrome(options=options)

    # 打开目标页面
    url = "https://cpu.zol.com.cn/soc/"
    driver.get(url)

    print("111111111111")
    # 获取页面源码
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")

    print("111111111111")
    # 找到所有的 CPU 信息块
    cpu_blocks = soup.find_all("div", class_="tianti-detail")

    print("111111111111")
    if not cpu_blocks:
        print("未找到任何 CPU 信息块，请检查页面结构是否变化。")
        driver.quit()
        return

    # 保存所有 CPU 信息
    cpu_info_list = []

    print("111111111111")
    for block in cpu_blocks:
        cpu_info = {}

        print("111111111111")
        # 综合排名
        rank = block.find("p", class_="number")
        cpu_info["排名"] = rank.text.strip() if rank else None

        print("111111111111")
        # CPU 系列
        cpu_series = block.find("div", class_="item",
                                string=lambda x: x and "CPU系列" in x)
        if cpu_series:
            cpu_info["CPU系列"] = cpu_series.find_next(
                "span", class_="content").text.strip()

        print("111111111111")
        # 核心/线程
        core_thread = block.find("div", class_="item",
                                 string=lambda x: x and "核心/线程" in x)
        if core_thread:
            cpu_info["核心/线程"] = core_thread.find_next(
                "span", class_="content").text.strip()

        print("111111111111")
        cpu_info_list.append(cpu_info)
        print(cpu_info)

    # 打印结果
        # for cpu in cpu_info_list:
    # print(cpu)

    driver.quit()


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
    # find_pages(5)
    print("111111111111")
    scrape_dynamic_cpu_info()
