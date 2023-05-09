import requests
import json
from bs4 import BeautifulSoup

# 构建请求 URL
url_template = 'http://110.41.160.173:8080/api/student/getQuestions?courseId=ebb2ac4476&page={}&chapterId='

# 遍历所有可能的页码，获取所有题目数据
questions = []

# 全局i
global i
i=1
for page in range(1, 10):
    url = url_template.format(page)
    response = requests.get(url)
    json_data = response.json()
    questions += json_data['data']['questionList']
# 解析并输出题目信息
for idx, question in enumerate(questions):
    # 去除题目中的 HTML 标签
    content = BeautifulSoup(question['content'], 'html.parser').get_text()

    # 去除选项中的 HTML 标签
    options = [option['content'] for option in question['answer']]
    answer = options.index([option['content'] for option in question['answer'] if option['right']][0]) + 1

    # 输出第几题

    print(f"### 第{idx+1}题")
    print(f"题目内容：{question['content'].replace('<p>', '').replace('</p>', '').replace('<br/>', '').replace('<br>', '').replace('<br />', '').replace('&nbsp', '').replace('</p', '').replace('</span>', '')}")
    for i, option in enumerate(options):
        print(f"- {option.replace('<p>', '').replace('</p>', '').replace('<br/>', '').replace('<br>', '').replace('<br />', '').replace('&nbsp', '').replace('</p', '').replace('</span>', '')}")
    print(f"\n\n正确答案 [rick](https://rick.icu) ：{chr(ord('A')+answer-1)}  \n")
