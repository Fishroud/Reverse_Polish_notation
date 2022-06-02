#算术表达式的逆波兰表示与计算
from turtle import position


operatorLevel = {
    '#': -1,
    '+': 0,
    '-': 0,
    '*': 1,
    '/': 1,
    '(': 10,
    ')': 10
}

#判断输入是否是数字
def isNumber(s):
    try:
        int(s)
        return True
    except ValueError:
        pass
    return False

#判断输入是否是操作符
def isOperator(s):
    if s in operatorLevel:
        return True
    return False

#判断输入是否合法
def isValid(s):
    return isOperator(s) or isNumber(s)

#定义栈
class Stack:
    def __init__(self):
        self.items=[]

    def push(self,item):
        self.items.append(item)

    def pop(self):
        return self.items.pop()

    def peek(self):
        return self.items[-1]

    #判断栈是否为空
    def is_empty(self):
        return self.items==[]

    def size(self):
        return len(self.items)


#计算表达式类
class CalExpression:
    #定义操作符优先级字典
    def __init__(self,expression):
        self.expression = expression
        self.bracketsError = False
        self.grammarError = False
        self.list = self.rnp()
        self.result = self.calReversePolishList()

    def getExpression(self):
        return self.expression

    def getList(self):
        return str(self.list)

    def getResult(self):
        return str(self.result)

    def rnp(self):
        #定义两个栈
        expression = self.expression
        #临时运算符栈
        operatorStack = Stack()
        operatorStack.push('#')
        #逆波兰表达式栈
        rnpStack = Stack()
        #从左到右遍历表达式
        length = len(expression)
        #括号数量
        brackets = 0
        #调度场算法
        i = 0
        while(i < length):
            j = i
            #如果是数字，取出完整的操作数并直接入栈
            while(j < length and isNumber(expression[j])):
                j += 1
            if i != j:
                rnpStack.push(expression[i:j])
                i = j
            #如果是操作符
            try:
                expression[i]
            except IndexError:
                break
            #判断输入符号是否合法
            if(not isValid(expression[j])):
                self.grammarError = True
                error_symbol = expression[j]
                position = self.expression.find(error_symbol)
                result = 'grammar error！error_symbol:{}，position:{}'.format(error_symbol,position + 1)
                self.grammarError = True
                return result
            if (isOperator(expression[i]) and not operatorStack.is_empty() and expression[i] != '(' and expression[i] != ')'):
                #则将该运算符与rnpStack栈栈顶元素比较
                while(operatorLevel[expression[i]] <= operatorLevel[operatorStack.peek()] and operatorStack.peek() != '('):
                    rnpStack.push(operatorStack.pop())
                #如果该运算符优先级高于operator栈栈顶运算符优先级，则将该运算符进operator栈
                operatorStack.push(expression[i])
            #如果是左括号，则直接入栈
            if(expression[i] == '('):
                brackets += 1
                operatorStack.push(expression[i])
            #如果是右括号，则将距离operator栈栈顶最近的(之间的运算符，逐个出栈，依次送入rnp栈，此时抛弃(
            if(expression[i] == ')'):
                brackets -= 1
                while(operatorStack.peek() != '('):
                    rnpStack.push(operatorStack.pop())
                operatorStack.pop()
            i += 1
        #判断左右括号是否匹配
        if(brackets != 0):
            self.bracketsError = True
            return 'brackets error！'
        #如果operator栈不为空，则将operator栈中剩余的运算符逐个出栈，送入rnp栈
        if(not operatorStack.is_empty()):
            while(operatorStack.peek() != '#'):
                rnpStack.push(operatorStack.pop())
        return rnpStack.items

    #计算逆波兰表达式数组
    def calReversePolishList(self):
        list = self.list
        #如果有语法和括号错误，则直接返回
        if(self.grammarError or self.bracketsError):
            return self.list
        calStack = Stack()
        for list_this in list:
            #如果是数字，则直接入栈
            if(isNumber(list_this)):
                calStack.push(list_this)
            #如果是操作符，则将两个栈顶元素出栈，计算结果入栈
            else:
                num2 = int(calStack.pop())
                num1 = int(calStack.pop())
                if(list_this == '+'):
                    calStack.push(num1 + num2)
                elif(list_this == '-'):
                    calStack.push(num1 - num2)
                elif(list_this == '*'):
                    calStack.push(num1 * num2)
                elif(list_this == '/'):
                    calStack.push(num1 / num2)
            #判断是否计算完毕
        if(calStack.size() != 1):
            error_num = calStack.pop()
            #在字符串中查找error_num的位置
            position = self.expression.find(str(error_num))
            return 'math error！'
        return calStack.pop()



userinput = input('请输入表达式：')
expression = CalExpression(userinput)
output = '逆波兰表达式为：{}\n计算结果为：{}'.format(expression.getList(),expression.getResult())
print(output)