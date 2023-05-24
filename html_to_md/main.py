import os
import pwd
import random
import shutil

import html2text
import pypandoc
from get_file_from_baidudisk import get_file

def get_folder_files_path(path):
    """Get the relative paths of all files in the current directory
    params: the folder path
    return: file_relative_paths, file_name_list
    """
    file_name_list = os.listdir(path)
    file_relative_paths = [path+"/"+i for i in file_name_list]
    return file_relative_paths, file_name_list
'''

'''
def md_to_word(md_file_folder):
    """transform markdown to word

    Args:
        md_file_paths (md_file_paths:list): the list of transforming markdown file
    """

    md_file_paths, file_names  = get_folder_files_path(md_file_folder)
    if len(md_file_paths) == 1:
        all_path = md_file_paths[0].split('.')[0]+'.docx'
        pypandoc.convert_file(md_file_paths[0], 'docx', outputfile=all_path)
        return
    father_folder = os.path.dirname(md_file_folder[:-1])
    output_folder = father_folder + "/" + md_file_folder.split('/')[-3] + "-docx/"
    for i in md_file_paths:
        # 定义输入和输出文件的路径
        if os.path.isfile(i):
            input_file = i
            if not os.path.exists(output_folder):
                os.makedirs(output_folder)
            output_file = '{}{}.docx'.format(output_folder, i.split('/')[-1].split('.')[0])
            # 调用pypandoc库进行转换
            pypandoc.convert_file(input_file, 'docx', outputfile=output_file)

def html_to_md(floder_path):
    file_relative_paths, file_name_list = get_folder_files_path(floder_path)
    output_folder_name = floder_path + "/" +floder_path.split('/')[-1] + "markdown/"
    dst_folder = floder_path + "/" +floder_path.split('/')[-1] + "html/"
    for i in range(len(file_relative_paths)):
        if not os.path.isdir(file_relative_paths[i]):
            html_file_ob = open(file_relative_paths[i], 'r', encoding='utf-8')
            html_content = html_file_ob.read()

            markdown = html2text.html2text(html_content)
            if not os.path.exists(output_folder_name):
                os.makedirs(output_folder_name)
            with open('{}{}.md'.format(output_folder_name, file_name_list[i].split('.')[0]), 'w', encoding='utf-8') as file:
                file.write(markdown)
            if not os.path.exists(dst_folder):
                os.makedirs(dst_folder)
            dst_file = dst_folder + file_name_list[i]
            with open(dst_file, 'w', encoding='utf-8') as f:
                pass
            shutil.move(file_relative_paths[i], dst_file)
            html_file_ob.close()
    
    return output_folder_name

def merge_files(input_folder, output_file):
    """将文件夹下的所有文件合并成一个文件"""
    # 打开输出文件
    print(input_folder, output_file)
    with open(output_file, 'wb') as output:
        # 遍历文件夹下的所有文件
        for filename in sort_filenames(os.listdir(input_folder)):
            print(filename)
            filepath = os.path.join(input_folder, filename)

            # 如果是文件则进行处理
            if os.path.isfile(filepath):
                # 合并文件
                with open(filepath, 'rb') as input_file:
                    shutil.copyfileobj(input_file, output)
    
def multi_merge_files(input_folder, max_size=20):
    """合并文件夹下的所有文件，并且合并的文件不能大于max_size MB"""
    father_folder = os.path.dirname(input_folder)
    output_folder = father_folder + input_folder.split('/')[-1] + "-merge"
    # 初始化变量
    merged_file_num = 1
    merged_file_size = 0
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    # 遍历文件夹下的所有文件
    for filename in sort_filenames(os.listdir(input_folder)):
        filepath = os.path.join(input_folder, filename)
        suffix = filename.split('.')[-1]
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
    return output_folder + '/'

def modify_md(folder_path, Multipart_count=True):
    """modify the markdown file reduce the 

    Args:
        folder_path (_type_): _description_
        Multipart_count (bool, optional): _description_. Defaults to True.

    Returns:
        _type_: _description_
    """
    father_folder = os.path.dirname(folder_path)
    output_folder = father_folder + folder_path.split('/')[-1] + "-extract/"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
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
        title = '\n' + '# ' + file_path.split('/')[-1].split('.')[0] + '\n'
        res.insert(start, title)
        output_file_path = os.path.join(output_folder, file_path.split('/')[-1])
        with open(output_file_path, 'a', encoding='utf-8') as file:
            file.writelines(res[start:end])
    res_one = ''
    if Multipart_count:
        res_one = multi_merge_files(output_folder, max_size=15)
    else:
        res_one
    # set the all file in the father folder
    all_folder = father_folder
    merge_files(output_folder, all_folder  + folder_path.split('/')[-1] + '.md')
    return res_one, os.path.dirname(all_folder) + "/"
        

def sort_filenames(filenames):
    """
    Sort the list of filenames by the number before the filename
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
    # os.path.abspath(os.path.dirname(pwd)+os.path.sep+".")
    # path not end /
    # path = r'./计算机技术/极客时间/专栏/141-OAuth 2.0实战课'
    path = r'./计算机技术/极客时间/专栏/156-动态规划面试宝典'

    # get_file(path)
    output_folder_name = html_to_md(path)
    # print(output_folder_name)
    merge_extract_folder, all_path = modify_md(output_folder_name, path)
    # print(merge_extract_folder, all_path)
    # md_to_word(merge_extract_folder)
    # md_to_word(all_path)