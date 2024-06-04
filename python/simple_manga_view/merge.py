"""
有文件夹结构如下
- root
  - dir1
    - file1
    - file2
  - dir2
    - file1
    - file2

要求将所有文件合并到一个文件中，按照文件名排序, 得到结果:
- root
  - file1-1 -> 改名为Image00001
  - file1-2 -> 改名为Image00002
  - file2-1 -> 改名为Image00003
"""
import os

root = r'G:\!fin-e\[韩漫]2022年新整理大合集[224本][36.5G]\2024\富家女姐姐'


def merge_files(root):
    files = []
    # 需要合并的文件收到一个arr里
    for dirpath, dirnames, filenames in os.walk(root):
        # dirpath相对盘符的层级 - root相对盘符的层级 = 1, 说明是第一层子文件夹
        level = dirpath.count(os.sep) - root.count(os.sep)
        if level != 1:
            continue
        for filename in filenames:
            files.append(os.path.join(dirpath, filename))
    # 排序
    files.sort()
    # 重命名(剪切位置)
    for i, file in enumerate(files):
        new_file = os.path.join(root, f"Image{i+1:05d}{os.path.splitext(file)[1]}")
        # print(new_file)
        os.rename(file, new_file)


if __name__ == "__main__":
    merge_files(root)
