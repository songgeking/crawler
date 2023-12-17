import random
import os


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
        ffmpeg_command = f'ffmpeg -i {video} -f segment -segment_time 00:00:02 -c copy {output_path}'  # ffmpeg切割视频代码
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
    ffmpeg_command = f'ffmpeg -f concat -i {txt_name} -c copy {video_path}\\{video_name}_concat.mp4'  # 合并视频ffmpeg代码
    os.system(ffmpeg_command)  # 执行ffmpeg命令


def move_video(video_path):  # 移动视频
    dir_list = load_dir(video_path)  # 获取当前文件夹下的所有文件夹
    for dir in dir_list:  # 遍历文件夹
        video_list = load_video(dir)  # 获取文件夹下的所有视频
        for video in video_list:  # 遍历视频
            if 'concat' in video:  # 如果视频名称包含“concat”，则把视频移动到D:\videos\
                output_path = 'd:\\videos'   # 把视频移动到d:\videos,可以改其他文件夹，但要确定文件已经建立了
                os.rename(video, os.path.join(output_path, os.path.basename(video)))  # 将视频移动到目标路径
                
    

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




def main():
    videos_path = 'D:\\视频'  # 视频文件夹路径
    cut_video(videos_path)  # 切割视频
    video_path = load_dir(videos_path)  # 获取切割后的视频文件夹路径
    for path in video_path:
        merge_video(path)  # 合并视频
    move_video(videos_path)  # 移动视频,把合并后的视频移动到D:\videos\


if __name__ == '__main__':
    main()
