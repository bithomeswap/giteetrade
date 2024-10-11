import zipfile
import os
def zip_ya(startdir,file_news):
    z = zipfile.ZipFile(file_news,'w',zipfile.ZIP_DEFLATED) #参数一：文件夹名
    for dirpath, dirnames, filenames in os.walk(startdir):
        fpath = dirpath.replace(startdir,'') #这一句很重要，不replace的话，就从根目录开始复制
        fpath = fpath and fpath + os.sep or ''#这句话理解我也点郁闷，实现当前文件夹以及包含的所有文件的压缩
        for filename in filenames:
            z.write(os.path.join(dirpath,filename),fpath+filename)
            print ('压缩成功')
    z.close()

if __name__=="__main__":
    ##文件夹内所有文件压缩
    # startdir = r"C:\Users\13480\Desktop\quant\【本地选股（A股）】SDK\QMTSDK选股"  #要压缩的文件夹路径
    # # startdir = "/root/test/----SDK-huaxin/同花顺【实时行情及基本面数据】SDK"
    # file_news = startdir +'.zip' # 压缩后文件夹的名字夹路径
    # zip_ya(startdir,file_news)
    
    ##单文件压缩
    startdir = r"C:\Users\13480\Desktop\quant\【格式转换、压缩、解压缩】"
    # 要转换的MSI文件路径
    msi_file = 'Cloudflare_WARP_Release-x64.msi'
    # 指定生成的ZIP文件路径
    zip_file = 'Cloudflare_WARP_Release-x64.zip'
    z = zipfile.ZipFile(startdir+"/"+zip_file,'w',zipfile.ZIP_DEFLATED) #参数一：文件夹名
    z.write(startdir+"/"+msi_file, os.path.basename(msi_file))
    # z.write(os.path.join(startdir+"/"+zip_file,startdir),startdir+zip_file)
    z.close()
    print ('压缩成功')
    