import requests
import json
import json_struct as jv
# 22.12.28


class Client():
    def __init__(self, target_url) -> None:
        self.url = target_url

    def get_json(self):
        '''
        得到完整Json数据
        '''
        self.res = requests.get(self.url).text
        self.res_json = json.loads(self.res)
        self.order_by_course()
        # 进行格式化
        vis = jv.visualizer(self.res)
        vis.visualize(with_sample=True)
        print("Success! Got the Json-Object.")

    def show_json(self):
        '''
        展示完整json数据
        '''
        print(self.res)

    def find_by_name(self, name):
        '''
        通过学生名查找`
        '''
        self.name_res = requests.get(self.url + f'?name={name}').text
        print(self.name_res)

    def find_by_gender(self, gender):
        '''
        通过学生性别查找
        '''
        self.gender_res = requests.get(self.url + f'?gender={gender}').text
        print(self.gender_res)

    def find_by_key(self, key):
        '''
        通过学生属性关键字查找
        '''
        self.key_res = requests.get(self.url + f'?q={key}').text
        print(self.key_res)

    def order_by_course(self):
        '''
        按课程整理信息
        '''
        a = self.res_json
        self.all_course = set()
        for student in a:
            courses = student['course']
            for course in courses:
                self.all_course.add(course['title'])
        # print(all_course)
        self.by_course = list()

        for course in self.all_course:
            course_info = {}
            # print(course)
            course_info['title'] = course
            student_info = []
            for student in a:
                courses = student['course']
                for stu_course in courses:
                    if stu_course['title'] == course:

                        student_info.append(
                            {'student_name': student['name'], 'grades': stu_course['score']})
            course_info['student'] = student_info
            # print(course_info)
            self.by_course.append(course_info.copy())

    def course_display(self):
        print(self.by_course)

    def student_filter(self, course, condition, value):
        '''
        按课程成绩过滤学生
        '''
        temp = []
        if condition == 'g':

            for student in course['student']:
                if student['grades'] >= value:
                    temp.append(student)
            course['student'] = temp
        if condition == 'l':

            for student in course['student']:
                if student['grades'] <= value:
                    temp.append(student)
            course['student'] = temp
        if condition == 'e':
            for student in course['student']:
                if student['grades'] >= value[0] and student['grades'] <= value[1]:
                    temp.append(student)
            course['student'] = temp
        print(course)


if __name__ == "__main__":
    json_path = './1/json_transport/db.json'

    url = "http://localhost:3000/students"
    client = Client(url)
    print('Json 结构展示\n')
    client.get_json()

    while True:
        ch = input(
            "1.展示全部数据\t\t5.按课程整理\n2.通过学生名查找\t6.按成绩查询\n3.通过性别过滤\n4.通过关键字查找\n你的选择是：")
        if ch == '1':

            client.show_json()
        elif ch == '2':
            name = input('请输入名字：')
            client.find_by_name(name)
        elif ch == '3':
            gender = input('请输入性别：')
            client.find_by_gender(gender)
        elif ch == '4':
            key = input('请输入关键字：')
            client.find_by_key(key)
        elif ch == '5':
            # key = input('请输入关键字：')
            client.course_display()
        elif ch == '6':
            allcourse = list(client.all_course)
            for i, course in enumerate(allcourse):
                print(f'[{i}] {course}\n')
            u_title = int(input('请输入课程序号: '))
            if not (u_title >= 0 and u_title < len(allcourse)):
                print('输入课程不存在，请重新输入。')
                continue
            course = [
                i for i in client.by_course if i['title'] == allcourse[u_title]][0]
            print(course)
            u_score = input(r'请输入成绩要求,例如 >90 <60 70-80 这三种格式:')
            if('<' in u_score):
                u_condition = u_score[1:].strip()
                try:
                    u_condition = int(u_condition)

                    client.student_filter(course, 'l', u_condition)
                except:
                    print('ERROR')
                    continue
            elif('>' in u_score):
                u_condition = u_score[1:].strip()
                try:
                    u_condition = int(u_condition)
                    client.student_filter(course, 'g', u_condition)
                except:
                    print('ERROR')
                    continue
            elif('-' in u_score):
                u_condition = u_score.strip().split('-')
                if (len(u_condition) != 2):
                    print('ERROR')
                    continue
                try:
                    a, b = int(u_condition[0]), int(u_condition[1])
                    client.student_filter(course, 'e', [a, b])
                except:
                    print('ERROR')
                    continue
            else:
                print('输入不合法')
        else:
            print('请进行正确选择！')
            break
