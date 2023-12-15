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
    random.shuffle(video_list)  # 打乱顺序
    for file in video_list:
        if 'output' in file:  # 打开list.txt 文件，把file写入txt里
            path, filename = os.path.split(file)
            txt_path = os.path.join(path, 'list.txt')
            with open(txt_path, 'a') as f:
                f.write('file' + ' ' + filename + '\n')
                f.close()
    return video_list


def cut_video(video_path):  # 切割视频
    videos = load_video(video_path)
    for video in videos:
        output_path = os.path.join(video_path, 'output_%02d.mp4')
        ffmpeg_command = f'ffmpeg -i {video} -f segment -segment_time 00:00:02 -c copy {output_path}'
        os.system(ffmpeg_command)


def merge_video(video_path):  # 合并视频
    videos = load_video(video_path)
    random.shuffle(videos)  # 打乱顺序
    new_videos = []
    for video in videos:
        if 'output' in video:
            new_videos.append(video)

    txt_path = video_path + '\\list.txt'
    ffmpeg_command = f'ffmpeg -f concat -i {txt_path} -c copy {video_path}\\concat.mp4'
    ff_command = ffmpeg_command
    print(ff_command)
    os.system(ffmpeg_command)


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


# cut_video('D:\\shipin')
# merge_video('D:\\shipin')
# video_shake('C:\\Users\\Entel\\Videos')  # 视频去抖
