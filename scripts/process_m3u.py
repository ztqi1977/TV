# -*- coding: utf-8 -*-
import re
import sys

def update_ipv6(in_file, out_file):
    # 编译正则表达式以提高效率
    tvg_name_pattern = re.compile(r'tvg-name="([^"]+)"')

    # 定义需要提取的 tvg-name 列表
    target_channels = {"CCTV1", "CCTV4", "CCTV6", "CCTV7", "CCTV8"}

    try:
        with open(in_file, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        filtered_lines = ["#EXTM3U"]  # 确保头部信息总是存在
        for i in range(len(lines)):
            if lines[i].startswith("#EXTINF:-1"):
                match = tvg_name_pattern.search(lines[i])
                if match and match.group(1) in target_channels:
                    filtered_lines.append(lines[i].rstrip('\n'))  # 移除行尾换行符
                    if i + 1 < len(lines):  # 检查索引是否越界
                        filtered_lines.append(lines[i + 1].rstrip('\n'))

        with open(out_file, 'w', encoding='utf-8') as temp_file:
            temp_file.write("\n".join(filtered_lines))

    except Exception as e:
        print(f"An error occurred: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python process_m3u.py <input_file> <output_file>", file=sys.stderr)
        sys.exit(1)

    in_file = sys.argv[1]
    out_file = sys.argv[2]
    update_ipv6(in_file, out_file)
