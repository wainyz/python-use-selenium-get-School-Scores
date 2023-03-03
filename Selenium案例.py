# -*- coding:utf-8 _*-
"""
============================
@author:笨磁
@time:2023/1/17:13:10
@email:Player_simple@163.com
@IDE:PyCharm
============================
"""
import re
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
import ddddocr
from PIL import Image

def tips():
    print('tips:使用之前请务必打开西华大学vpn确认连接到校园网,否则程序无法运行.')
def get_score(bro):
    url = 'http://jwc.xhu.edu.cn/cjcx/cjcx_cxXsgrcj.html?doType=query&gnmkdm=N305005&su=' + str(name)
    bro.get(url)
    source = bro.page_source
    finder = re.compile('"bfzcj":"(.*?)",.*?"kcmc":"(.+?)",.*"xm":"(.*?)",')
    data = finder.findall(source)
    return data
def print_score(data):
    with open('./ScoreInformation.txt','w') as file:
        for item in data:
            file.write(f'{item[0]}   {item[1]}   {item[2]}\n')
        file.close()
    print('#查询到本学期成绩:')
    print('成绩   科目   姓名')
    for item in data:
        print(f'{item[0]}   {item[1]}   {item[2]}')


def get_examination(bro):
    url = 'http://jwc.xhu.edu.cn/kwgl/kscx_cxXsksxxIndex.html?doType=query&gnmkdm=N358105&su='+str(name)
    bro.get(url)
    source = bro.page_source
    finder = re.compile('"zwh":"(\d+?)","ksmc":"(.+?)","kssj":"(.+?)",.*?"cdmc":"(.+?)",.*?,.*?kcmc":"(.+?)"')
    data = finder.findall(source)
    return data

def print_examination(data):
    with open('./examination.txt','w') as file:
        for item in data:
            file.write(f'{item[0]}\t{item[1]}\t{item[2]}\t{item[3]}\t{item[4]}\n')
        file.close()
    print('#查询到本学期考试信息:')
    print('座位号\t考试类型\t考试时间\t地点\t科目')
    for item in data:
        print(f'{item[0]}\t{item[1]}\t{item[2]}\t{item[3]}\t\t{item[4]}')

if __name__=='__main__':
    tips()
    Edge_options_ = Options()
    Edge_options_.add_argument('--headless')
    Edge_options_.add_argument('--disable-gpu')
    bro = webdriver.Edge(options=Edge_options_)
    bro.set_window_rect(0,0,500,800)
    bro.set_page_load_timeout(3)
    bro.get('http://jwc.xhu.edu.cn/xtgl/login_slogin.html')
    while True:
        name = input("输入学号:")
        mm = input("输入教务系统密码:")
        input_1 = bro.find_element(By.ID,'yhm')
        input_1.send_keys(str(name))
        input_2 = bro.find_element(By.ID,'mm')
        input_2.send_keys(str(mm))
        try:
            #如果出现验证码,自动识别输入
            yzm = bro.find_element(By.ID,'yzm')
            #计算截取验证码的坐标
            rangle = (217,366,324,395)
            bro.save_screenshot('./html_temp.png')
            with Image.open('./html_temp.png') as file:
                frame = file.crop(rangle)
                code_img = './code_img.png'
                frame.save(code_img)
            with open('./code_img.png','rb') as code_i:
                data_img = code_i.read()
                code_i.close()
            ocr = ddddocr.DdddOcr(old=True)
            yzm_str = ocr.classification(data_img)
            if len(yzm_str) == 0 :
                yzm_str = '本次识别失败!'
            yzm.send_keys(yzm_str)
            #print(yzm_str)
        except:
            pass
        btn = bro.find_element(By.ID,'dl')
        btn.click()
        time.sleep(1)
        if '/login' in bro.current_url:
            tips_data = bro.find_element(By.ID,'tips')
            print(f'登陆失败,{tips_data.text}...')
        else:
            print('登陆成功!')
            break
    print_score(get_score(bro))
    print_examination(get_examination(bro))
    bro.quit()