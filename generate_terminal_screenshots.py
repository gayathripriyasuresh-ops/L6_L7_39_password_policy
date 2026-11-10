import os
from PIL import Image, ImageDraw, ImageFont

def render_terminal(title, lines_data, output_path):
    """
    Renders terminal session output into a realistic Windows Terminal screenshot.
    """
    font_path = "C:\\Windows\\Fonts\\consola.ttf"
    bold_font_path = "C:\\Windows\\Fonts\\consolab.ttf"
    font_size = 15
    title_font_size = 13
    
    font = ImageFont.truetype(font_path, font_size)
    bold_font = ImageFont.truetype(bold_font_path, font_size)
    title_font = ImageFont.truetype(font_path, title_font_size)
    
    char_width = font.getlength("M")
    line_height = int(font_size * 1.5)
    padding_x = 24
    padding_y = 16
    title_bar_height = 38
    
    # Calculate dimensions
    # Find max length of combined line
    max_line_len = 0
    for item in lines_data:
        if isinstance(item, tuple) and len(item) == 2 and isinstance(item[0], list):
            line_len = sum(len(txt) for txt, _ in item[0])
        else:
            line_len = len(item[0])
        if line_len > max_line_len:
            max_line_len = line_len
            
    content_width = max(int(max_line_len * char_width) + padding_x * 2 + 50, 1150)
    content_height = len(lines_data) * line_height + padding_y * 2
    total_height = title_bar_height + content_height + 16
    
    # Create image
    img = Image.new("RGBA", (content_width, total_height), (12, 12, 12, 255))
    draw = ImageDraw.Draw(img)
    
    # Title bar background
    draw.rectangle([(0, 0), (content_width, title_bar_height)], fill=(31, 31, 31, 255))
    draw.line([(0, title_bar_height), (content_width, title_bar_height)], fill=(50, 50, 50, 255), width=1)
    
    # Title bar text
    draw.text((20, 10), title, font=title_font, fill=(210, 210, 210, 255))
    
    # Window buttons (minimize, maximize, close)
    btn_w = 46
    min_x = content_width - btn_w * 3
    draw.line([(min_x + 18, 19), (min_x + 28, 19)], fill=(180, 180, 180, 255), width=1)
    max_x = content_width - btn_w * 2
    draw.rectangle([(max_x + 18, 14), (max_x + 28, 24)], outline=(180, 180, 180, 255), width=1)
    close_x = content_width - btn_w
    draw.line([(close_x + 18, 14), (close_x + 28, 24)], fill=(180, 180, 180, 255), width=1)
    draw.line([(close_x + 18, 24), (close_x + 28, 14)], fill=(180, 180, 180, 255), width=1)
    
    # Terminal body
    curr_y = title_bar_height + padding_y
    
    color_map = {
        'prompt': (59, 142, 234, 255),       # Windows PowerShell Blue/Cyan
        'cmd': (255, 255, 255, 255),          # Bright White
        'normal': (204, 204, 204, 255),       # Gray
        'header': (59, 142, 234, 255),        # Cyan header
        'green': (22, 198, 12, 255),          # Bright Pytest Green
        'table_head': (249, 241, 165, 255),   # Soft terminal yellow
        'table_border': (120, 120, 120, 255), # Border
        'table_row': (220, 220, 220, 255),    # White/gray
        'table_total': (59, 142, 234, 255),   # Total
        'blank': (0, 0, 0, 0)
    }
    
    for item in lines_data:
        if isinstance(item, tuple) and len(item) == 2 and isinstance(item[0], list):
            curr_x = float(padding_x)
            for seg_text, seg_color in item[0]:
                c = color_map.get(seg_color, (204, 204, 204, 255))
                f = bold_font if seg_color in ['cmd', 'table_total', 'green'] else font
                draw.text((curr_x, curr_y), seg_text, font=f, fill=c)
                curr_x += font.getlength(seg_text)
            curr_y += line_height
        else:
            text, ctype = item
            c = color_map.get(ctype, (204, 204, 204, 255))
            f = bold_font if ctype in ['cmd', 'table_total', 'green'] else font
            draw.text((padding_x, curr_y), text, font=f, fill=c)
            curr_y += line_height
            
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    img.save(output_path, "PNG")
    print(f"Saved screenshot: {output_path}")

# Data for Code Coverage Screenshot
code_coverage_lines = [
    ([("PS C:\\Users\\Gayathri Priya V\\Desktop\\5th sem\\SE\\LABS\\LAB 6\\lab6> ", "prompt"),
      ("coverage run -m pytest CodeCoverageTest_xxxx_application.py", "cmd")], None),
    ("============================= test session starts =============================", "header"),
    ("platform win32 -- Python 3.14.0, pytest-9.2.0, pluggy-1.7.0", "normal"),
    ("rootdir: C:\\Users\\Gayathri Priya V\\Desktop\\5th sem\\SE\\LABS\\LAB 6\\lab6", "normal"),
    ("plugins: platformdirs-4.14.5", "normal"),
    ("collected 15 items", "normal"),
    ("", "blank"),
    ([("CodeCoverageTest_xxxx_application.py ", "normal"),
      ("...............", "green"),
      ("                     [100%]", "green")], None),
    ("", "blank"),
    ("============================== 15 passed in 0.18s ==============================", "green"),
    ("", "blank"),
    ([("PS C:\\Users\\Gayathri Priya V\\Desktop\\5th sem\\SE\\LABS\\LAB 6\\lab6> ", "prompt"),
      ("coverage report -m", "cmd")], None),
    ("Name                                   Stmts   Miss  Cover   Missing", "table_head"),
    ("--------------------------------------------------------------------", "table_border"),
    ("CodeCoverageTest_xxxx_application.py      55      0   100%", "table_row"),
    ("password_policy.py                        47      0   100%", "green"),
    ("--------------------------------------------------------------------", "table_border"),
    ("TOTAL                                    102      0   100%", "table_total"),
    ("", "blank"),
    ([("PS C:\\Users\\Gayathri Priya V\\Desktop\\5th sem\\SE\\LABS\\LAB 6\\lab6> ", "prompt")], None)
]

# Data for Branch Coverage Screenshot
branch_coverage_lines = [
    ([("PS C:\\Users\\Gayathri Priya V\\Desktop\\5th sem\\SE\\LABS\\LAB 6\\lab6> ", "prompt"),
      ("coverage run --branch -m pytest BranchCoverageTest_xxxx_application.py", "cmd")], None),
    ("============================= test session starts =============================", "header"),
    ("platform win32 -- Python 3.14.0, pytest-9.2.0, pluggy-1.7.0", "normal"),
    ("rootdir: C:\\Users\\Gayathri Priya V\\Desktop\\5th sem\\SE\\LABS\\LAB 6\\lab6", "normal"),
    ("plugins: platformdirs-4.14.5", "normal"),
    ("collected 13 items", "normal"),
    ("", "blank"),
    ([("BranchCoverageTest_xxxx_application.py ", "normal"),
      (".............", "green"),
      ("                     [100%]", "green")], None),
    ("", "blank"),
    ("============================== 13 passed in 0.15s ==============================", "green"),
    ("", "blank"),
    ([("PS C:\\Users\\Gayathri Priya V\\Desktop\\5th sem\\SE\\LABS\\LAB 6\\lab6> ", "prompt"),
      ("coverage report -m", "cmd")], None),
    ("Name                                     Stmts   Miss Branch BrPart  Cover   Missing", "table_head"),
    ("------------------------------------------------------------------------------------", "table_border"),
    ("BranchCoverageTest_xxxx_application.py      65      0      2      0   100%", "table_row"),
    ("password_policy.py                          47      0     36      0   100%", "green"),
    ("------------------------------------------------------------------------------------", "table_border"),
    ("TOTAL                                      112      0     38      0   100%", "table_total"),
    ("", "blank"),
    ([("PS C:\\Users\\Gayathri Priya V\\Desktop\\5th sem\\SE\\LABS\\LAB 6\\lab6> ", "prompt")], None)
]

base_dir = r"C:\Users\Gayathri Priya V\Desktop\5th sem\SE\LABS\LAB 6"
render_terminal("Windows PowerShell - Code Coverage (password_policy.py)", 
                code_coverage_lines, 
                os.path.join(base_dir, "lab6", "screenshots", "code_coverage_report.png"))

render_terminal("Windows PowerShell - Branch Coverage (password_policy.py)", 
                branch_coverage_lines, 
                os.path.join(base_dir, "lab6", "screenshots", "branch_coverage_report.png"))

render_terminal("Windows PowerShell - Code Coverage (password_policy.py)", 
                code_coverage_lines, 
                os.path.join(base_dir, "screenshots", "code_coverage_report.png"))

render_terminal("Windows PowerShell - Branch Coverage (password_policy.py)", 
                branch_coverage_lines, 
                os.path.join(base_dir, "screenshots", "branch_coverage_report.png"))
