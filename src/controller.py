#!/usr/bin/env python3

import tkinter as tk
from tkinter import filedialog
from cli_manager import CLIManager
import sys,subprocess, os
from colorama import init, Fore, Style
import pandas as pd
from tabulate import tabulate
import textwrap
from db import DB

init(autoreset=True)


class Controller():
    '''
    Main Application : Controller Class    
    '''    
    def __init__(self, file=None, browse=False) -> None:
        '''
        Init Function: setup the ui and handle options
        :param: file - the file to convert
        :param: show_ui - options to display the user interface or use command line
        :param: browse - option to use file explorer to find a file
        '''
        self.file = file
        self.data = None
        self.column_names = None
        df = None

        self.table_color = Fore.BLUE
        self.column_color = Fore.GREEN
        self.type_color = Fore.YELLOW
        self.error_color = Fore.RED

        if browse:
            self.file = self.open_file_dialog()

        if self.file != None:  
            self.file_type = self.determine_file_type()
        else:
            print("Must pick a file")
            sys.exit(0)

        if self.file_type == 'CSV file':
            df = self.parse_csv()
        elif self.file_type == 'XML file':
            df = self.parse_xml()
        elif self.file_type == 'Excel file':
            df = self.parse_excel()
        elif self.file_type == 'JSON file':
            df = self.parse_json()
        elif self.file_type == 'SQL file':
            db_type = self.determine_db_type(self.file)
            db = DB()
            if db_type == 'SQLite':
                df = db.parse_sqlite3(self.file)
            elif db_type == 'MySQL':
                df = db.parse_mysql(self.file)
            elif db_type == 'PostgreSQL':
                print("PostGreSql")
                # Replace with actual credentials
                df = db.parse_postgresql(host='localhost', user='postgres', password='password', database='dbname')
            else:
                print(f"Unknown database type: {self.file}")
                sys.exit(1)
        else:
            self.show_file()

        formatted_df = FormattedDataFrame(df)
        result = format(formatted_df)
        if result:
            with subprocess.Popen(['less', '-R'], stdin=subprocess.PIPE) as less_proc:
                    less_proc.communicate(result.encode('utf-8'))
        else:
            print("None type")

    def determine_db_type(self,file_path):
        sqlite_keywords = ["AUTOINCREMENT", "WITHOUT ROWID", "PRAGMA", "sqlite_sequence"]
        mysql_keywords = ["AUTO_INCREMENT", "ENGINE=", "CHARSET=", "UNSIGNED"]
        postgres_keywords = ["SERIAL", "BIGSERIAL", "SMALLSERIAL", "VARCHAR", "BOOLEAN"]

        try:
            with open(file_path, 'r') as file:
                sql_content = file.read().upper()
            
            if any(keyword in sql_content for keyword in sqlite_keywords):
                return 'SQLite'
            elif any(keyword in sql_content for keyword in mysql_keywords):
                return 'MySQL'
            elif any(keyword in sql_content for keyword in postgres_keywords):
                return 'PostgreSQL'
            else:
                return 'SQLite'
        except Exception as e:
            print(f"An error occurred while checking the SQL file: {e}")
            return 'Unknown'
        
    

    def parse_excel(self):
        try:
            df = pd.read_excel(self.file)
            return df
        except Exception as e:
            print(f"An error occurred while parsing Excel file: {e}")
            return None
        
    def parse_xml(self):
        try:
            df = pd.read_xml(self.file)
            return df
        except Exception as e:
            print(f"An error occurred while parsing XML file: {e}")
            return None
    
    def parse_csv(self):
        try:
            df = pd.read_csv(self.file)
            return df
        except Exception as e:
            print(f"An error occurred while parsing CSV file: {e}")
    

    def parse_json(self):
        try:
            df = pd.read_json(self.file)
            if any(df.applymap(lambda x: isinstance(x, dict)).any()):
                df = pd.json_normalize(df.to_dict(orient='records'))
            return df
        except Exception as e:
            print(f"An error occurred while parsing JSON file: {e}")
            return None

    def open_file_dialog(self):
        root = tk.Tk()
        root.withdraw()  # Hide the root window
        file = filedialog.askopenfilename(title="Select a file")
        return file
        
    
    def colored_text(self, text, color):
        return f"{color}{text}{Style.RESET_ALL}"
    
    def determine_file_type(self) -> str:
        '''
        Function: determine the file type to convert by splitting the extension and iterating through a dictionary
        :return: str
        '''
        _, file_extension = os.path.splitext(self.file)
        file_types = {
            '.csv': 'CSV file',
            '.json': 'JSON file',
            '.xml': 'XML file',
            '.xlsx': 'Excel file',
            '.sql': 'SQL file',
        }
        return file_types.get(file_extension.lower(), 'Unknown file type')
        

    def show_file(self):
        try:
            command = f'batcat {self.file}'
            exit_code = os.system(command)
            if exit_code != 0:
                print(f"An error occurred: Command exited with code {exit_code}")
            
        except Exception as e:
            print(self.colored_text(f'Exception opening file {self.file}:', self.type_color))
            print(self.colored_text(e, self.error_color))

        
        sys.exit(0)

class FormattedDataFrame:
    def __init__(self, df):
        self.df = df

    def __format__(self, format_spec):
        # Wrap the data
        wrapped_data = self.df.applymap(lambda x: '\n'.join(textwrap.wrap(str(x), width=100)))
        
        # Format the header
        header = Fore.BLUE + Style.BRIGHT + ' '.join(wrapped_data.columns) + Style.RESET_ALL
        
        # Format the table
        table = tabulate(wrapped_data, headers='keys', tablefmt='plain', showindex=False)
        table = table.split('\n')
        
        # Color the table rows
        colored_table = [Fore.BLUE + Style.BRIGHT + table[0] + Style.RESET_ALL] + [
            Fore.YELLOW + row + Style.RESET_ALL + '\n' for row in table[1:]
        ]
        
        result = '\n'.join(colored_table)
        return result
        
            
    


        
        
