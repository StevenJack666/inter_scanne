
'''
OCR测试
'''
if __name__ == "__main__":
    from datetime import datetime

    # 字符串时间
    time_str = "2022-12-31"

    # 格式化字符串
    format_str = "%Y-%m-%d"

    # 将字符串转换为 datetime 对象
    time_obj = datetime.strptime(time_str, "%Y-%m-%d")
    # 将 datetime 对象转换为时间戳
    time_stamp = int(time_obj.timestamp() * 1000)

    print(time_stamp)