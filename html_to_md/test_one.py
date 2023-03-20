import os
import shutil

def merge_files(input_folder, output_folder, suffix, max_size=20):
    """合并文件夹下的所有文件，并且合并的文件不能大于max_size MB"""

    # 初始化变量
    merged_file_num = 1
    merged_file_size = 0
    os.makedirs(output_folder)
    # 遍历文件夹下的所有文件
    for filename in os.listdir(input_folder):
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

if __name__ == '__main__':
    # 测试代码
    merge_files('高并发40讲md', 'output_folder', 'md', max_size=18)
    
import schedule
import time

def task():
    print("Job Executing!")

# for every n minutes
schedule.every(10).minutes.do(task)

# every hour
schedule.every().hour.do(task)

# every daya at specific time
schedule.every().day.at("10:30").do(task)

# schedule by name of day
schedule.every().monday.do(task)

# name of day with time
schedule.every().wednesday.at("13:15").do(task)

while True:
    schedule.run_pending()
    time.sleep(1)