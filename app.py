from flask import Flask, request, jsonify, render_template
app = Flask(__name__)

# 数字リスト
numbers = []
# 四則演算リスト
operations = []

# 四則演算の関数
def add(x, y):
    return x + y

def subtract(x, y):
    return x - y

def multiply(x, y):
    return x * y

def divide(x, y):
    if y == 0:
        raise ZeroDivisionError("0で割ることはできません。")  # 割れると世界が壊れる
    return x / y

# データ処理の関数
def process_input(input_value):
    global numbers, operations

    if input_value.isdigit():
        # 入力が数字の場合、リストに追加
        numbers.append(int(input_value))
    elif input_value in ["+", "-", "*", "/"]:
        # 入力が四則演算記号の場合、対応する関数をリストに追加
        if input_value == "+":
            operations.append(add)
        elif input_value == "-":
            operations.append(subtract)
        elif input_value == "*":
            operations.append(multiply)
        elif input_value == "/":
            operations.append(divide)
    else:
        # 無効な入力
        raise ValueError("無効な入力です。数字または +, -, *, / を使用してください。")

# 計算結果を計算する関数
def calculate_result():
    global numbers, operations

    # 不正結果の場合
    if len(numbers) - 1 != len(operations):
        raise ValueError("演算が不正です。正しい形式で入力してください。")

    # 初期値
    result = numbers[0]

    # 四則演算を順番に適用
    for i, operation in enumerate(operations):
        result = operation(result, numbers[i + 1])

    return result

# ルートエンドポイントでHTMLを提供
@app.route('/')
def index():
    return render_template('calculator.html')

# /calculateエンドポイントで計算を処理
@app.route('/calculate', methods=['POST'])
def calculate():
    global numbers, operations
    data = request.get_json()
    expression = data.get('expression', '')

    # 入力をリセット
    numbers = []
    operations = []

    # 式を解析して処理
    current_num = ''
    try:
        for char in expression:
            if char.isdigit():
                current_num += char
            elif char in ["+", "-", "*", "/"]:
                if current_num == '':
                    raise ValueError("不正な式です。")
                process_input(current_num)
                process_input(char)
                current_num = ''
            else:
                raise ValueError("無効な文字が含まれています。")
        if current_num != '':
            process_input(current_num)

        # 計算を実行
        result = calculate_result()
    except ZeroDivisionError as e:
        return jsonify({"result": str(e)}), 400
    except ValueError as e:
        return jsonify({"result": str(e)}), 400

    return jsonify({"result": result})

if __name__ == "__main__":
    app.run(debug=True)
