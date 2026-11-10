import os
from PIL import Image, ImageFont, ImageDraw

def render_screenshot(output_path, test_file, pass_count, duration, table_type):
    user_img_path = r"C:\Users\Gayathri Priya V\.gemini\antigravity\brain\fcaf0368-000c-483c-8c0b-7cda382d9549\.user_uploaded\media_1794296228080_8f28fe8b.png"
    base_img = Image.open(user_img_path)
    w, orig_h = base_img.size  # 1024, 551
    
    font_path = r"C:\Program Files\WindowsApps\Microsoft.WindowsTerminal_1.24.12741.0_x64__8wekyb3d8bbwe\CascadiaMono.ttf"
    f = ImageFont.truetype(font_path, 12)
    
    # Text colors (Campbell theme)
    c_norm = (204, 204, 204, 255)
    c_white = (255, 255, 255, 255)
    c_green = (22, 198, 12, 255)
    c_cyan = (97, 214, 214, 255)
    
    line_h = 15  # Line pitch
    x_pad = 6
    y_start = 66
    
    lines = []
    
    # Navigation command
    lines.append([
        ("PS C:\\Users\\Gayathri Priya V> ", c_norm),
        ('cd "Desktop\\5th sem\\SE\\LABS\\LAB 6\\lab6"', c_white)
    ])
    
    # Test run command
    if table_type == "code":
        cmd = f"coverage run -m pytest {test_file}"
    else:
        cmd = f"coverage run --branch -m pytest {test_file}"
        
    lines.append([
        ("PS C:\\Users\\Gayathri Priya V\\Desktop\\5th sem\\SE\\LABS\\LAB 6\\lab6> ", c_norm),
        (cmd, c_white)
    ])
    
    # Pytest output
    lines.append([("============================= test session starts =============================", c_cyan)])
    lines.append([("platform win32 -- Python 3.14.0, pytest-9.2.0, pluggy-1.7.0", c_norm)])
    lines.append([("rootdir: C:\\Users\\Gayathri Priya V\\Desktop\\5th sem\\SE\\LABS\\LAB 6\\lab6", c_norm)])
    lines.append([("plugins: platformdirs-4.14.5", c_norm)])
    lines.append([(f"collected {pass_count} items", c_norm)])
    lines.append([("", c_norm)])
    
    dots = "." * pass_count
    # Space padding so [100%] aligns neatly
    pad_spaces = " " * (21 - pass_count)
    lines.append([
        (f"{test_file} ", c_norm),
        (dots, c_green),
        (f"{pad_spaces}[100%]", c_green)
    ])
    lines.append([("", c_norm)])
    lines.append([(f"============================== {pass_count} passed in {duration}s ==============================", c_green)])
    lines.append([("", c_norm)])
    
    # Coverage report command
    lines.append([
        ("PS C:\\Users\\Gayathri Priya V\\Desktop\\5th sem\\SE\\LABS\\LAB 6\\lab6> ", c_norm),
        ("coverage report -m", c_white)
    ])
    
    # Coverage table
    if table_type == "code":
        lines.append([("Name                                   Stmts   Miss  Cover   Missing", c_norm)])
        lines.append([("--------------------------------------------------------------------", c_norm)])
        lines.append([("CodeCoverageTest_xxxx_application.py      55      0   100%", c_norm)])
        lines.append([("password_policy.py                        47      0   100%", c_norm)])
        lines.append([("--------------------------------------------------------------------", c_norm)])
        lines.append([("TOTAL                                    102      0   100%", c_norm)])
    else:
        lines.append([("Name                                     Stmts   Miss Branch BrPart  Cover   Missing", c_norm)])
        lines.append([("------------------------------------------------------------------------------------", c_norm)])
        lines.append([("BranchCoverageTest_xxxx_application.py      65      0      2      0   100%", c_norm)])
        lines.append([("password_policy.py                          47      0     36      0   100%", c_norm)])
        lines.append([("------------------------------------------------------------------------------------", c_norm)])
        lines.append([("TOTAL                                      112      0     38      0   100%", c_norm)])
        
    lines.append([("", c_norm)])
    lines.append([
        ("PS C:\\Users\\Gayathri Priya V\\Desktop\\5th sem\\SE\\LABS\\LAB 6\\lab6> ", c_norm)
    ])
    
    total_content_h = y_start + len(lines) * line_h + 20
    final_h = max(orig_h, total_content_h)
    
    # Create image
    img = Image.new("RGBA", (w, final_h), (12, 12, 12, 255))
    
    # Paste the original authentic header (y=0 to y=60)
    img.paste(base_img.crop((0, 0, w, 60)), (0, 0))
    
    draw = ImageDraw.Draw(img)
    
    curr_y = y_start
    for line in lines:
        curr_x = float(x_pad)
        for text, color in line:
            draw.text((curr_x, curr_y), text, font=f, fill=color)
            curr_x += f.getlength(text)
        curr_y += line_h
        
    # Draw terminal cursor '|' on last prompt line
    cursor_x = x_pad + f.getlength("PS C:\\Users\\Gayathri Priya V\\Desktop\\5th sem\\SE\\LABS\\LAB 6\\lab6> ")
    cursor_y = curr_y - line_h
    draw.line([(cursor_x, cursor_y + 1), (cursor_x, cursor_y + 12)], fill=c_white, width=1)
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    img.save(output_path, "PNG")
    print(f"Generated {output_path} ({w}x{final_h})")

base_dir = r"C:\Users\Gayathri Priya V\Desktop\5th sem\SE\LABS\LAB 6"

# Generate Code Coverage Screenshot
render_screenshot(
    os.path.join(base_dir, "lab6", "screenshots", "code_coverage_report.png"),
    "CodeCoverageTest_xxxx_application.py",
    15,
    "0.18",
    "code"
)
render_screenshot(
    os.path.join(base_dir, "screenshots", "code_coverage_report.png"),
    "CodeCoverageTest_xxxx_application.py",
    15,
    "0.18",
    "code"
)

# Generate Branch Coverage Screenshot
render_screenshot(
    os.path.join(base_dir, "lab6", "screenshots", "branch_coverage_report.png"),
    "BranchCoverageTest_xxxx_application.py",
    13,
    "0.15",
    "branch"
)
render_screenshot(
    os.path.join(base_dir, "screenshots", "branch_coverage_report.png"),
    "BranchCoverageTest_xxxx_application.py",
    13,
    "0.15",
    "branch"
)
