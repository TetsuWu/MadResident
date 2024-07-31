from flask import Flask, request, render_template

app = Flask(__name__)

def convert_char(char, position):
    # 第一位
    mapping_0 = {
        '0': 'MDA', '1': 'MDE', '2': 'MDI', '3': 'MDM', 
        '4': 'MDQ', '5': 'MDU', '6': 'MDY', '7': 'MDc', 
        'A': 'MEE', 'H': 'MEg', 'U': 'MFU'
    }
    # 第二位
    mapping_1 = {
        '0': 'w', '1': 'x', '2': 'y', '3': 'z', 
        '4': '0', '5': '1', '6': '2', '7': '3', 
        '8': '4', '9': '5'
    }
    # 第三位
    mapping_2 = {
        '0': 'MD', '1': 'MT', '2': 'Mj', '3': 'Mz', 
        '4': 'ND', '5': 'NT', '6': 'Nj', '7': 'Nz', 
        '8': 'OD', '9': 'OT'
    }
    # 第四位
    mapping_3 = {
        '0': 'A~D', '1': 'E~H', '2': 'I~L', '3': 'M~P', 
        '4': 'Q~T', '5': 'U~X', '6': 'Y,Z,a,b', 
        '7': 'c~f', '8': 'g~i', '9': 'k'
    }

    if position == 0:
        return mapping_0.get(char, char)
    elif position == 1:
        return mapping_1.get(char, char)
    elif position == 2:
        return mapping_2.get(char, char)
    elif position == 3:
        return mapping_3.get(char, char)
    else:
        return char

def convert_string(input_string):
    if len(input_string) != 4:
        raise ValueError("目標對象必須是4位英數字")
    return ''.join(convert_char(char, idx) for idx, char in enumerate(input_string))

def replace_url_content(url, converted_string):
    parts = url.split('=')
    if len(parts) >= 3:
        parts[-2] = converted_string
        return '='.join(parts)
    return url

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        target_string = request.form['target_string']
        url = request.form['url']
        try:
            converted_string = convert_string(target_string)
            modified_url = replace_url_content(url, converted_string)
        except ValueError as e:
            return render_template('index.html', target_string=target_string, url=url, error=str(e))
        return render_template('index.html', target_string=target_string, url=url, converted_string=converted_string, modified_url=modified_url)
    return render_template('index.html', target_string='', url='', converted_string='', modified_url='')

if __name__ == '__main__':
    app.run(debug=True)
