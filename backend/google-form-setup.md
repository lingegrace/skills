# 用 Google 表单收反馈（约 5 分钟）

网站上的三个入口（请求 skill、拉绳反馈、定制咨询）会直接提交到你的 Google 表单。

## 1. 建表单

打开 https://forms.google.com ，新建一个空白表单，标题写 `Skill Library inbox`，添加 **4 个题目**，题目名称和题型如下（顺序不重要）：

| 题目名称 | 题型 |
|---|---|
| `Type` | 简答（Short answer） |
| `Message` | **段落（Paragraph）**：用户留言可能很长 |
| `Email` | 简答（Short answer） |
| `Page` | 简答（Short answer） |

不要用多选、日期、时间这些题型。网站提交的都是文字。

都**不要**设成必填。

## 2. 打开收件和通知

在 **回复（Responses）** 标签页：
- 点绿色的表格图标，选 **链接到 Google 表格**，以后每条回复会自动写进表格。
- 点 **⋮ → 获取新回复的电子邮件通知**，这样每条都会发到你的邮箱。

在 **设置 → 回复** 里，确认 **"收集电子邮件地址"已关闭**，**"仅限……的用户"已关闭**，否则访客提交不了。

## 3. 拿到"预填链接"，发给 Claude

1. 点右上角 **⋮ → 获取预填链接**（Get pre-filled link）。
2. 4 个题目里分别随便填：`TYPE`、`MESSAGE`、`EMAIL`、`PAGE`。
3. 点 **获取链接 → 复制链接**，把这个链接发给 Claude 就行。

链接长这样：
`https://docs.google.com/forms/d/e/1FAIpQL…/viewform?usp=pp_url&entry.123456=TYPE&entry.234567=MESSAGE&…`

Claude 会从里面取出表单地址和 4 个 `entry.` 编号，填进 `data/site.yaml`，然后发一条测试消息。
