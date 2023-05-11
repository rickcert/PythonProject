import json
import requests
import html

url_template = 'http://110.41.160.173:8080/api/student/getQuestions?courseId=ebb2ac4476&page={}&chapterId='

with open('1.html', 'w', encoding='utf-8') as f:
    f.write('<html><head><meta charset="utf-8"></head><body>')
    simple_question_count = 0
    judgement_question_count = 0
    choice_question_count = 0
    for page in range(1, 10):
        url = url_template.format(page)
        response = requests.get(url)
        data = json.loads(response.text)
        question_list = data['data']['questionList']

        for question in question_list:
            if question['type'] == '4444':
                # 简答题
                answers = question['answer']
                correct_answer = answers[0]['content']
                options = ''
                question_type = '简答题'
                simple_question_count += 1
                question_number = '{}'.format(simple_question_count)
            elif question['type'] == '1111':
                # 判断题
                answers = question['answer']
                correct_answer =answers[0]['content']
                options = ''
                question_type = '判断题'
                judgement_question_count += 1
                question_number = '{}'.format(judgement_question_count)
            else:
                # 选择题
                answers = question['answer']
                correct_answer = ''
                options = ''
                for j, answer in enumerate(answers):
                    option = answer['content']
                    options += '{}<br>'.format( option)
                    if answer['right']:
                        correct_answer += chr(ord('A') + j)
                question_type = '选择题'
                choice_question_count += 1
                question_number = '{}'.format(choice_question_count)

            question_content = question['content'].replace('<p>', '').replace('</p>', '')
            if question_type in ['简答题']:
                f.write('<p>## 简答题 第{}题 <br>知识点：{}<br>题目：<p></p>```<p>{}</p>```<br></p>正确答案：<p>```{}</p>```'.format(
                    question_number, question['point'], question_content, correct_answer))
            elif question_type in ['判断题']:
                f.write('<p>## 判断题 第{}题 <br>知识点：{}<br>题目：{}<br></p>正确答案：{}'.format(
                    question_number, question['point'], question_content, correct_answer))
            else:
                f.write('<p>## 选择题 第{}题 <br>知识点：{}<br>题目：{}<br></p>选项：<br><p>```{}</p>```<br><p>正确答案：{}</p>'.format(
                    question_number, question['point'], question_content, options, correct_answer))
            f.write('<hr>')
    f.write('</body></html>')
