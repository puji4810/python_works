

import requests
from bs4 import BeautifulSoup

# 设置目标URL
url = "https://detail.zol.com.cn/cpu/intel/"

# 设置请求头，模拟浏览器访问
headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

# 发送请求
response = requests.get(url, headers=headers)

# 检查请求是否成功
if response.status_code == 200:
        # 解析页面内容
    soup = BeautifulSoup(response.text, 'html.parser')
        
        # 存储结果的列表
    products = []
        
        # 查找商品信息块
    items = soup.find_all('p')
    for item in items:
         name_tag = item.find('a', title=True)
         if name_tag:
            name = name_tag['title']  # 商品名称
            price_tag = item.find_next_sibling('p')
            if price_tag and price_tag.find('em', class_='price'):
                price = price_tag.find('em', class_='price').text.strip()  # 商品价格
                if price != '价格面议':
                    products.append({"商品名称": name, "价格": price})
                    
    for product in products:
        print(f"商品名称: {product['商品名称']}, 价格: {product['价格']}")
else:
    print("请求失败，状态码：", response.status_code)
