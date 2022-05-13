import requests
import pymysql as pymysql
from lxml import etree

requests.packages.urllib3.disable_warnings()


class DX():
    def __init__(self,cookies):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36 Edg/101.0.1210.39'}
        self.headers2 = {
            "Content-Type": "application/x-www-form-urlencoded",
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36 Edg/101.0.1210.39'}

        self.cookies = cookies
        self.cookies = {i.split("=")[0]: i.split("=")[1] for i in self.cookies.split("; ")}

    def getproblem(self):
        url = "https://dangxiao.hnust.edu.cn/index.php?s=/Exam/practice/lib/1"
        r = requests.get(url=url, headers=self.headers, cookies=self.cookies, verify=False)
        html = etree.HTML(r.text)
        # lxml 会自动修 HTML ，查看一下 lxml 修正后的结果
        etree.tostring(html, encoding='utf-8', pretty_print=True, method="html").decode('utf-8')
        problemid = html.xpath('//*[@id="form1"]/table/tbody/tr[1]/td[1]/input//@name')[0]
        # 获取题目id
        id = int(problemid.split('_')[-1].split('"')[0].split('[')[0].split('"')[0])
        name = html.xpath('//*[@id="form1"]/table/thead/tr/th//text()')
        # 获取题目选项
        selectionA = ''
        selectionB = ''
        selectionC = ''
        selectionD = ''
        tag = 0
        try:
            if (name[1] == " （多选题）"):
                print(name[1])
                tag = 1
        except Exception as e:
            print(e)
            print(str(tag) + "非多选")
        try:
            selectionA = html.xpath('//*[@id="form1"]/table/tbody/tr[1]/td[2]//text()')[0]
        except Exception as e:
            print(e)
        try:
            selectionB = html.xpath('//*[@id="form1"]/table/tbody/tr[2]/td[2]//text()')[0]
        except Exception as e:
            print(e)
        try:
            selectionC = html.xpath('//*[@id="form1"]/table/tbody/tr[3]/td[2]//text()')[0]
        except Exception as e:
            print(e)
        try:
            selectionD = html.xpath('//*[@id="form1"]/table/tbody/tr[4]/td[2]//text()')[0]
        except Exception as e:
            print(e)
        return id, problemid, name[0], tag, selectionA, selectionB, selectionC, selectionD

    def getcorrectanswer(self, problemid, list):
        answerlist = []
        url = "https://dangxiao.hnust.edu.cn/index.php?s=/exam/practice"
        for i in list:
            datas = {problemid: i,
                     "method": "submit"}
            r = requests.post(url=url, headers=self.headers, cookies=self.cookies, verify=False, data=datas)
            status = r.json()['status']
            print(status)
            if (status == 200):
                answerlist.append(i)
                return answerlist

    def getcorrectanswer2(self, problemid, list):
        url = "https://dangxiao.hnust.edu.cn/index.php?s=/exam/practice"
        flag = 0
        answerlist = []
        for i in list:
            for j in list:
                if (i != j):
                    datas = problemid + "=" + i + "&" + problemid + "=" + j + "&method=submit"
                    r = requests.post(url=url, headers=self.headers2, cookies=self.cookies, verify=False, data=datas)
                    status = r.json()['status']
                    if (status == 200):
                        answerlist.append(i)
                        answerlist.append(j)
                        flag = 1
        if flag == 0:
            answerlist.clear()
            answerlist = self.getcorrectanswer3(problemid, list)
        return answerlist

    def getcorrectanswer3(self, problemid, list):
        flag = 0
        url = "https://dangxiao.hnust.edu.cn/index.php?s=/exam/practice"
        answerlist = []
        for i in list:
            for j in list:
                for k in list:
                    if (i != j and i != k and j != k):
                        datas = problemid + "=" + i + "&" + problemid + "=" + j + "&" + problemid + "=" + k + "&method=submit"
                        r = requests.post(url=url, headers=self.headers2, cookies=self.cookies, verify=False,
                                          data=datas)
                        status = r.json()['status']
                        if (status == 200):
                            answerlist.append(i)
                            answerlist.append(j)
                            answerlist.append(k)
                            flag = 1

        if (flag == 0):
            answerlist.clear()
            answerlist = ["A", "B", "C", "D"]
        return answerlist

    def getanswer(self, problemid, tag):
        correctanswerlist = []
        if tag == 0:
            list = ["A", "B", "C", "D"]
            correctanswerlist = self.getcorrectanswer(problemid, list)
        else:
            list = ["A", "B", "C", "D"]
            correctanswerlist = self.getcorrectanswer2(problemid, list)
        return correctanswerlist

    def save(self, id, name, topic, selectionA, selectionB, selectionC, selectionD, correctanswerlist):
        db = pymysql.connect(host='localhost', user='root', password='111111', database='hnustdx')

        cursor = db.cursor()
        sql = "INSERT INTO hqh_question(question_id,question_name,topic,OptionA,OptionB,OptionC,OptionD," \
              "correct_answer) VALUES (%s,%s,%s,%s,%s,%s,%s,%s) "
        try:
            cursor.execute(sql,
                           (id, name, topic, selectionA, selectionB, selectionC, selectionD, str(correctanswerlist)))
            db.commit()
            print('插入数据成功')
        except Exception as e:
            db.rollback()
            print("插入数据失败")
            print(e)
        db.close()

    def run(self, count):
        for i in range(0, count):
            print("===================" + str(i) + "=====================")
            id, problemid, name, tag, selectionA, selectionB, selectionC, selectionD = self.getproblem()
            print(id, problemid, name, tag, selectionA, selectionB, selectionC, selectionD)
            correctanswerlist = self.getanswer(problemid, tag)
            topic = "单选题"
            if selectionC == "":
                topic = "判断题"
            if type(correctanswerlist) != 'str':
                correctanswerlist = str(correctanswerlist)
            if len(correctanswerlist) > 1:
                topic = "多选题"
            self.save(id, name, topic, selectionA, selectionB, selectionC, selectionD, correctanswerlist)
            print(correctanswerlist)


if __name__ == '__main__':
    cookies="PHPSESSID=vlicns96bfrq8m236pttrnode3"
    count=2000
    rick = DX(cookies)
    rick.run(count)
