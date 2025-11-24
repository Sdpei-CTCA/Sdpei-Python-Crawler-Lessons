from time import sleep
import csv
from datetime import datetime

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from pathlib import Path
import os


def get_status_text(status_class):
    """根据状态类名获取状态文本"""
    status_map = {
        "status-1": "未知",
        "status-2": "已失效",
        "status-3": "有效",
        "status-4": "尚未生效",
        "status-null": "无状态"
    }
    return status_map.get(status_class, "未知状态")


def main():
    keyword = input("请输入搜索关键词：")
    url = "https://flk.npc.gov.cn/search"
    options = Options()
    #options.add_argument("--headless")  # 最大化窗口
    options.add_argument("--disable-images")  # 禁用图片加载提高速度
    options.add_experimental_option("detach", True)  # 保持浏览器打开
    local_driver = Path("drivers/msedgedriver.exe")
    driver = webdriver.Edge(service=Service(str(local_driver)), options=options)
    
    try:
        driver.get(url)
        sleep(3)
        
        # 使用更稳定的选择器
        # 查找输入框：通过 placeholder 属性定位
        search_box = driver.find_element(By.XPATH, "//input[@placeholder='请输入']")
        search_box.send_keys(keyword)
        
        # 查找搜索按钮：定位输入框旁边的搜索图标
        # 注意：有时候点击图标可能没反应，可以尝试回车键
        search_box.send_keys(Keys.ENTER)
        # 或者如果必须点击图标：
        # search_button = driver.find_element(By.XPATH, "//div[contains(@class, 'search-input')]//i[contains(@class, 'el-input-icon')]")
        # search_button.click()
        
        sleep(3)
        
        # 获取所有结果项
        # 更新结果项的选择器，根据 HTML 结构，结果项在 .result-item 类中
        results = driver.find_elements(By.CSS_SELECTOR, ".result-item")
        
        # 准备CSV数据
        csv_data = []
        
        for result in results:
            try:
                # 获取标题
                title_element = result.find_element(By.CSS_SELECTOR, ".title-content")
                title = title_element.text.strip()
                
                # 获取状态
                status_element = result.find_element(By.CSS_SELECTOR, ".status")
                status_class = status_element.get_attribute("class").split()[-1]
                status_text = get_status_text(status_class)
                
                # 获取描述信息
                desc_elements = result.find_elements(By.CSS_SELECTOR, ".desc div")
                details = [elem.text.strip() for elem in desc_elements if elem.text.strip()]
                
                # 提取分类、制定机关、公布日期等信息
                law_type = ""
                department = ""
                publish_date = ""
                effect_date = ""
                
                for detail in details:
                    if "公布日期" in detail:
                        publish_date = detail.replace("公布日期：", "").strip()
                    elif "施行日期" in detail:
                        effect_date = detail.replace("施行日期：", "").strip()
                    elif "分类" in detail or any(word in detail for word in ["法律", "法规", "决定"]):
                        law_type = detail
                    elif "制定机关" in detail:
                        department = detail.replace("制定机关：", "").strip()
                
                # 添加到CSV数据
                csv_data.append({
                    "标题": title,
                    "状态": status_text,
                    "分类": law_type,
                    "制定机关": department,
                    "公布日期": publish_date,
                    "施行日期": effect_date
                })
                
                print(f"提取到: {title}")
                
            except Exception as e:
                print(f"处理结果时出错: {e}")
                continue
        
        # 保存为CSV文件
        if csv_data:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"法律法规搜索结果_{keyword}_{timestamp}.csv"
            
            with open(filename, 'w', newline='', encoding='utf-8-sig') as csvfile:
                fieldnames = ['标题', '状态', '分类', '制定机关', '公布日期', '施行日期']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                
                writer.writeheader()
                for row in csv_data:
                    writer.writerow(row)
            
            print(f"结果已保存到: {filename}")
            print(f"共提取 {len(csv_data)} 条记录")
        else:
            print("未找到任何结果")
            
    except Exception as e:
        print(f"程序执行出错: {e}")
    finally:
        driver.quit()


if __name__ == "__main__":
    main()