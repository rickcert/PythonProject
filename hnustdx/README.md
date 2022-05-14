# hnustdx
爬取湖南科技大学党课题库

## 网站分析

- 服务器直接生成html返回给客服端
- 采用thinkphp3.4.3 还不需要cookies.......
- 页面结构如图
-  ![image-20220515001308938](https://cdn.jsdelivr.net/gh/rickhqh/pic/img/202205150013056.png)

## 试题页面

- 入党积极分子考试题库:https://dangxiao.hnust.edu.cn/index.php?s=/Exam/practice/lib/1

- 发展对象考试题库:https://dangxiao.hnust.edu.cn/index.php?s=/Exam/practice/lib/2

- 预备党员考试题库:https://dangxiao.hnust.edu.cn/index.php?s=/Exam/practice/lib/3

  

## 页面数据获取

xpath解析

- ```html
  name = html.xpath('//*[@id="form1"]/table/thead/tr/th//text()')
  ```

- ```
  problemid = html.xpath('//*[@id="form1"]/table/tbody/tr[1]/td[1]/input//@name')[0]
  ```

- ```
  selectionA = html.xpath('//*[@id="form1"]/table/tbody/tr[1]/td[2]//text()')[0]
  ```

## 获取答案

- 校验答案网址:https://dangxiao.hnust.edu.cn/index.php?s=/exam/practice
- Content-Type为:application/x-www-form-urlencoded
- 拿答案方法:**只能撞题库!!!!!**
-  ![image-20220515002353462](https://cdn.jsdelivr.net/gh/rickhqh/pic/img/202205150023560.png)

## 总结

这网站真憨比。。。。。。。

哦，还有个笑点

 ![image-20220515002604772](https://cdn.jsdelivr.net/gh/rickhqh/pic/img/202205150026854.png)