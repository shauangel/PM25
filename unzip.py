import zipfile
import os


def zipper(zipname):
    print(zipname)
    if zipname.endswith('.zip'):
        zip = zipfile.ZipFile(zipname)
        zip.extractall("/Users/shauangel/PycharmProjects/PM25/data/")
        zip.close()


def unzip():
    path = "data/"
    years = os.listdir(path)
    for y_dir in years:
        url = path+y_dir
        zipper(url)
        if os.path.isdir(url.removesuffix('.zip')):
            months = os.listdir(url.removesuffix('.zip'))
            for m_dir in months:
                m_url = url.removesuffix('.zip') + '/' + m_dir
                zipper(m_url)
                # m_url = path + m_dir.removesuffix('.zip')
                if os.path.isdir(m_url.removesuffix('.zip')):
                    days = os.listdir(m_url.removesuffix('.zip'))
                    for d_dir in days:
                        zipper(m_url.removesuffix('.zip') + '/' + d_dir)


if __name__ == "__main__":
    unzip()