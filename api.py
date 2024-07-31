from pathlib import Path
import logging

from quart import Quart, jsonify, request


from conf import BASE_DIR
from db.account import SessionLocal, Account
from douyin_uploader.main import douyin_setup
from tencent_uploader.main import weixin_setup
from tk_uploader.main_chrome import tiktok_setup
from utils.base_social_media import (
    SOCIAL_MEDIA_DOUYIN,
    SOCIAL_MEDIA_TENCENT,
    SOCIAL_MEDIA_TIKTOK,
)
from utils.files_times import get_videos

app = Quart(__name__)


# 请求上下文中初始化和关闭数据库 session
@app.before_request
def create_session():
    request.db = SessionLocal()


@app.teardown_request
def remove_session(exception=None):
    SessionLocal.remove()


# 登录获取cookie接口 可传cookie字符串/出二维码自己识别
@app.route("/api/login/<platform>/<account>", Methods=["POST"])
async def login(platform, account):
    print(f"Logging in with account {account} on platform {platform}")

    # TODO 优化一下保存到数据库
    # cookie保存地址
    account_file = Path(BASE_DIR / "cookies" / f"{platform}_{account}.json")
    # 查询账号信息
    account_user = request.db.query(Account).filter(Account.platform == platform and Account.name == account).first()
    if account_user:
        account_user.cookie_path = account_file
        request.db.update(account_user)
    else:
        account_user = Account(platform=platform, name=account, cookie_path=account_file)
        request.db.add(account_user)
    account_file.parent.mkdir(exist_ok=True)
    cookie_gen_result = False
    if platform == SOCIAL_MEDIA_DOUYIN:
        cookie_gen_result = await douyin_setup(str(account_file), handle=True)
    elif platform == SOCIAL_MEDIA_TIKTOK:
        cookie_gen_result = await tiktok_setup(str(account_file), handle=True)
    elif platform == SOCIAL_MEDIA_TENCENT:
        cookie_gen_result = await weixin_setup(str(account_file), handle=True)

    request.db.commit()
    
    return jsonify(message=f"cookie 生成, {'成功' if cookie_gen_result else '失败'}!", account=account_user)


# 设置目标文件夹：平台/账号/目标文件夹
@app.route("/api/set_target_folder/", methods=["POST"])
def set_target_folder(dest_folder):
    pass


# 获取文件夹下的文件列表
@app.route("/api/list_videos", methods=["POST"])
def list_videos():
    pass


# 多平台发布接口：平台/账号/目标文件/标题/标签/发布时间
@app.route("/api/upload/<platform>", methods=["POST", "GET"])
def upload(platform):
    mp4_files = get_videos(r"D:\MyProject\f2\Download\douyin\post\_睿睿妈")
    if mp4_files is not None:
        print("xxx")
        # title, tags = get_title_and_hashtags(video_file)
    # video_file = args.video_file
    #
    # if args.publish_type == 0:
    #     print("Uploading immediately...")
    #     publish_date = 0
    # else:
    #     print("Scheduling videos...")
    #     publish_date = parse_schedule(args.schedule)
    #
    # if args.platform == SOCIAL_MEDIA_DOUYIN:
    #     await douyin_setup(account_file, handle=False)
    #     app = DouYinVideo(title, video_file, tags, publish_date, account_file)
    # elif args.platform == SOCIAL_MEDIA_TIKTOK:
    #     await tiktok_setup(account_file, handle=True)
    #     app = TiktokVideo(title, video_file, tags, publish_date, account_file)
    # elif args.platform == SOCIAL_MEDIA_TENCENT:
    #     await weixin_setup(account_file, handle=True)
    #     category = TencentZoneTypes.LIFESTYLE.value  # 标记原创需要否则不需要传
    #     app = TencentVideo(title, video_file, tags, publish_date, account_file, category)
    #
    # await app.main()

    return {"message": f"文件列表: {mp4_files}"}


if __name__ == "__main__":
    # 创建日志记录器
    logger = logging.getLogger(__name__)
    # 设置日志级别
    logger.setLevel(logging.INFO)
    # 创建处理器
    handler = logging.StreamHandler()
    # 设置处理器级别
    handler.setLevel(logging.INFO)
    # 创建格式器
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    # 添加格式器到处理器
    handler.setFormatter(formatter)
    # 添加处理器到日志记录器
    logger.addHandler(handler)
    # 返回报文中文乱码处理
    app.json.ensure_ascii = False
    app.run(debug=True)
