# conda install zipfile
import zipfile
import os
# 指定要解压缩的 zip 文件路径和解压缩目标路径
basepath = r'C:\Users\13480\gitee\quant\实用工具\【格式转换、解压缩】\解压缩zip压缩文件\2024-01-03.zip'
filepath = r'C:\Users\13480\gitee\quant\实用工具\【格式转换、解压缩】\解压缩zip压缩文件\demo'
# 创建目标文件夹
if not os.path.exists(filepath):
    os.makedirs(filepath)
# 打开 zip 文件
with zipfile.ZipFile(basepath, 'r') as zip_ref:
    # 解压缩所有文件到目标文件夹
    zip_ref.extractall(filepath)
print("Zip 文件解压缩完成！")
