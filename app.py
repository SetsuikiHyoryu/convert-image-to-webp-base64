'''
Author: 雪域冰龍
Date: 2023/10/09
Description: 压缩并获取图片的 base64 字符串
'''

import requests
from PIL import Image
import io
import base64
import os

# [[获取图片处理信息]]
print('处理图片的方式：')
print('1. 生成 webp 副本')
print('2. 生成 webp base64 字符串')
print('3. 生成原图 base64 字符串\n')

handling_type = input('请选择处理图片的方式（仅数字）：')

print('图片的来源：')
print('1. 本地')
print('2. 网络\n')

source_type = input('请选择图片的来源（仅数字）：')
image_path = input('请输入图片的地址：')
saving_destination = input('请输入生成结果保存的目录（默认为 ./images/）：') or './images/'

# 获取图片名称（含扩展名）
image_name_full = os.path.basename(image_path)
# 分离图片名称和扩展名
image_name_no_extension, image_extension = os.path.splitext(image_name_full)

# [[获取图片]]
image_file = None

if source_type == '1':
    with open(image_path, 'rb') as file:
        image_file = file.read()
else:
    response = requests.get(image_path)

    if response.status_code == 200:
        image_file = response.content
    else:
        print('请求失败，HTTP 状态码：', response.status_code)

# [[缩放图片]]
image_stream = io.BytesIO(image_file)
original_image = Image.open(image_stream)
limited_height = 720

# 限制图片为 720p 以内
if original_image.height > limited_height:
    scale_factor = 0

    while original_image.height * (scale_factor + 0.1) <= limited_height:
        scale_factor += 0.1

    smaller_image = original_image.resize((
        round(original_image.width * scale_factor),
        round(original_image.height * scale_factor)
    ))

    image_stream = io.BytesIO()
    image_type = image_extension.lstrip('.').upper()

    smaller_image.save(
        image_stream, 'JPEG' if image_type == 'JPG' else image_type
    )

# [[处理图片]]
image_base64 = None
format = f"data:image/{image_extension.lstrip('.')};base64,"

if handling_type == '1':
    image = Image.open(image_stream)

    image.save(
        os.path.join(saving_destination, image_name_no_extension + '.webp'),
        'WEBP'
    )

elif handling_type == '2':
    webp_stream = io.BytesIO()
    image = Image.open(image_stream)
    image.save(webp_stream, 'WEBP')
    image_base64 = base64.b64encode(webp_stream.getvalue()).decode('utf-8')
    format = "data:image/webp;base64,"

elif handling_type == '3':
    image_base64 = base64.b64encode(image_stream.getvalue()).decode('utf-8')

# 将 base64 文本写入本地
if handling_type == '2' or handling_type == '3':
    with open(
        os.path.join(saving_destination, image_name_no_extension + '.txt'),
        'w'
    ) as file:
        file.write(format + image_base64)
