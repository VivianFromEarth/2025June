# 2025June
# 9th June 【Class 1 - python基础】
## 1. 环境准备
### 检查Python版本
python --version
### 创建并激活虚拟环境
python -m venv myenv
### Windows
myenv\Scripts\activate
### Linux/Mac
source myenv/bin/activate
### 安装第三方库
pip install requests


## 2. 变量、变量类型、作用域

- 基本变量类型：`int`、`float`、`str`、`bool`、`list`、`tuple`、`dict`、`set`。
- 作用域：全局变量、局部变量，`global` 和 `nonlocal` 关键字。
- 类型转换：如 `int()`、`str()`。

**代码示例：**

```python
# 变量类型
name = "Alice"       # str
age = 20             # int
grades = [90, 85, 88]  # list
info = {"name": "Alice", "age": 20}  # dict

# 类型转换
age_str = str(age)
number = int("123")

# 作用域
x = 10  # 全局变量
def my_function():
    y = 5  # 局部变量
    global x
    x += 1
    print(f"Inside function: x={x}, y={y}")

my_function()
print(f"Outside function: x={x}")

## 3. 运算符及表达式

- 算术运算符：`+`, , , `/`, `//`, `%`, `*`。
- 比较运算符：`==`, `!=`, `>`, `<`, `>=`, `<=`。
- 逻辑运算符：`and`, `or`, `not`。
- 位运算符：`&`, `|`, `^`, `<<`, `>>`。

**代码示例：**

```python
# 算术运算
a = 10
b = 3
print(a + b)  # 13
print(a // b)  # 3（整除）
print(a ** b)  # 1000（幂）

# 逻辑运算
x = True
y = False
print(x and y)  # False
print(x or y)   # True

# 比较运算
print(a > b)  # True
   
