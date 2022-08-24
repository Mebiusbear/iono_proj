from ionox import download_codg,unzip_Z
import os

def download_data(year,begin,end):
    download_codg(year=year,begin=begin,end=end)
    data_dir = "./data"
    filenames = [os.path.join(data_dir,"CODG%03d0.22I.Z"%num) for num in range(begin,end+1)]

    for filename in filenames:
        if os.path.exists(filename):
            unzip_Z([filename])
            if os.remove(filename):
                print (filename,"remove!")

if __name__ == "__main__":
    year = 2022
    begin = 10
    end = 11
    download_data(year=year,begin=begin,end=end)
