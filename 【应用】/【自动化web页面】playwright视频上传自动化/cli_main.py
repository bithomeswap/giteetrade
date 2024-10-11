#作者weixin：lianghuajiaoyi123456
import argparse
import asyncio
import datetime
from os.path import exists
from pathlib import Path

from conf import BASE_DIR
from uploader.douyin_uploader.main import douyin_setup, DouYinVideo
from uploader.ks_uploader.main import ks_setup, KSVideo
from uploader.tencent_uploader.main import weixin_setup, TencentVideo
from uploader.tk_uploader.main_chrome import tiktok_setup, TiktokVideo
from utils.base_social_media import get_supported_social_media, get_cli_action, SOCIAL_MEDIA_DOUYIN, SOCIAL_MEDIA_TENCENT, SOCIAL_MEDIA_TIKTOK, SOCIAL_MEDIA_KUAISHOU
from utils.constant import TencentZoneTypes
from utils.files_times import get_title_and_hashtags

def parse_schedule(schedule_raw):
    if schedule_raw:
        schedule = datetime.strptime(schedule_raw, '%Y-%m-%d %H:%M')
    else:
        schedule = None
    return schedule

async def main():
    # 硬编码参数
    account_name = "19511189162"#用于存放该账户的cookies信息的文件夹

    # 【动作】例如："login","upload"
    # action = "login"#获取cookies
    action = "upload"#发布视频

    # 【平台】例如: douyin, tencent, tiktok, kuaishou
    # platform = "kuaishou"#快手有些细节要改
    platform = "douyin"#抖音完全正常
    # platform = "tencent"#微信无法使用【保存的cookie有问题】
    
    # 视频文件路径【只能英文】
    video_file = r"C:\Users\13480\gitee\trade\【应用】\【自动化web页面】playwright视频上传自动化\videos\demo.mp4"
    publish_type = 0  # 0 立即发布, 1 计划发布

    # schedule = datetime.datetime.now()-datetime.timedelta(days=1) # 计划发布时间
    schedule = datetime.datetime.now()-datetime.timedelta(hours=1) # 计划发布时间（这个时间不对）

    # 参数校验
    if action == 'upload':
        if not exists(video_file):
            raise FileNotFoundError(f'Could not find the video file at {video_file}')
        if publish_type == 1 and not schedule:
            raise ValueError("The schedule must be specified for scheduled publishing.")
    account_file = Path(f"{platform}_{account_name}.json")
    account_file.parent.mkdir(exist_ok=True)
    if action == 'upload':
        if not exists(video_file):
            raise FileNotFoundError(f'Could not find the video file at {video_file}')
        if publish_type == 1 and not schedule:
            print("The schedule must must be specified for scheduled publishing.")
    account_file = Path(f"{platform}_{account_name}.json")
    account_file.parent.mkdir(exist_ok=True)
    # 根据 action 处理不同的逻辑
    if action == 'login':
        print(f"Logging in with account {account_name} on platform {platform}")
        if platform == SOCIAL_MEDIA_DOUYIN:
            await douyin_setup(str(account_file), handle=True)
        elif platform == SOCIAL_MEDIA_TIKTOK:
            await tiktok_setup(str(account_file), handle=True)
        elif platform == SOCIAL_MEDIA_TENCENT:
            await weixin_setup(str(account_file), handle=True)
        elif platform == SOCIAL_MEDIA_KUAISHOU:
            await ks_setup(str(account_file), handle=True)
    elif action == 'upload':
        title, tags = get_title_and_hashtags(video_file)
        video_file = video_file
        if publish_type == 0:
            print("Uploading immediately...")
            publish_date = datetime.datetime.now()
        if platform == SOCIAL_MEDIA_DOUYIN:
            await douyin_setup(account_file, handle=False)
            app = DouYinVideo(title, video_file, tags, publish_date, account_file)
        elif platform == SOCIAL_MEDIA_TIKTOK:
            await tiktok_setup(account_file, handle=True)
            app = TiktokVideo(title, video_file, tags, publish_date, account_file)
        elif platform == SOCIAL_MEDIA_TENCENT:
            await weixin_setup(account_file, handle=True)
            category = TencentZoneTypes.LIFESTYLE.value  # 标记原创需要否则不需要传
            app = TencentVideo(title, video_file, tags, publish_date, account_file, category)
        elif platform == SOCIAL_MEDIA_KUAISHOU:
            await ks_setup(account_file, handle=True)
            app = KSVideo(title, video_file, tags, publish_date, account_file)
        else:
            print("Wrong platform, please check your input")
            exit()
        await app.main()
if __name__ == "__main__":
    asyncio.run(main())
