import random
import os
import time
import shutil


def load_dir(path):  # 读取当前文件夹下的所有文件夹
    dir_list = []
    for file in os.listdir(path):
        if os.path.isdir(os.path.join(path, file)):
            dir_list.append(os.path.join(path, file))
    return dir_list


def load_video(mp4_path):  # 读取当前文件夹下的mp4文件+
    video_list = []
    for file in os.listdir(mp4_path):
        if file.endswith('.mp4'):
            video_list.append(os.path.join(mp4_path, file))    
    return video_list


def cut_video(video_path):  # 切割视频
    videos = load_video(video_path)    
    for video in videos:
        video_name = os.path.basename(video).replace('.mp4', '')        
        if not os.path.exists(os.path.join(video_path, video_name)):  # 新建目录video_path\video_name
            os.mkdir(os.path.join(video_path, video_name))
            print(os.path.join(video_path, video_name))
            print('新建目录成功')            
        output_path = os.path.join(video_path,  video_name, f'{video_name}_output_%02d.mp4')  # 拼接输出路径和文件名
        print(output_path)
        ffmpeg_command = f'ffmpeg -safe 0 -i {video} -f segment -segment_time 00:00:02 -c copy {output_path}'  # ffmpeg切割视频代码
        os.system(ffmpeg_command)


def merge_video(video_path):  # 合并视频
    videos = load_video(video_path)    
    video_name = os.path.basename(video_path)  # 获取当前目录名    
    random.shuffle(videos)  # 打乱顺序
    txt_name = video_path + '\\list.txt'  # 生成txt文件保存视频路径
    for video in videos:  # 将视频路径写入txt文件中        
        video = os.path.basename(video)  # 获取文件夹名
        with open(txt_name, 'a', encoding='utf-8') as f:  # 以追加的方式写入txt文件中            
            f.write('file ' + video + '\n')  # 将视频路径写入txt文件中，格式（file xx.mp4）
            f.close()
    ffmpeg_command = f'ffmpeg -f concat -safe 0 -i {txt_name} -c copy {video_path}\\{video_name}_concat.mp4'  # 合并视频ffmpeg代码
    os.system(ffmpeg_command)  # 执行ffmpeg命令


def move_video(video_path, output_path):  # 移动视频
    dir_list = load_dir(video_path)  # 获取当前文件夹下的所有文件夹
    for dir in dir_list:  # 遍历文件夹
        video_list = load_video(dir)  # 获取文件夹下的所有视频        
        for video in video_list:  # 遍历视频
            if 'concat' in video:  # 如果视频名称包含“concat”，则把视频移动到D:\videos\                               
                shutil.move(video, output_path)  # 将视频移动到目标路径
    # 重命名output_path里的所有文件


def rename(re_path):
    name_list = load_video(re_path)
    for name in name_list:
        new_name = name.replace('_concat', '')
        os.rename(name, new_name)
    print('已完成重命名')
    

# 视频去抖
def video_shake(video_path):
    videos = load_video(video_path)
    for video in videos:
        output_path = os.path.join(video_path, 'fangdou.mp4')
        ff_cmd = f'ffmpeg -i {video} -vf vidstabdetect=stepsize=32:shakiness=10:accuracy=10:result=transform_vectors.trf -f null -'
        ff_cmd2 = f'ffmpeg -i {video} -vf vidstabtransform=input=transform_vectors.trf:zoom=0:smoothing=10 {output_path}'
        os.system(ff_cmd)
        print('------------------------------')
        os.system(ff_cmd2)
        # 删除transform_vectors.trf
        os.remove('transform_vectors.trf')


def main():
    videos_path = '\\\\192.168.2.254\\Downloads\\video'  # 视频文件夹路径
    re_path = 'D:\\videos'  # 重命名output_path里的所有文件
    cut_video(videos_path)  # 切割视频
    video_path = load_dir(videos_path)  # 获取切割后的视频文件夹路径
    for path in video_path:
        merge_video(path)  # 合并视频
    time.sleep(5)  # 等待5秒钟，等待合并视频完成
    move_video(videos_path, re_path)  # 移动视频,把合并后的视频移动到D:\videos\
    time.sleep(10)  # 等待5秒钟，等待移动视频完成
    rename(re_path)  # 重命名output_path里的所有文件


if __name__ == '__main__':
    main()    
    
