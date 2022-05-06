# Simple directory organizer

Simple python script developed to auto organize the downloads folder using a crontab

fully native, dont require any package

## Running

    Arguments:
       first argument   -> path to organize :: ["/mnt/c/downloads"]
       second argument  -> organize folders :: [-y or -n]
      
    Command: 
      python app.py /DESIRED/PATH/HERE
    
    Examples:
      python app.py /c/Users/Name/Downloads -y
      python app.py /c/Users/Name/Downloads -n
      
## References
https://docs.python.org/3/library/pathlib.html

https://docs.python.org/3/library/os.html

https://docs.python.org/3/library/shutil.html
