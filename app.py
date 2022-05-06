from ast import arg
from operator import truediv
import os, pathlib, shutil, sys

class HandleDirectory:
    def __init__(self, spath, ignore_dir=True):
        '''Auto organize files by type
        
            Arguments:
        
            spath       -> folder path to organize :: ("/mnt/c/downloads")
        
            ignore_dir  -> dont organize folders :: (True or False)
        '''
        self.dpath = spath
        self.ignore_dir = ignore_dir
        self.files_schema = {}
        self.dirs_schema = {}

        self.success_moved_count = 0
        self.error_moved_count = 0

    # extract all suffix for files, including dir and files without type
    def suffix (self, _path):
        """
        The final component's last suffix, including directory and unknown file type.
        This includes the leading period. For example: '.txt'
        """
        _pathobject = pathlib.Path(_path)
        return ((_pathobject.suffix or ".unknown") 
                if not _pathobject.is_dir() else 
                (".dir"))
    # return dictionary with grouped files per type {type : [{filename, filename2, filename3}]}
    def __group_files (self, _files):
        for file in _files:
            _filetype = file.get("filetype")
            _filename = file.get("filename")
            
            if self.ignore_dir and _filetype == ".dir":
                pass

            _chunk = self.files_schema.get(_filetype, [])
            _chunk.append(_filename)
            
            self.files_schema[_filetype] = _chunk

    # handy function to join directory
    def __dir_join (self, d:str) -> str:
        return f"{self.dpath}/{d}"

    # make folders and store in global variable
    def __make_dirs(self):
        schema_keys = set(self.files_schema.keys())

        for sk in schema_keys:
            _pathdir = self.__dir_join(sk[1:])

            try: 
                if not os.path.isdir(_pathdir):
                    os.mkdir(_pathdir)
            except FileExistsError: pass

            self.dirs_schema[sk] = _pathdir

    # handle files from origin to target
    def __move_files(self):
        schema_keys = set(self.files_schema.keys())

        for _k in schema_keys:
            _dir = self.dirs_schema.get(_k)
            _files = self.files_schema.get(_k)

            try:
                for _file in _files:
                    shutil.move(self.__dir_join(_file),f"{_dir}/{_file}")
                    self.success_moved_count += 1
            except:
                self.error_moved_count += 1
        
    # process everything
    def process(self):
        _files = os.listdir(self.dpath)
        _files = [self.__dir_join(f) for f in _files]

        files_obj = [{
            "filename" : pathlib.Path(_f).name,
            "filetype" : self.suffix(_f)
        } for _f in _files]

        self.__group_files(files_obj)
        self.__make_dirs()
        self.__move_files()

        print(f"Finished!!\nSuccess: {self.success_moved_count} Error: {self.error_moved_count}")


# execute script only if is being executed explicitly
if __name__ == "__main__":
    # get args from terminal input
    args = dict(enumerate(sys.argv[1:], 0))
    
    # return help arguments
    if args.get(0) == "help":
        print("Usage: python app.py /mnt/c/FolderName -y")
        sys.exit()

    # settings
    desired_path = args.get(0, False)
    include_dirs = True if args.get(1, "-y") == "-y" else False

    # run script
    if desired_path:
        HandleDirectory(
            desired_path, 
            include_dirs
        ).process()

        print(f"Running on [{desired_path}]")