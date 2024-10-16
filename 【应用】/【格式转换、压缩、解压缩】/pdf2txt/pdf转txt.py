# pip3 install "modelscope==1.7.2rc0" -f
# pip install pdfplumber
import glob
import pdfplumber
import re
import os


def check_lines(page, top, buttom):
    lines = page.extract_words()[::]
    text = ''
    last_top = 0
    last_check = 0
    for each_line in lines:
        if top == '' and buttom == '':
            if abs(last_top - each_line['top']) <= 2:
                text = text + each_line['text']
            elif last_check > 0 and not re.search('(?:。|；|\d|报告全文)$', text):
                text = text + each_line['text']
            else:
                text = text + '\n' + each_line['text']
        elif top == '':
            if each_line['top'] > buttom:
                if abs(last_top - each_line['top']) <= 2:
                    text = text + each_line['text']
                elif last_check > 0 and not re.search('(?:。|；|\d|报告全文)$', text):
                    text = text + each_line['text']
                else:
                    text = text + '\n' + each_line['text']
        else:
            if each_line['top'] < top and each_line['top'] > buttom:
                if abs(last_top - each_line['top']) <= 2:
                    text = text + each_line['text']
                elif last_check > 0 and not re.search('(?:。|；|\d|报告全文)$', text):
                    text = text + each_line['text']
                else:
                    text = text + '\n' + each_line['text']
        last_top = each_line['top']
        last_check = each_line['x1'] - page.width * 0.85

    return text


def change_pdf_to_txt(name):
    pdf = pdfplumber.open(name)

    all_text = {}
    allrow = 0
    for i in range(len(pdf.pages)):
        page = pdf.pages[i]
        buttom = 0
        tables = page.find_tables()
        if len(tables) >= 1:
            count = len(tables)
            for table in tables:
                if table.bbox[3] < buttom:
                    pass
                else:
                    count = count - 1

                    top = table.bbox[1]
                    text = check_lines(page, top, buttom)
                    text_list = text.split('\n')
                    for _t in range(len(text_list)):
                        all_text[allrow] = {}
                        all_text[allrow]['page'] = page
                        all_text[allrow]['allrow'] = allrow
                        all_text[allrow]['type'] = 'text'
                        all_text[allrow]['inside'] = text_list[_t]
                        allrow = allrow + 1

                    buttom = table.bbox[3]
                    new_table = table.extract()
                    r_count = 0

                    for r in range(len(new_table)):
                        row = new_table[r]
                        if row[0] == None:
                            r_count = r_count + 1
                            for c in range(len(row)):
                                if row[c] != None and row[c] != '' and row[c] != ' ':
                                    if new_table[r - r_count][c] == None:
                                        new_table[r - r_count][c] = row[c]
                                    else:
                                        new_table[r - r_count][c] = new_table[r -
                                                                              r_count][c] + row[c]
                                    new_table[r][c] = None
                        else:
                            r_count = 0
                    end_table = []
                    for row in new_table:
                        if row[0] != None:
                            cell_list = []
                            for cell in row:
                                if cell != None:
                                    cell = cell.replace('\n', '')
                                else:
                                    cell = ''
                                cell_list.append(cell)
                            end_table.append(cell_list)
                    for row in end_table:
                        all_text[allrow] = {}
                        all_text[allrow]['page'] = page
                        all_text[allrow]['allrow'] = allrow
                        all_text[allrow]['type'] = 'excel'
                        all_text[allrow]['inside'] = str(row)
                        allrow = allrow + 1

                    if count == 0:
                        text = check_lines(page, '', buttom)
                        text_list = text.split('\n')
                        for _t in range(len(text_list)):
                            all_text[allrow] = {}
                            all_text[allrow]['page'] = page
                            all_text[allrow]['allrow'] = allrow
                            all_text[allrow]['type'] = 'text'
                            all_text[allrow]['inside'] = text_list[_t]
                            allrow = allrow + 1

        else:
            text = check_lines(page, '', '')
            text_list = text.split('\n')
            for _t in range(len(text_list)):
                all_text[allrow] = {}
                all_text[allrow]['page'] = page
                all_text[allrow]['allrow'] = allrow
                all_text[allrow]['type'] = 'text'
                all_text[allrow]['inside'] = text_list[_t]
                allrow = allrow + 1

    save_path_1 = f'{folder_path}\\' + \
        name.split('\\')[-1].replace('.pdf', '.txt')
    save_path_2 = f'{folder_path}\\' + \
        name.split('\\')[-1].replace('.pdf', '_txt.txt')
    for key in all_text.keys():
        with open(save_path_1, 'a+', encoding='utf-8') as file:
            file.write(str(all_text[key]) + '\n')
        with open(save_path_2, 'a+', encoding='utf-8') as file:
            file.write(str(all_text[key]['inside']) + '\n')


folder_path = '/home/wth000/gitee/quant/【格式转换、压缩、解压缩】/微盘股'
# folder_path = r'C:\Users\13480\gitee\trade\高考志愿填报系统\河北省2024高考一分一档和投档线'
# 获取文件夹内所有文件名称
file_names = glob.glob(folder_path + '/*')
file_names = sorted(file_names, reverse=True)
print(file_names)
# 打印文件名称
name_list = []
for file_name in file_names:
    print(file_name)
    try:
        name_list.append(file_name)
        allname = file_name.split('\\')[-1]
        date = allname.split('__')[0]
        name = allname.split('__')[1]
        year = allname.split('__')[4]
        change_pdf_to_txt(file_name)
    except Exception as e:
        print(f"发生bug: {e}")
