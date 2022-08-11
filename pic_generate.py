from PIL import Image, ImageFont, ImageDraw
import glob
from math import ceil
import textwrap

chapters = glob.glob('clean_novel/*.txt')
words_per_line = 55
font_path = 'C:\\Windows\\fonts\\SIMHEI.TTF'
font = ImageFont.truetype(font_path, 15)
_, _, w, h = font.getbbox('哈')
line_spacing = 4
h = h + line_spacing

if __name__ == '__main__':

    for chapter in chapters:
        with open(chapter, encoding='utf-8') as f:
            lines = f.readlines()

        n_lines = 0
        new_text = ''
        for line in lines:
            n_lines += ceil(len(line) / words_per_line)
            new_text += '\n'.join(textwrap.wrap(line, words_per_line)) + '\n'

        img_length = (n_lines + 16) * h * 0.9
        img_width = w * (words_per_line + 16)

        img = Image.new('RGB', (int(img_width), int(img_length)), (255, 255, 255))
        d = ImageDraw.Draw(img)
        d.multiline_text((8 * w, 8 * h), new_text, font=font, fill=(0, 0, 0), spacing=line_spacing)
        img.show()
        img.save(chapter.replace('.txt', '.png').replace('clean_novel', 'pic').replace('三国', '三国演义'), quality=100, subsampling=0)
        img.close()
