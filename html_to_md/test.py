import os

for root, dirs, files in os.walk('/home/luman/文档/01-数据结构与算法之美'):
    print(root, dirs, files)
    print()