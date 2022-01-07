import sys
import urllib
import webbrowser
import os
import requests
import shutil

from urllib import request


class VAR:
    # Main Vars

    file = ""
    filetype = ""
    filename = "File"
    folder = "./downloads/"
    separator = "---"
    pyname = "DownMe.py"

    dirpaths = []

    # MESSAGESS
    commands = '''
            -----------------------------------------------------------------------------------
                                                COMMAND LIST
            -----------------------------------------------------------------------------------
            -h / -help -> Shows help
            -list -> Shows this command list
            -f  FILE -> Txt file that contains your urls
            -ft EXTENSION -> Sets the default extension for your downloaded files
            -n / -name FILENAME -> Sets a name for your downloaded files (Default Name = File)
            -o / -output FOLDER -> Sets an specific folder for your downloaded files
            --Log2 -> Used to load complex Logs. For more reference use --ref
            --Log3 -> Used to load complex Logs that include [FILENAME] and/or [FILETYPE] vars
            --ref -> Link to README in Github.\n
    '''

    help = '''
            \n        
            -----------------------------------------------------------------------------------
                                                    SYNTAX
            -----------------------------------------------------------------------------------
            
            DownMe.py -h / -help  || --ref || -f FILE | -ft EXTENSION || -n / -name FILENAME ||
            -o / -output FOLDER || --Log2 | --Log3
            
            
            [Example Command Line]
            
            python DownMe.py -f file.txt -ft .jpg -n "Long name" -o "specific folder name"
            
            python DownMe.py -f file.txt -ft .jpg -n "Long Name" --Log2
            
            
            -----------------------------------------------------------------------------------
                                                    NOTES
            ------------------------------------------------------------------------------------
            
            EXTENSION -> Write a dot followed by extension (.jpg, .exe, .rar, etc)

            UNIQUE ARGS -> -h / -help, --ref

            REQUIRED ARGS -> -f , -ft 

            OPTIONAL ARGS -> -n, -o, --Log2, --Log3\n\n''' + commands

    FileNotFoundError = '''
    \n
    /////////////////////////////////////////////////////////
    ///// Filename or path is wrong or does not exist ///////
    /////////////////////////////////////////////////////////

    '''

    downfinish = '''
    \n
    /////////////////////////////////////////////////////////
    ///////// All downloads finished successfully! //////////
    /////////////////////////////////////////////////////////

    '''

    nofileselected = '''
    \n
    ////////////////////////////////////////////////////////////////////////////
    ///////// No file selected. Please select a file. Write file path //////////
    ////////////////////////////////////////////////////////////////////////////

    '''

    nofiletypeselected = '''
    \n
    //////////////////////////////////////////////////////////////////////////////////////
    ///////// No file type selected. Please select a file type. Write file path //////////
    //////////////////////////////////////////////////////////////////////////////////////

    '''


class INBUILTFUNC:

    @staticmethod
    def delete_Log2_var():
        var = ["[FILENAME]", "[FILETYPE]"]

        for j in range(len(var)):
            if var[j] in VAR.dirpaths:
                index = VAR.dirpaths.index(var[j])+1
                var1 = VAR.dirpaths[index]
                VAR.dirpaths.remove(var1)
                VAR.dirpaths.remove(var[j])

    @staticmethod
    def check_if_Log2_var():
        for j in range(len(VAR.dirpaths)):
            if VAR.dirpaths[j] == "[FILETYPE]":
                VAR.filetype = str(VAR.dirpaths[j + 1])
                filetypevar = str(VAR.dirpaths[j + 1])

            if VAR.dirpaths[j] == "[FILENAME]":
                VAR.filename = str(VAR.dirpaths[j + 1])
                filenamevar = str(VAR.dirpaths[j + 1])

        if "[FILETYPE]" in VAR.dirpaths:
            VAR.dirpaths.remove("[FILETYPE]")
            VAR.dirpaths.remove(filetypevar)
        if "[FILENAME]" in VAR.dirpaths:
            VAR.dirpaths.remove("[FILENAME]")
            VAR.dirpaths.remove(filenamevar)

    @staticmethod
    def mkdir_main(mkdir):
        if not os.path.isdir(mkdir):
            os.mkdir(mkdir)

    @staticmethod
    def check_if_main_var(args):
        if "-f" not in args:
            while True:
                try:
                    print(VAR.nofileselected)
                    opt = str(input("////// -> "))
                    if opt:
                        VAR.file = opt
                        break
                except TypeError:
                    pass

        if "-ft" not in args and "--Log3" not in args:
            while True:
                try:
                    print(VAR.nofiletypeselected)
                    opt = str(input("////// -> "))
                    if opt:
                        VAR.filetype = opt
                        break
                except TypeError:
                    pass

    @staticmethod
    def read_sys_args(args):

        if args[0] == VAR.pyname and len(args) == 1:
            MAINFUNC.help()
        if args[0] == VAR.pyname and args[1] == "--ref":
            webbrowser.open("https://github.com/d1g1tus/DownMe")
            quit()
        if args[0] == VAR.pyname and args[1] == "-list":
            print(VAR.commands)
            quit()

        if args[0] == VAR.pyname:
            for i in range(len(args)):
                if args[i] == "-h" or args[i] == "-help":
                    if len(args) == 2:
                        MAINFUNC.help()

                if args[i] == "-f":
                    VAR.file = args[i+1]
                if args[i] == "-ft":
                    VAR.filetype = args[i+1]
                if args[i] == "-n" or args[i] == "-name":
                    VAR.filename = args[i+1]
                if args[i] == "-o" or args[i] == "-output":
                    VAR.folder = VAR.folder + args[i+1] + '/'

            INBUILTFUNC.check_if_main_var(args)
            if "--Log3" in args:
                if VAR.separator not in INBUILTFUNC.read_file(VAR.file):
                    print("\n ////// -> File log is not Log3. Process cannot proceed.\n")
                else:
                    MAINFUNC.start_download_full()

            if "--Log2" in args:
                if VAR.separator not in INBUILTFUNC.read_file(VAR.file):
                    print("\n ////// -> File log is not Log2. Process cannot proceed.\n")
                else:
                    MAINFUNC.start_download_full()
            else:
                try:
                    if VAR.separator in INBUILTFUNC.read_file(VAR.file):
                        print("\n ////// -> File log is Log2. Process cannot proceed. Add --Log2 to the script line\n")
                    else:
                        INBUILTFUNC.mkdir_main(VAR.folder)
                        MAINFUNC.start_downloand_urls()
                except TypeError:
                    pass

            quit()

    @staticmethod
    def read_file(file):
        try:
            with open(file, 'r') as read:
                lines = read.readlines()
                read.close()
            return lines
        except FileNotFoundError:
            print(VAR.FileNotFoundError)

    @staticmethod
    def mkdir(dirs):

        dirs = dirs.split(' - ')

        for element in dirs:
            if element != '':
                VAR.dirpaths.append(element.strip())

        INBUILTFUNC.check_if_Log2_var()

        for j in range(len(VAR.dirpaths)):

            if not os.path.isdir(VAR.folder + VAR.dirpaths[j]):
                os.mkdir(VAR.folder + VAR.dirpaths[j] + '/')

                VAR.folder = VAR.folder + VAR.dirpaths[j] + '/'
            else:
                VAR.folder = VAR.folder + VAR.dirpaths[j] + '/'

        return VAR.folder

    @staticmethod
    def get_urls(file, position):
        urls = []
        nextline = file.index(VAR.separator, position + 1)
        distance = file[position + 1:nextline]

        for j in range(len(distance)):
            try:
                list1 = []
                list1[:0] = distance[j]
                list2 = ['h', 't', 't', 'p']
                lol = -1
                asuma = 0
                for k in range(len(list2)):
                    lol = lol + 1
                    if list2[k] == list1[lol]:
                        asuma = asuma + 1
                    if asuma == 4:
                        urls.append(distance[j].strip())
            except IndexError:
                pass
            except ValueError:
                pass

        return urls

    @staticmethod
    def check_if_link(line):
        list1 = []
        list1[:0] = line
        list2 = ['h', 't', 't', 'p']
        lol = -1
        asuma = 0
        for k in range(len(list2)):
            lol = lol + 1
            try:
                if list2[k] == list1[lol]:
                    asuma = asuma + 1
                if asuma == 4:
                    return True
                else:
                    return False
            except IndexError:
                pass

    @staticmethod
    def parse_file_full(file):
        alist1 = []

        for i in range(len(file)):
            alist1.append(file[i].strip())

        for j in range(len(alist1)):
            if alist1[j] == VAR.separator:
                header = alist1[j-1]
                condition = INBUILTFUNC.check_if_link(header)
                if condition is False:
                    outputpath = INBUILTFUNC.mkdir(header)
                    urls = INBUILTFUNC.get_urls(file, alist1.index(alist1[j]))
                    MAINFUNC.download(outputpath, urls)


class MAINFUNC:

    @staticmethod
    def help():
        print(VAR.help)
        quit()

    @staticmethod
    def start_download_full():
        fileread = INBUILTFUNC.read_file(VAR.file)
        INBUILTFUNC.parse_file_full(fileread)

    @staticmethod
    def start_downloand_urls():
        urls = INBUILTFUNC.read_file(VAR.file)
        MAINFUNC.download(VAR.folder, urls)

    @staticmethod
    def download(path, urls):
        print("\n")
        for i in range(len(urls)):
            fullpath = path + VAR.filename + str(i) + VAR.filetype
            try:
                urllib.request.urlretrieve(urls[i], fullpath)
            except:
                r = requests.get(urls[i], stream=True)
                if r.status_code == 200:
                    with open(fullpath, 'wb') as f:
                        r.raw.decode_content = True
                        shutil.copyfileobj(r.raw, f)
            result = "[+] " + fullpath + " ///// -> [" + str(i + 1) + " / " + str(len(urls)) + "] - Downloaded"
            print(result)
        VAR.dirpaths.clear()
        VAR.folder = "./downloads/"
        print(VAR.downfinish)


if __name__ == "__main__":
    INBUILTFUNC.mkdir_main(VAR.folder)
    INBUILTFUNC.read_sys_args(sys.argv)


