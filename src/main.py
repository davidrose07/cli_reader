#!/usr/bin/env python3

from controller import *
import argparse


def main() -> None:
    '''
    Main Function to start the application. uses parsed arguements to handle bash script or run directly from python with command line arguements

    :param: file_path - file to convert
    :param: browse -    option to use file explorer to find a file    
    '''
    parser = argparse.ArgumentParser(description="Read files from the command line with a browse option.")
    parser.add_argument("file", nargs='?', default=None, help="The path to the file to be processed.")
    parser.add_argument("-b", "--b", action="store_true", help="Browse for a file.")

    args = parser.parse_args()

    if not args.file and not args.b:
        print('Program requires a file name or browse option\ncli-reader -f <filename> or -b <browse>\n-help or --help to display options')
    else:
        controller = Controller(args.file, browse=args.b)
        

if __name__ == "__main__":
    main()


    

    












