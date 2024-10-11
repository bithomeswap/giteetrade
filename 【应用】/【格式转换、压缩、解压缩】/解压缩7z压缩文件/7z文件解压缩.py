import py7zr
basepath=r"C:\Users\13480\gitee\quant\实用工具\【格式转换、解压缩】"
fliename="Clash.for.Windows-0.20.39-win.7z"
with py7zr.SevenZipFile(basepath+"/"+fliename, mode='r') as z:
    # 打印压缩包中的文件列表
    print(z.getnames())
    # 解压所有文件到指定目录
    z.extractall(path=basepath)