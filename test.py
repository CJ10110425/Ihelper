from openai import OpenAI
import os
import dotenv

# 加载环境变量
dotenv.load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)


def create_chat_response():
    # 设置聊天消息
    gpt_assistant_prompt = "身為一個參加 2024 年陽明交大歡樂耶誕城的#I型人格#完美主義#高效率菁英的學生"  # 替换为您的提示内容
    # 替换为用户的提示内容
    gpt_user_prompt = "\n幫我根據以下推薦路線給出每一個推薦路線的內容介紹以及優缺點分析，遵照：路線一\n路線二、路線三，每一個路線分析簡短有力\n以下有三個推薦路線：\n入口 -> 糖餅屋 -> 卡哇伊小屋 -> 燭火時光 -> 飲品角--溫暖一杯 -> 小食街角 -> 木藝聖誕坊 -> 表演舞台\n入口 -> 卡哇伊小屋-> 糖餅屋- > 小食街角 -> 木藝聖誕坊-> 飲品角--溫暖一杯-> 表演舞台-> 話劇-> 燭火時光\n入口 -> 小食街角-> 卡哇伊小屋-> 燭火時光 -> 飲品角--溫暖一杯-> 小食街角> 表演舞台 -> 木藝聖誕坊-> 小食街角-> 糖餅屋\n每個景點的內容以下：\n🪵木藝聖誕坊: ➡️在這邊你可以用雕刻好的木頭DIY(黏貼及彩繪)屬於2023年的聖誕節裝飾小物\n🍭糖餅屋: ➡️這裡可以買到烤棉花糖跟薑餅人。這些食物都很應景呢! 買來跟聖誕樹一起拍照吧!\n🥐小食街角（旁邊有聖誕樹可以停留拍照）: ➡️這裡可以買到墨西哥捲餅、三明治等等的輕食，他們家的食物份量小，很適合逛街時嘴饞的你們!\n🪮卡哇伊小屋: ➡️這家店有很多CP值高又精美的頭飾，可以買來拍照!\n🍵飲品角--溫暖一杯: ➡️這家店賣許多熱飲，在飲控中的朋友們，他們也有提供熱水~\n🕯️燭火時光（旁邊有聖誕樹可以停留拍照）: ➡️這家是賣香氛蠟燭的店。不覺得買一小個蠟燭回家點燃，就很有過節的氣氛嗎?\n表演舞台與話劇遵照以下快閃活動時間：\n(詳細地點皆會標示在地圖上)\n➡️12/23（一）15:00-19:30 薑餅人製作工坊\n➡️16:00-17:00 音樂表演\n➡️16:00-18:00 話劇表演（睡美人）\n➡️19:00-19:30 聖誕老人來發送小點心\n➡️12/24（二）17:00-18:00 音樂表演\n➡️16:00-18:00 話劇表演（羅密歐與茱麗葉）\n➡️19:00-19:30 聖誕老人發送小點心\n➡️20:0户的提示内容"
    message = [
        {"role": "assistant", "content": gpt_assistant_prompt},
        {"role": "user", "content": gpt_user_prompt}
    ]

    # 设置调用参数
    temperature = 0.2
    frequency_penalty = 0.0

    # 调用 GPT-4 聊天模型
    response = client.chat.completions.create(model="gpt-4",
    messages=message,
    temperature=temperature,
    frequency_penalty=frequency_penalty)
    path = response.choices[0].message.content
    path = detect_and_extract_route("路線一", path)
    return path


def detect_and_extract_route(route_name, route_text):
    # 在文本中查找路线名称
    start_index = route_text.find(route_name)
    
    if start_index == -1:
        return "未找到指定路線"
    
    # 提取路线一以后的内容
    route_content = route_text[start_index + len(route_name):].strip()
    path = "路線一" + route_content
    return path

if __name__ == "__main__":
    gpt_assistant_prompt = "身為一個參加 2024 年陽明交大歡樂耶誕城的#I型人格#完美主義#高效率菁英的學生"  # 替换为您的提示内容
    # 替换为用户的提示内容
    gpt_user_prompt = "\n幫我根據以下推薦路線給出每一個推薦路線的內容介紹以及優缺點分析，遵照：路線一\n路線二、路線三，每一個路線分析簡短有力\n以下有三個推薦路線：\n入口 -> 糖餅屋 -> 卡哇伊小屋 -> 燭火時光 -> 飲品角--溫暖一杯 -> 小食街角 -> 木藝聖誕坊 -> 表演舞台\n入口 -> 卡哇伊小屋-> 糖餅屋- > 小食街角 -> 木藝聖誕坊-> 飲品角--溫暖一杯-> 表演舞台-> 話劇-> 燭火時光\n入口 -> 小食街角-> 卡哇伊小屋-> 燭火時光 -> 飲品角--溫暖一杯-> 小食街角> 表演舞台 -> 木藝聖誕坊-> 小食街角-> 糖餅屋\n每個景點的內容以下：\n🪵木藝聖誕坊: ➡️在這邊你可以用雕刻好的木頭DIY(黏貼及彩繪)屬於2023年的聖誕節裝飾小物\n🍭糖餅屋: ➡️這裡可以買到烤棉花糖跟薑餅人。這些食物都很應景呢! 買來跟聖誕樹一起拍照吧!\n🥐小食街角（旁邊有聖誕樹可以停留拍照）: ➡️這裡可以買到墨西哥捲餅、三明治等等的輕食，他們家的食物份量小，很適合逛街時嘴饞的你們!\n🪮卡哇伊小屋: ➡️這家店有很多CP值高又精美的頭飾，可以買來拍照!\n🍵飲品角--溫暖一杯: ➡️這家店賣許多熱飲，在飲控中的朋友們，他們也有提供熱水~\n🕯️燭火時光（旁邊有聖誕樹可以停留拍照）: ➡️這家是賣香氛蠟燭的店。不覺得買一小個蠟燭回家點燃，就很有過節的氣氛嗎?\n表演舞台與話劇遵照以下快閃活動時間：\n(詳細地點皆會標示在地圖上)\n➡️12/23（一）15:00-19:30 薑餅人製作工坊\n➡️16:00-17:00 音樂表演\n➡️16:00-18:00 話劇表演（睡美人）\n➡️19:00-19:30 聖誕老人來發送小點心\n➡️12/24（二）17:00-18:00 音樂表演\n➡️16:00-18:00 話劇表演（羅密歐與茱麗葉）\n➡️19:00-19:30 聖誕老人發送小點心\n➡️20:0户的提示内容"
    path = create_chat_response(gpt_assistant_prompt, gpt_user_prompt)
    print(path)
    print(detect_and_extract_route("路線一", path))
    