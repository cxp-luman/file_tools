import os
import random
import shutil

import html2text
import pypandoc


def get_folder_files_path(path):
    """获取当前目录下的所有文件相对路径
    params: the folder path
    return: file_relative_paths, file_name_list
    """
    file_name_list = os.listdir(path)
    file_relative_paths = [path+i for i in file_name_list]
    return file_relative_paths, file_name_list
'''

'''
def md_to_word(md_file_paths):
    """transform markdown to word

    Args:
        md_file_paths (md_file_paths:list): the list of transforming markdown file
    """
    for i in md_file_paths:
        # 定义输入和输出文件的路径
        input_file = i
        if not os.path.exists('./{}docx'.format(i.split('/')[0])):
            os.makedirs('./{}docx'.format(i.split('/')[0]))
        output_file = '{}docx/{}.docx'.format(i.split('/')[0], i.split('/')[-1].split('.')[0])

        # 调用pypandoc库进行转换
        pypandoc.convert_file(input_file, 'docx', outputfile=output_file)

def html_to_md(file_relative_paths, file_name_list, output_folder_name):
    for i in range(len(file_relative_paths)):
        html_file_ob = open(file_relative_paths[i], 'r', encoding='utf-8')
        html_content = html_file_ob.read()

        markdown = html2text.html2text(html_content)
        if not os.path.exists(output_folder_name):
            os.makedirs(output_folder_name)
        with open('{}{}.md'.format(output_folder_name, file_name_list[i].split('.')[0]), 'w', encoding='utf-8') as file:
            file.write(markdown)
        html_file_ob.close()
    return output_folder_name

def merge_files(input_folder, output_file):
    """将文件夹下的所有文件合并成一个文件"""
    # 打开输出文件
    with open(output_file, 'wb') as output:
        # 遍历文件夹下的所有文件
        for filename in sort_filenames(os.listdir(input_folder)):
            filepath = os.path.join(input_folder, filename)

            # 如果是文件则进行处理
            if os.path.isfile(filepath):
                # 合并文件
                with open(filepath, 'rb') as input_file:
                    shutil.copyfileobj(input_file, output)
    
def multi_merge_files(input_folder, output_folder, suffix, max_size=20):
    """合并文件夹下的所有文件，并且合并的文件不能大于max_size MB"""

    # 初始化变量
    merged_file_num = 1
    merged_file_size = 0
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    # 遍历文件夹下的所有文件
    for filename in sort_filenames(os.listdir(input_folder)):
        filepath = os.path.join(input_folder, filename)

        # 如果是文件则进行处理
        if os.path.isfile(filepath):
            # 如果当前文件大小大于20MB，则需要新建一个文件进行合并
            if merged_file_size + os.path.getsize(filepath) > max_size * 1024 * 1024:
                merged_file_num += 1
                merged_file_size = 0

            # 拼接输出文件名
            output_filename = "merged_{}_{}.{}".format(input_folder.split('/')[-1], merged_file_num, suffix)
            output_filepath = os.path.join(output_folder, output_filename)

            # 合并文件
            with open(output_filepath, 'ab') as output_file:
                with open(filepath, 'rb') as input_file:
                    shutil.copyfileobj(input_file, output_file)

            # 更新变量
            merged_file_size += os.path.getsize(filepath)


def modify_md(folder_path, output_name, Multipart_count=True):
    os.makedirs(output_name)
    file_relative_paths, _ = get_folder_files_path(folder_path)
    sorted_file_relative_paths = sort_filenames(file_relative_paths)
    for i in range(len(sorted_file_relative_paths)):
        file_path = sorted_file_relative_paths[i]
        with open(file_path, 'r', encoding='utf-8') as f:
            res = f.readlines()
        start, end  = 0, 0
        for line_index in range(len(res)):
            if '时长' in res[line_index]:
                start = line_index + 3
            if '©' in res[line_index]:
                end = line_index - 2
        print(file_path)
        title = '\n' + '# ' + file_path.split('/')[-1].split('.')[0] + '\n'
        res.insert(start, title)
        output_file_path = os.path.join(output_name, file_path.split('/')[-1])
        with open(output_file_path, 'a', encoding='utf-8') as file:
            file.writelines(res[start:end])
    if Multipart_count:
        multi_merge_files(output_name, output_name + '分片合并', 'md', max_size=18)
    all_folder = output_name+'all'
    os.makedirs(all_folder)
    merge_files(output_name, all_folder + '/' + output_name+'.md')
        

def sort_filenames(filenames):
    """
    将文件名列表按照文件名前数字排序
    """
    def filter(x):
        x = x.split('/')[-1]
        try:
            int(x.split("丨")[0])
        except:
            return random.randint(100,120)
        return int(x.split("丨")[0])
    sorted_filenames = sorted(filenames, key=lambda x: filter(x))
    return sorted_filenames

if __name__ == '__main__':
    path = r'./高并发40讲/'
    file_relative_paths, file_name_list = get_folder_files_path(path)
    sorted_files = sort_filenames(file_name_list)
    output_folder_name = html_to_md(file_relative_paths, file_name_list, r'./高并发40讲md/')
    modify_md(output_folder_name, '高并发40讲modify')
    res, _ = get_folder_files_path('高并发40讲modify分片合并/')
    md_to_word(res)