from fontTools.ttLib import TTFont

def get_supported_characters(font_file):
    """
    获取字体支持的字符列表和总数量
    """
    # 加载字体文件
    font = TTFont(font_file)
    cmap_table = font["cmap"]

    # 获取 Unicode 映射表
    characters = set()
    for cmap in cmap_table.tables:
        if cmap.platformID == 3 and cmap.platEncID in [1, 10]:  # Windows Unicode BMP 和 Full Repertoire
            characters.update(cmap.cmap.keys())

    # 返回字符集和支持的字符数量
    return characters, len(characters)

def get_name(record_id, font, platform_id=3, encoding_id=1, language_id=0x409):
    """
    从 fontTools 获取字体的名称记录 (例如 Family Name, Style Name)
    """
    name_table = font["name"]
    for record in name_table.names:
        if (record.nameID == record_id and
            record.platformID == platform_id and
            record.platEncID == encoding_id and
            record.langID == language_id):
            return str(record.string, encoding="utf-16-be")
    return None

def extract_font_properties(font_file):
    """
    从 TTF/OTF 文件提取字体的主要属性。
    """
    # 加载字体文件
    font = TTFont(font_file)

    # 1. 获取字体名称
    family_name = get_name(1, font) if get_name(1, font) else "Unknow"  # Family Name
    style_name = get_name(2, font) if get_name(2, font) else "Unknow"  # Subfamily (Style)
    full_name = get_name(4, font) if get_name(4, font) else "Unknow"  # Full Font Name

    # 2. 获取字体权重和斜体信息
    os2_table = font.get("OS/2", 'Unknow')
    weight_class = os2_table.usWeightClass if os2_table != "Unknow" else "Unknow"  # 字体权重 (100-900)
    is_italic = bool(os2_table.fsSelection & 0x01) if os2_table != "Unknow" else "Unknow"  # 判断是否斜体

    # 3. 获取下划线位置和厚度
    post_table = font.get("post", 'Unknow')
    underline_position = post_table.underlinePosition if post_table != "Unknow" else "Unknow"
    underline_thickness = post_table.underlineThickness if post_table != "Unknow" else "Unknow"

    # 4. 获取字体行高信息（从 hhea 表）
    hhea_table = font.get("hhea", "Unknow")
    ascender = hhea_table.ascent if hhea_table != "Unknow" else "Unknow"
    descender = hhea_table.descent if hhea_table != "Unknow" else "Unknow"
    line_gap = hhea_table.lineGap if hhea_table != "Unknow" else "Unknow"

    # 5. 获取字体支持的字符集和数量
    characters, char_count = get_supported_characters(font_file)

    # 结果输出
    properties, maps = {
        "家族": family_name,
        "样式": style_name,
        "完整名字": full_name,
        "粗细": weight_class,
        "是否斜体": is_italic,
        "垂直偏移量": underline_position,
        "下划线粗细": underline_thickness,
        "Ascender": ascender,
        "Descender": descender,
        "Line Gap": line_gap,
        "支持字符数量": char_count if char_count != 0 else 'Unknow'
    }, "".join(chr(c) for c in characters if c <= 0xFFFF)

    return properties, maps

def convert_otf_to_ttf(input_path, output_path):
    """将 OTF 转换为 TTF"""
    try:
        # 加载 OTF 文件
        font = TTFont(input_path)
        # 保存为 TTF 格式
        font.save(output_path)
        print(f"转换成功: {input_path} -> {output_path}")
    except Exception as e:
        print(f"转换失败: {e}")

__all__ = ['extract_font_properties', 'convert_otf_to_ttf']

if __name__ == "__main__":
    # 设置字体文件路径
    font_file = "fonts\\monaco.ttf"

    # 提取并打印字体属性
    properties, _ = extract_font_properties(font_file)
    for key, value in properties.items():
        if key == "支持字符列表":
            print(f"{key}: {value[:50]}...")  # 显示前 50 个字符，避免列表过长
        else:
            print(f"{key}: {value}")
