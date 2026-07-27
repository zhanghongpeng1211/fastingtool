#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fix_paths.py — 一键修复站群所有HTML文件的CSS/JS路径
把绝对路径 /style.css 和 /ads-loader.js 改成相对路径

用法:
    python fix_paths.py <站点文件夹路径>

示例:
    python fix_paths.py D:\桌面文件\fastingtool
    python fix_paths.py /home/user/fastingtool
"""

import os
import sys

def get_relative_prefix(file_path, root_dir):
    """计算文件到根目录的相对路径前缀"""
    rel = os.path.relpath(file_path, root_dir)
    depth = rel.count(os.sep)
    if depth == 0:
        return ''
    return '../' * depth

def fix_file(file_path, root_dir):
    """修复单个HTML文件的路径"""
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    original = content
    prefix = get_relative_prefix(file_path, root_dir)

    # 修复CSS路径
    content = content.replace('href="/style.css"', f'href="{prefix}style.css"')
    content = content.replace("href='/style.css'", f'href="{prefix}style.css"')

    # 修复JS路径
    content = content.replace('src="/ads-loader.js"', f'src="{prefix}ads-loader.js"')
    content = content.replace("src='/ads-loader.js'", f'src="{prefix}ads-loader.js"')

    # 修复ads-loader.js里的fetch路径
    content = content.replace("fetch('/ads.json')", f"fetch('{prefix}ads.json')")
    content = content.replace('fetch("/ads.json")', f'fetch("{prefix}ads.json")')

    if content != original:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def main():
    if len(sys.argv) < 2:
        print("用法: python fix_paths.py <站点文件夹路径>")
        print("示例: python fix_paths.py D:\\桌面文件\\fastingtool")
        sys.exit(1)

    root_dir = os.path.abspath(sys.argv[1])

    if not os.path.isdir(root_dir):
        print(f"错误: 路径不存在 {root_dir}")
        sys.exit(1)

    fixed_count = 0
    total_count = 0

    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith('.html'):
                total_count += 1
                file_path = os.path.join(dirpath, filename)
                if fix_file(file_path, root_dir):
                    fixed_count += 1
                    rel = os.path.relpath(file_path, root_dir)
                    prefix = get_relative_prefix(file_path, root_dir)
                    print(f"[已修复] {rel}  →  CSS/JS前缀: '{prefix}'")

    print(f"\n扫描完成: {total_count} 个HTML文件")
    print(f"修复完成: {fixed_count} 个文件")
    print(f"无需修改: {total_count - fixed_count} 个文件")

if __name__ == '__main__':
    main()
