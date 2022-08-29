import glob
import os
import time
import requests
import base64
import json

# 导入CreateQGUI模块
from qgui import CreateQGUI, MessageBox
# 【可选】导入自定义导航栏按钮模块、GitHub导航栏模块
from qgui.banner_tools import BaseBarTool, GitHub, AIStudio
# 【可选】一次性导入所有的主界面工具模块
from qgui.notebook_tools import *
# 【可选】导入占位符
from qgui.manager import QStyle, HORIZONTAL

token = " "


# 小说续写
def Novel_Sequel(args: dict):
    url = "https://wenxin.baidu.com/younger/portal/api/rest/1.0/ernie/3.0/zeus"
    fo = open(args["文件选择3"].get(), "r", encoding='utf-8')

    dic = 0

    # 进度条
    for i in range(1, 41):
        time.sleep(0.01)
        args["进度条3"].set(i)

    payload = {
        'access_token': token,
        'text': '上文：' + fo.read(),
        'seq_len': 1000,
        'task_prompt': '',
        'dataset_prompt': '',
        'topk': 10,
        'stop_token': '',
        'is_unidirectional': 1,
        'min_dec_len': 100,
        'min_dec_penalty_text': '[gEND]'
    }

    # 进度条
    for i in range(41, 61):
        time.sleep(0.01)
        args["进度条3"].set(i)

    response = requests.request("POST", url, data=payload)
    if response.text != "":
        dic = eval(response.text)

        # 进度条
        for i in range(61, 81):
            time.sleep(0.05)
            args["进度条3"].set(i)

        # 创建结果文档
        text_create_3(dic["data"]['result'], args)

    # 进度条
    for i in range(81, 91):
        time.sleep(0.02)
        args["进度条3"].set(i)
    for i in range(91, 100):
        time.sleep(0.06)
        args["进度条3"].set(i)
    for i in range(100, 101):
        time.sleep(0.5)
        args["进度条3"].set(i)

    # 输出结果文档
    print(dic["data"]['result'])

    # 也可以在终端中打印组件，顺便绑定用户调研函数
    q_gui.print_tool(RadioButton(["满意", "一般", "很差"], title="使用体验:", name="feedback", bind_func=feedback))


# 文本纠错
def text_error_correction(args: dict):
    url = "https://wenxin.baidu.com/younger/portal/api/rest/1.0/ernie/3.0/zeus"
    fo = open(args["文件选择2"].get(), "r", encoding='utf-8')
    dic = 0
    # 进度条
    for i in range(1, 41):
        time.sleep(0.01)
        args["进度条2"].set(i)

    payload = {
        'text': "改正下面文本中的错误：\"" + fo.read()+"\"",
        'seq_len': 1000,
        'task_prompt': 'Correction',
        'dataset_prompt': '',
        'access_token': token,
        'topk': 1,
        'stop_token': ''
    }

    # 进度条
    for i in range(41, 61):
        time.sleep(0.01)
        args["进度条2"].set(i)

    response = requests.request("POST", url, data=payload)
    if response.text != "":
        dic = eval(response.text)

        # 进度条
        for i in range(61, 81):
            time.sleep(0.05)
            args["进度条2"].set(i)

        # 创建结果文档
        text_create_2(dic["data"]['result'], args)

    # 进度条
    for i in range(81, 91):
        time.sleep(0.02)
        args["进度条2"].set(i)
    for i in range(91, 100):
        time.sleep(0.06)
        args["进度条2"].set(i)
    for i in range(100, 101):
        time.sleep(0.5)
        args["进度条2"].set(i)

    # 将结果输出到控制台
    print(dic["data"]['result'])

    # 也可以在终端中打印组件，顺便绑定用户调研函数
    q_gui.print_tool(RadioButton(["满意", "一般", "很差"], title="使用体验:", name="feedback", bind_func=feedback))


def Hand_Write(args: dict):
    '''
    手写文字识别
    '''
    # encoding:utf-8

    # client_id 为官网获取的AK， client_secret 为官网获取的SK
    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=TcPPU19bTYCFtxLHFvGVo9tu&client_secret=tfaZTHNlcvxBG9sYV7cGbCW5hTcjdKla'

    response = requests.get(host)

    dic = eval(response.text)
    token = dic['access_token']

    request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/handwriting"
    # 二进制方式打开图片文件
    f = open(args["文件选择1"].get(), 'rb')
    img = base64.b64encode(f.read())

    params = {"image": img}
    request_url = request_url + "?access_token=" + token
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(request_url, data=params, headers=headers)
    dic = eval(response.text)
    i = 0
    data = dic['words_result']
    length = len(data)

    words = " "

    for i in range(0, length):
        words = words + dic['words_result'][i]['words']
        word = dic['words_result'][i]['words']
        text_create_1(word, args)
        print(dic['words_result'][i]['words'])

    # 文档纠错
    url = "https://wenxin.baidu.com/younger/portal/api/rest/1.0/ernie/3.0/zeus"
    fo = open(args["保存位置1"].get(), "r", encoding='utf-8')
    dic = 0
    # 进度条
    for i in range(1, 41):
        time.sleep(0.01)
        args["进度条1"].set(i)

    token = requests.request("POST",
                             "https://wenxin.baidu.com/younger/portal/api/oauth/token",
                             data={
                                 "grant_type": "client_credentials",
                                 "client_id": "PMywBGGeWST03IRRFD7VdHaaYFwMA0xG",
                                 "client_secret": "FFkPTQurtncFk1dOXkUrPxEmk6GjDYvj"},
                             timeout=3)
    token = json.loads(token.text)["data"]

    payload = {
        'text': "改正下面文本中的错误：\"" + words +"\"",
        'seq_len': 1000,
        'task_prompt': 'Correction',
        'dataset_prompt': '',
        'access_token': token,
        'topk': 1,
        'stop_token': ''
    }

    # 进度条
    for i in range(41, 61):
        time.sleep(0.01)
        args["进度条1"].set(i)

    response = requests.request("POST", url, data=payload)

    if response.text != "":
        dic = eval(response.text)

        # 进度条
        for i in range(61, 81):
            time.sleep(0.05)
            args["进度条1"].set(i)

        # 创建结果文档
        text_create(dic["data"]['result'], args)

    # 进度条
    for i in range(81, 91):
        time.sleep(0.02)
        args["进度条1"].set(i)
    for i in range(91, 100):
        time.sleep(0.06)
        args["进度条1"].set(i)
    for i in range(100, 101):
        time.sleep(0.5)
        args["进度条1"].set(i)

    # 将结果输出到控制台
    print(dic["data"]['result'])

    # 也可以在终端中打印组件，顺便绑定用户调研函数
    q_gui.print_tool(RadioButton(["满意", "一般", "很差"], title="使用体验:", name="feedback", bind_func=feedback))


# 用户调研
def feedback(args: dict):
    # 用户调研Callback
    info = args["feedback"].get()
    if info == "满意":
        print("您的支持是对我们最大的鼓励！")
    elif info == "一般":
        print("我们会努力改进的！")
    else:
        print("啊~我们对此非常抱歉。如有问题可联系平台客服进行解决呦~QQ:3092665186")


def bind_dir(args: dict):
    # 获取所选择文件所在的文件夹路
    path = os.path.dirname(args["保存位置1"].get())
    # 可以通过name参数来设置对应的内容，使用set方法即可完成设置
    args["保存位置1"].set(path)
    print("保存位置已修改为：", args["保存位置1"].get())


def bind_dir_1(args: dict):
    # 获取所选择文件所在的文件夹路
    path = os.path.dirname(args["保存位置2"].get())
    # 可以通过name参数来设置对应的内容，使用set方法即可完成设置
    args["保存位置2"].set(path)
    print("保存位置已修改为：", args["保存位置2"].get())


def bind_dir_2(args: dict):
    # 获取所选择文件所在的文件夹路
    path = os.path.dirname(args["保存位置3"].get())
    # 可以通过name参数来设置对应的内容，使用set方法即可完成设置
    args["保存位置3"].set(path)
    print("保存位置已修改为：", args["保存位置3"].get())


# msg数据保存
def text_create(msg, args: dict):
    desktop_path = args["保存位置1"].get()  # 新创建的txt文件的存放路径
    full_path = desktop_path  # 也可以创建一个.doc的word文档
    file = open(full_path, 'w', encoding='utf-8')
    file.write(msg)
    file.write('\r\n')        # msg也就是信息
    file.close()


def text_create_1(msg, args: dict):
    desktop_path = args["保存位置1"].get()  # 新创建的txt文件的存放路径
    full_path = desktop_path  # 也可以创建一个.doc的word文档
    file = open(full_path, 'a', encoding='utf-8')
    file.write(msg)
    file.write('\r\n')        # msg也就是信息
    file.close()


def text_create_2(msg, args: dict):
    desktop_path = args["保存位置2"].get()  # 新创建的txt文件的存放路径
    print("")
    full_path = desktop_path  # 也可以创建一个.doc的word文档
    file = open(full_path, 'w', encoding='utf-8')
    file.write(msg)           # msg也就是信息
    file.close()


def text_create_3(msg, args: dict):
    desktop_path = args["保存位置3"].get()  # 新创建的txt文件的存放路径
    full_path = desktop_path  # 也可以创建一个.doc的word文档
    file = open(full_path, 'w', encoding='utf-8')
    file.write(msg)  # msg也就是信息
    file.close()


def go_to_first_page(args: dict):
    args["QGUI-BaseNoteBook"].set(0)


def acess_tken(args: dict):
    # 获取Token
    global token
    token = requests.request("POST",
                             "https://wenxin.baidu.com/younger/portal/api/oauth/token",
                             data={
                                 "grant_type": "client_credentials",
                                 "client_id": args["client_id"].get(),
                                 "client_secret": args["client_secret"].get()},
                             timeout=3)
    token = json.loads(token.text)["data"]
    print("API KEY 已修改为：" + args["client_id"].get())
    print("Secret KEY 已修改为：" + args["client_secret"].get())
    MessageBox.info("API修改成功~")


def acess_token():
    global token
    token = requests.request("POST",
                             "https://wenxin.baidu.com/younger/portal/api/oauth/token",
                             data={
                                 "grant_type": "client_credentials",
                                #  "client_id": "PMywBGGeWST03IRRFD7VdHaaYFwMA0xG",
                                #  "client_secret": "FFkPTQurtncFk1dOXkUrPxEmk6GjDYvj"},
                                 "client_id": "jMp1UuMESExHSYoSXKlRgO5M1mmWTIGV",
                                 "client_secret": "nukcB8G8IjifV5XlkOd45MLgVSr83usW"},
                             timeout=3)
    token = json.loads(token.text)["data"]


# 创建主界面
q_gui = CreateQGUI(title="文本处理系统                   ",  # 界面标题
                   tab_names=["更改API", "文本识别", "文档纠错", "小说续写", "帮助"],  # 界面中心部分的分页标题
                   style=QStyle.lumen)  # 皮肤

# 在界面最上方添加一个按钮，链接到GitHub主页
q_gui.add_banner_tool(GitHub(url="https://www.nwpu.edu.cn/", name="访问西工大官网"))
# 也可以是AI Studio
q_gui.add_banner_tool(AIStudio(url="https://wenxin.baidu.com/moduleApi/key", name="获取API"))

# 获取默认token
acess_token()

# 在主界面部分添加一个文件选择工具
# 更改用户
q_gui.add_notebook_tool(Label(text="此仅提供有限试用次数，如需获取更多请点击左上角去获取属于您自己的API账号（非必要）", title="温馨提示:"))
q_gui.add_notebook_tool(InputBox(name="client_id", default="", label_info="API KEY:"))
q_gui.add_notebook_tool(InputBox(name="client_secret", default="", label_info="Secret KEY:"))
run_menu = RunButton(bind_func=acess_tken, text="登录")
q_gui.add_notebook_tool(run_menu)

# 文本识别
q_gui.add_notebook_tool(Label(text="请上传清晰图片且每次识别字数不超过1000字", title="温馨提示:", tab_index=1))
q_gui.add_notebook_tool(
    ChooseFileTextButton(name="文件选择1", label_info="请选择图片", entry_info="图片路径", button_info="选择图片", async_run=True,
                         tab_index=1))
q_gui.add_notebook_tool(
    ChooseFileTextButton(name="保存位置1", label_info="选择保存位置", entry_info="目标路径", button_info="选择文件",
                         tab_index=1, async_run=True))
run_menu = HorizontalToolsCombine([Progressbar(name="进度条1"), RunButton(bind_func=Hand_Write, tab_index=1, text="开始识别")],
                                  tab_index=1)
q_gui.add_notebook_tool(run_menu)

# 第二页 - 文本纠错
# 添加一个文件选择工具
q_gui.add_notebook_tool(Label(text="每次纠错字数不应超过1000字", title="温馨提示:", tab_index=2))
q_gui.add_notebook_tool(
    ChooseFileTextButton(name="文件选择2", label_info="请选择文档", entry_info="文档路径", button_info="选择文档", tab_index=2,
                         async_run=True))
q_gui.add_notebook_tool(
    ChooseFileTextButton(name="保存位置2", label_info="选择保存位置", entry_info="目标路径", button_info="选择文件",
                         tab_index=2, async_run=True))
run_menu = HorizontalToolsCombine([Progressbar(name="进度条2"), RunButton(bind_func=text_error_correction, tab_index=2,
                                                                       text="开始纠错")], tab_index=2)
q_gui.add_notebook_tool(run_menu)

# 第三页 - 小说续写
# 添加一个文件选择工具
q_gui.add_notebook_tool(Label(text="原文不得超过1000字", title="温馨提示:", tab_index=3))
q_gui.add_notebook_tool(
    ChooseFileTextButton(name="文件选择3", label_info="请选择文档", entry_info="文档路径", button_info="选择文档", tab_index=3,
                         async_run=True))
q_gui.add_notebook_tool(
    ChooseFileTextButton(name="保存位置3", label_info="选择保存位置", entry_info="目标路径", button_info="选择文件",
                         tab_index=3, async_run=True))
run_menu = HorizontalToolsCombine([Progressbar(name="进度条3"), RunButton(bind_func=Novel_Sequel, tab_index=3,
                                                                       text="开始续写")], tab_index=3)
q_gui.add_notebook_tool(run_menu)

# 帮助文档
q_gui.add_notebook_tool(Label(title="帮助文档", text="1.在进行更改API时需要确认账户与密码对应，否则无法运行，需要对其进行覆盖或者重启"
                                                 "应用程序。\n2.所有待处理文件等均需限制在1000字以内。\n3.所有待处理文本中不得含有侮辱性词汇，"
                                                 "否则程序无法正常运行。\n4.使用OCR时注意上传照片需要清晰可见，行与行直接界限分明，可以兼容."
                                                 "jpg与.npg文件，对于大量手写文字内容，可以拍成多张照片后上传，识别时间随字数量的增大"
                                                 "而增大。\n5.使用文本纠错时需上传.txt文件，为防止不必要报错，格式应设置为utf-8格式。",
                              alignment=LEFT, tab_index=4))
q_gui.add_notebook_tool(Label(title="", text="更多详细内容请前往  ”使用说明“  进行查看。",
                              alignment=LEFT, tab_index=4))
# 左侧信息栏
# 简单加个简介
q_gui.set_navigation_about(author="NPU AI 15",
                           version="1.1.2",
                           github_url="https://www.nwpu.edu.cn/",
                           other_info=["欢迎加入NPU！"])

# 注意事项
q_gui.set_navigation_info(title="注意事项",
                          info="本应用已给定默认API接口，但使用次数有限，更多次数请前往文心大模型官网注册获取自己的API账户，"
                               "登录后方可无限制使用。 "
                               "\ntips：若遇到程序报错且多次运行均无法通过的情况，那么需要您将输入文件更改为utf-8格式在进行运行。")

# 也可以加一下其他西工大信息
q_gui.set_navigation_info(title="NPU简介",
                          info="西北工业大学，简称“西工大”，是中华人民共和国工业和信息化部"
                               "直属，中国唯一一所以同时发展航空、航天、航海工程教育和科学研究为特色的全国重点大学，")

# 跑起来~切记！一定要放在程序末尾

q_gui.run()
