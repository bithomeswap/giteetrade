import gzip
import shutil
def zip_to_gz(zip_file_path, gz_file_path):
    with open(zip_file_path, 'rb') as zip_file:
        with gzip.open(gz_file_path, 'wb') as gz_file:
            shutil.copyfileobj(zip_file, gz_file)
# 使用示例
zip_file_path = r'C:\Users\13480\gitee\trade\高考志愿填报系统\PYQT界面\dist\gaokao.zip'  # ZIP文件路径
gz_file_path = r'C:\Users\13480\gitee\trade\高考志愿填报系统\PYQT界面\dist\gaokao.gz'    # 输出的GZ文件路径
zip_to_gz(zip_file_path, gz_file_path)