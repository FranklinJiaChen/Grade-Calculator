FILE_INPUT = "1.17.csv"
#header column for sheets info
COURSE = 0
NAME = 1
DUE_DATE = 2
STATUS = 4
GRADE = 5
WEIGHT = 6 #6 when before 4.12 else 5
WEIGHTED = 7 #5 when before 4.12 else 6 (not used)
#splitting name
TYPE = 0
NUMBER = 1
WANTED_GRADE = 90
EXTRA_DATA = True

class Data:
    def __init__(self, course: str, type: str, number: int, due_date: str, status: float, grade: float, weight: float) -> None:
        """
        Creates a data class.
        Data is the individual lines of the spreadsheet. A single piece of school work.
        PARAMETERS
        course: which course is this work from
        type: What kind of work is it such as project, quiz, midterm or final
        number: The number of the type of work for example 2 could indicate the 2nd midterm of the 2nd quiz
            if the number is -1, it is an unique type of work that has no 2nd, for example a final
        status: refers to what stage the work is at 
            -1 is for N/A
            0 is incomplete
            1 is complete
            1.5 is mark returned and needs to be reviewed
            2 is finished with material
        grade: the grade achieved on the work
            a value between 0-100 (with a few exceptions)
        weight: how much the work contributes the final grade
            a value between 0-1
        """
        self.course = course
        self.type = type
        self.number = number
        self.due_date = due_date
        self.status = status
        self.grade = grade
        self.weight = weight

    def __str__(self) -> str:
        """
        return a str representation of class work
        """
        if (self.number != -1):
            return f'{self.course}\'s {self.type} {self.number}'
        return f'{self.course}\'s {self.type}'

    
    def find_errors(self) -> None:
        """
        tries to find error in data/spreadsheet
        """
        if self.status != -1:
            if (self.status < 0 or self.status > 2):
                print(f'{self}: status error')
            if ((self.grade < 0 or self.grade > 100) and self.grade != -1):
                print(f'{self}: grade error')
            if (self.weight < 0 or self.weight > 1):
                print(f'{round(self, 2)}: weight error')


class Work:
    def __init__(self, course: str, type: str) -> None:
        """
        This creates a work Class
        Work is a collection of "Data" that have have the same "course" and "type". I.e. MATH 101 Midterms or CSC 115 quizzes.
        course: which course is this work from
        PARAMETERS
        type: What kind of work is it such as project, quiz, midterm or final
        work_list: a list with all the individual work/"data" in this work
        effect: a value given showing how much this work contributed to getting my grade.
            A positive number shows that this work boosted my overall grade in the class
            A negative number shows that this work dropped my overall in the class
            The bigger the magnitude shows the bigger the pull (boost/drop).
        grade: the (weighted) grade achieved on the work
            a value between 0-100 (with a few exceptions)
        max_grade: the max possible (weighted) grade that could have been achieved in this work
        """
        self.course = course
        self.type = type
        self.work_list = []
        self.effect = 0
        
    def set_effect(self, effect: float):
        """
        sets effect of Work on grade
        """
        self.effect = effect


    def work_append(self, data: Data):
        """
        appends data to this work's database
        """
        self.work_list.append(data)

    def calculate_grade(self) -> None:
        """
        calculate grade of this work type
        """
        self.grade = 0
        self.max_grade = 0
        for i in self.work_list:
            if i.status >= 1.5:
                self.grade += i.grade*i.weight
                self.max_grade += i.weight
    def __str__(self) -> str:
        """
        returns a str representation of Work
        """
        return f'{self.course}-{self.type}'


class WorkNode:
    def __init__(self, data: Work) -> None:
        """
        create a WorkNode with no next or prev
        """
        self.data = data
        self.next = None
        self.prev = None
    
    def __str__(self) -> str:
        """
        returns a str representation of WorkNode
        """
        return f'this node contains {self.data}'


class LinkedList:
    def __init__(self) -> None:
        """
        create an Linked List of work nodes
        """
        self.head = None
        self.size = 0
        self.tail = None

    def add(self, n: WorkNode) -> None:
        """
        adds a node to the linked list so that the effect is in order. Highest effect at top and lowest at bottom
        """
        if self.head == None:
            self.head = n
            self.tail = n
        elif self.head.data.effect < n.data.effect:
            self.head.prev = n
            n.next = self.head
            self.head = n
        elif self.size == 1:
            self.head.next = n
            n.prev = self.head
            self.tail = n
        else:
            cur = self.head
            while cur != None:
                if cur.data.effect < n.data.effect:
                    cur.prev.next = n
                    n.prev = cur.prev
                    n.next = cur
                    cur.prev = n
                    break
                cur = cur.next
            if cur == None:
                n.prev = self.tail
                self.tail.next = n
                self.tail = n
        self.size += 1
    def print_all(self) -> None:
        """
        prints out all the data of the work
        """
        cur = self.head
        while cur != None:
            if cur.data.effect >= 0:
                    print(f'    [+{round(cur.data.effect, 2)}]: {cur.data.type}\'s grade is {round(cur.data.grade/cur.data.max_grade, 2)}%')
            else:
                print(f'    [{round(cur.data.effect, 2)}]: {cur.data.type}\'s grade is {round(cur.data.grade/cur.data.max_grade, 2)}%')
            cur = cur.next

    
class Class:
    def __init__(self, name: str) -> None:
        """
        Class is the course. Contains the all components of "work"
        This creates a Class class
        PARAMETERS
        name: is the name of the course in uvic style i.e. MATH 211
        grade: the percentage grade that you currently have if you do nothing for rest of term. 
            a value from 0-100 (could be exceptions)
        max_grade: the max grade you could have achieved if all marked work was 100% for the term so far.
            a value from 0-1
        data: contains a list of all "data" class in course
        name_to_work: a dictionary from the name of a work type to the work object that belongs in the course
        """
        self.name = name
        self.grade = 0
        self.max_grade = 0
        self.data = []
        self.name_to_work = {}
    
    def update_grade(self, grade: float) -> None:
        """
        adds grade to your current grade
        """
        self.grade += grade


    def update_max_grade(self, weight: float) -> None:
        """
        adds the maximum possible achieved grade to your max grade
        """
        self.max_grade += weight


    def __str__(self) -> str:
        """
        same as get_grade
        """
        return f'{self.name}: current grade is at {round(self.grade/self.max_grade, 2)}%'

    def is_course_done(self) -> bool:
        """
        return if course is done
        """
        if round(1-self.max_grade, 2) == 0.00:
            return True
        return False

    def get_current_grade(self) -> float:
        """
        returns current grade
        """
        if self.max_grade == 0:
            return 0
        return round(self.grade/self.max_grade, 2)


    def get_needed_grade(self) -> float:
        """
        returns needed grade needed to get a 9/9 (or wanted grade)
        """
        # if not self.is_course_done():
        return round((WANTED_GRADE-0.5-(self.grade))/(1-self.max_grade), 2)


    def get_grade_if_did_nothing(self) -> float:
        """
        returns grade if you did nothing for the rest of term
        """
        return round((self.grade), 2)


    def get_grade_if_you_ace(self) -> float:
        """
        returns grade if you did aced the rest of term
        this is kinda a bad mindset. Probably shouldn't exist lol
        """
        return round((100-self.max_grade*100+self.grade), 2)
    

    def data_append(self, data: Data) -> None:
        """
        adds specific class work data to the course
        """
        self.data.append(data)

    def print_all_work(self) -> None:
        """
        print every single work done in class
        """
        for i in self.data:
            print(i)

    def print_work_needs_marks(self) -> None:
        """
        print every work done in class
        """
        for i in self.data:
            if i.status >= 1 and i.status < 1.5:
                print(i)
    
    def print_unmarked_work(self) -> None:
        """
        print every unmarked work done in class
        """
        for i in self.data:
            if i.status < 1.5 and i.status != -1:
                print(i)

    def print_reviewable_work(self) -> None:
        """
        print every work that should be reviewed
        """
        empty = True
        for i in self.data:
            if i.status >= 1.5 and i.status < 2:
                if empty:
                    print("should review:")
                    empty = False
                print(f'    {i}')
    
    def MVP(self) -> None:
        """
        find the work that had the highest effect on the grade
        """
        highest = None
        data = None
        for i in self.data:
            if i.status >= 1.5:
                effect = i.grade*i.weight-i.weight*self.get_current_grade()
                if highest == None or effect > highest:
                    highest = effect
                    data = i
        if highest != None:
            if EXTRA_DATA:
                print(f'    [+{round(highest, 2)}]: {data} is the MVP with a {round(data.grade, 2)}%')
            else:
                print(f'    {data} is the MVP with a {data.grade}%')
        else:
            print(f'    no contest')
    
    def biggest_L(self) -> None:
        """
        find the work that had the worst effect on the grade
        """
        lowest = None
        data = None
        for i in self.data:
            if i.status >= 1.5:
                effect = i.grade*i.weight-i.weight*self.get_current_grade()
                if lowest == None or effect < lowest:
                    lowest = effect
                    data = i
        if lowest != None:
            if EXTRA_DATA:
                print(f'    [{round(lowest, 2)}]: {data} is the biggest L with a {round(data.grade, 2)}%')
            else:
                print(f'    {data} is the biggest L with a {data.grade}%')
        else:
            print(f'    no contest')
        

    def make_sub_groups(self) -> None:
        """
        makes class instances for all of this course's work type
        """
        if self.name_to_work == {}:
            for i in self.data:
                if i.status != -1:
                    if i.type not in self.name_to_work:
                        self.name_to_work[i.type] = Work(self.name, i.type)
                    self.name_to_work[i.type].work_append(i)
                    

    def average_of_groups(self) -> None:
        """
        gets the average of all this course's work type
        """
        self.make_sub_groups()
        my_list = LinkedList()
        for k in self.name_to_work:
            self.name_to_work[k].calculate_grade()
            if self.name_to_work[k].max_grade != 0:
                work_grade = self.name_to_work[k].grade
                work_max_grade = self.name_to_work[k].max_grade
                self.name_to_work[k].set_effect(round(work_grade-work_max_grade*self.get_current_grade(), 2))
                my_list.add(WorkNode(self.name_to_work[k]))
        my_list.print_all()
                

    def find_errors(self) -> None:
        """
        tries to find error in spreadsheet
        """
        total = 0
        for i in self.data:
            if i.status != -1:
                total += i.weight
                i.find_errors()
        if round(total, 2) != 1:
            print(f'{self.name}: weight error: {round(total, 4)}')
    
            
name_to_class = {} #course name to the class class

file_handle = open(FILE_INPUT, "r")
file_handle.readline()
for line in file_handle:
    # print(line) #for debugging
    line = line.rstrip()
    line_data = line.split(',')
    split_name = line_data[NAME].rsplit(' ', 1)
    if len(split_name) == 1:
        split_name.append(-1)

    # try:
    data = Data(line_data[COURSE], split_name[TYPE], split_name[NUMBER], line_data[DUE_DATE],
    float(line_data[STATUS]), float(line_data[GRADE]), float(line_data[WEIGHT]))
    # except ValueError:
    #     print(ValueError)

    if line_data[COURSE] not in name_to_class:
        name_to_class[line_data[COURSE]] = Class(line_data[COURSE])
    if float(line_data[STATUS]) >= 1.5:
        name_to_class[line_data[COURSE]].update_grade(float(line_data[WEIGHT])*float(line_data[GRADE]))
        name_to_class[line_data[COURSE]].update_max_grade(float(line_data[WEIGHT]))
    name_to_class[line_data[COURSE]].data_append(data)
file_handle.close()


for i in name_to_class:
    #print(f'{name_to_class[i].name}: works that need marks:')
    if name_to_class[i].is_course_done():
        print(f'{name_to_class[i].name}: Final grade is {name_to_class[i].get_current_grade()}%')
        print("Highlights:")
        name_to_class[i].MVP()
        name_to_class[i].biggest_L()
        print("Info:")
        name_to_class[i].average_of_groups()
        print()
    else:
        print(f'{name_to_class[i].name}: Current grade is {name_to_class[i].get_current_grade()}%')

        if not name_to_class[i].is_course_done():
            print(f'{name_to_class[i].name}: To achieve a {WANTED_GRADE}%, maintain a {name_to_class[i].get_needed_grade()}% average')
        print(f'{name_to_class[i].name}: If you do nothing, you\'ll get {name_to_class[i].get_grade_if_did_nothing()}%')
        print(f'{name_to_class[i].name}: If you ace, you\'ll get {name_to_class[i].get_grade_if_you_ace()}%')

        # print(f'{name_to_class[i].print_reviewable_work()}')

    name_to_class[i].find_errors()
    name_to_class[i].print_unmarked_work()
    # name_to_class[i].print_work_needs_marks()
    # if name_to_class[i].is_course_done():
    
    print()