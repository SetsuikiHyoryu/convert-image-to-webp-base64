# 压缩图片并获取图片的 Base64 编码

## 目的

工作中保密图片不适合外链至 Markdown 文档，又图片过大不便嵌入 Markdown 文档，故作此程序以便压缩图片以便于嵌入 Markdwon 文档。  
压缩方式为将图片压缩为 **720p** 以内的 **webp** 格式。

## 必须依赖

### Python

Python 3.11.1（为开发时使用的版本）

### 第三方包

```shell
pip install -r requirements.txt
```

## 启动方式

```shell
python app.py
```

启动后为交互式操作。

## 个人主页

<https://setsuikihyoryu.github.io/zh/>
