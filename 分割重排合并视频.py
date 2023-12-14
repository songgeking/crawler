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
            with open('list.txt', 'a') as f:
                f.write('file' + ' ' + filename + '\n')
                f.close()
    return video_list


def cut_video(video_path):  # 切割视频
    videos = load_video(video_path)
    for video in videos:
        ffmpeg_command = f'ffmpeg -i {video} -f segment -segment_time 00:00:02 -c copy output_%02d.mp4'
        # ffmpeg_command = f'ffmpeg -i {video} -f segment -segment_time 2 -reset_timestamps 1 -break_non_keyframes 1 {video_path}\\output_%02d.mp4'  # 这个出来的时间非常准确
        os.system(ffmpeg_command)


def merge_video(video_path):  # 合并视频
    videos = load_video(video_path)
    random.shuffle(videos)  # 打乱顺序
    new_videos = []
    for video in videos:
        if 'output' in video:
            new_videos.append(video)

    txt = video_path + '\list.txt'    
    ffmpeg_command = f'ffmpeg -f concat -i {txt} -c copy concat.mp4'
    os.system(ffmpeg_command)


merge_video('D:\\videos')
