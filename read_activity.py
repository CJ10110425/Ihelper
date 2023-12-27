import json

with open('data.json', 'r', encoding='utf-8') as json_file:
    data = json.load(json_file)



def read_organizer():
    organizer = data['TextContent']['Activity']['ActivityInfo']['活動主辦方']
    return str(organizer)


def read_location():
    location = data['TextContent']['Activity']['ActivityInfo']['活動地點']
    return str(location)


def read_time():
    time = data['TextContent']['Activity']['ActivityInfo']['活動時間']
    return str(time)


def read_merchant_guide():
    merchant_guide = data['TextContent']['Activity']['ActivityInfo']['商家指南']
    result = []
    result.append("商家指南:")
    for merchant, description in merchant_guide.items():
        result.append(f"{merchant}: {description}\n")
    return '\n'.join(result)

def read_flash_event_guide():
    flash_event_guide = data['TextContent']['Activity']['ActivityInfo']['🎉快閃活動指南']
    return f"🎉快閃活動指南:\n{flash_event_guide}"

# 提取所需的内容并返回一个包含所有内容的字符串


def extract_activity_info():
    activity_info = data['TextContent']['Activity']['ActivityInfo']
    result = []
    result.append("活動主辦方: " + str(activity_info['活動主辦方']))
    result.append("活動地點: " + str(activity_info['活動地點']))
    result.append("活動時間: " + str(activity_info['活動時間']))
    result.append("商家指南:")
    for merchant, description in activity_info['商家指南'].items():
        result.append(f"{merchant}: {description}")
    result.append("🎉快閃活動指南:")
    result.append(activity_info['🎉快閃活動指南'])
    return '\n'.join(result)

if __name__ == "__main__":
    # 调用函数以分别读取不同的内容
    organizer_str = read_organizer()
    location_str = read_location()
    time_str = read_time()
    merchant_guide_str = read_merchant_guide()
    flash_event_guide_str = read_flash_event_guide()
    activity_info = extract_activity_info(data)

    # 打印或使用返回的字符串
    print("活動主辦方:", organizer_str)
    print("活動地點:", location_str)
    print("活動時間:", time_str)
    print("商家指南:", merchant_guide_str)
    print("🎉快閃活動指南:", flash_event_guide_str)
    print("活動信息:", activity_info)


