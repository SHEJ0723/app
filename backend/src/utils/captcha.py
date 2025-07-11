import random
import string
import base64
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import os

class CaptchaGenerator:
    @staticmethod
    def generate_text(length=4):
        """生成随机验证码文本"""
        # 排除容易混淆的字符
        characters = string.ascii_uppercase + string.digits
        characters = characters.replace('0', '').replace('O', '').replace('1', '').replace('I', '')
        return ''.join(random.choices(characters, k=length))

    @staticmethod
    def generate_captcha():
        """生成验证码图片"""
        # 图片尺寸
        width = 120
        height = 40
        # 背景颜色
        bg_color = (255, 255, 255)
        # 文字颜色
        text_colors = ['#4C4C4C', '#5C5C5C', '#6C6C6C', '#7C7C7C']
        
        # 创建图片
        image = Image.new('RGB', (width, height), bg_color)
        draw = ImageDraw.Draw(image)
        
        # 生成文本
        text = CaptchaGenerator.generate_text()
        
        try:
            # 获取字体文件路径
            font_path = os.path.join(os.path.dirname(__file__), 'fonts', 'arial.ttf')
            if not os.path.exists(font_path):
                # 如果没有指定字体，使用默认字体
                font = ImageFont.load_default()
            else:
                font = ImageFont.truetype(font_path, 30)
        except Exception:
            font = ImageFont.load_default()

        # 绘制文字
        text_width = width / 4
        for i, char in enumerate(text):
            x = 10 + i * text_width
            y = random.randint(2, 8)
            # 随机选择颜色
            text_color = random.choice(text_colors)
            draw.text((x, y), char, font=font, fill=text_color)

        # 添加干扰线
        for i in range(3):
            x1 = random.randint(0, width)
            y1 = random.randint(0, height)
            x2 = random.randint(0, width)
            y2 = random.randint(0, height)
            draw.line([(x1, y1), (x2, y2)], fill='#DCDCDC', width=1)

        # 添加噪点
        for i in range(30):
            x = random.randint(0, width)
            y = random.randint(0, height)
            draw.point([x, y], fill='#DCDCDC')

        # 转换为base64
        buffer = BytesIO()
        image.save(buffer, format='PNG')
        img_str = base64.b64encode(buffer.getvalue()).decode()

        return {
            'text': text,
            'image': f'data:image/png;base64,{img_str}'
        } 