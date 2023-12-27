import json

# 指定 JSON 文件的路径
json_file_path = "data.json"


# 打开 JSON 文件并解析内容
with open(json_file_path, "r", encoding="utf-8") as json_file:
    data = json.load(json_file)


def get_question_and_answer(question_key):
    try:
        # 访问问题和答案
        question_data = data["TextContent"]["Activity"]["Quick questions and answers"][question_key]
        question = question_data["選項"]
        answer = question_data["回答"]["答案"]
        # correct_answer = question_data["回答"]["答對"]
        # incorrect_answers = question_data["回答"]["答錯"]
        return question, answer
    except KeyError:
        return None, None

def get_quiestion_reply(question_key):
    try:
        # 访问问题和答案
        question_data = data["TextContent"]["Activity"]["Quick questions and answers"][question_key]
        correct_answer = question_data["回答"]["答對"]
        incorrect_answers = question_data["回答"]["答錯"]
        return correct_answer, incorrect_answers
    except KeyError:
        return None, None

if __name__ == '__main__':

    question, answer = get_question_and_answer("請問本次聖誕市集的活動吉祥物是？")
    print(question)
    print(answer)
