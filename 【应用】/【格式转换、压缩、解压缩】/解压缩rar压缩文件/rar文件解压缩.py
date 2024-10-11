# pip install patool
import patoolib

# 要解压的RAR文件路径
rar_file_path = r"C:\Users\13480\gitee\quant\实用工具\【格式转换、解压缩】\解压缩rar压缩文件\gjzqqmt_ceshi.rar"
# 解压到的目标文件夹路径
extract_path = r"C:\Users\13480\gitee\quant\实用工具\【格式转换、解压缩】\解压缩rar压缩文件"
# 使用patool库解压缩RAR文件
patoolib.extract_archive(rar_file_path,outdir=extract_path)
# #需要安装辅助工具
# 安装WinRAR：
# 首先，你可以前往WinRAR官网（https://www.win-rar.com/download.html）下载WinRAR安装程序。
# 运行安装程序，按照提示完成WinRAR的安装过程。
# 将WinRAR路径添加到系统环境变量：
# 打开控制面板，并点击“系统与安全”。
# 选择“系统”，然后点击“高级系统设置”。
# 在弹出窗口中，点击“环境变量”按钮。
# 在“系统变量”下找到名为“Path”的变量，双击该变量。
# 在变量值的末尾添加WinRAR安装目录的路径（比如C:\Program Files\WinRAR），每个路径之间使用分号进行分隔。
# 确认保存更改并关闭所有窗口。
# 重新运行Python代码：
# 安装完WinRAR并将其路径添加到环境变量后，重新运行你的Python代码。
# patool库应该能够成功调用WinRAR来解压缩RAR文件了。
# 通过以上步骤，你应该能够成功安装支持RAR格式的解压缩工具并让patool库正常工作。如果有任何问题，请随时告诉我。