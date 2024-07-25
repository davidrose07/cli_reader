CLI File Reader

A command-line tool for reading and processing various file types, including CSV, JSON, XML, Excel, and SQL databases. The tool supports both direct file processing and interactive file browsing.
Features

    File Processing: Supports CSV, JSON, XML, Excel, and SQL file types.
    Interactive File Browsing: Allows users to browse and select files using a GUI file dialog.
    Command-line Interface: Execute commands and view processed data directly in the terminal.
    Database Support: Converts MySQL and PostgreSQL SQL files to SQLite format for easier processing.

Installation

    Clone the repository:

    git clone <repository-url>

    cd <repository-directory>

    Install the required Python packages:

    First method
    pip install -r requirements.txt
        USAGE: 
        -python3 cli_reader.py <file>
        -python3 cli_reader.py -b   <browse>  

    Preferred Method:
    pip install -e . 
    reader <file>
    reader -b <browse>

Command-line Arguments

    file: The path to the file to be processed. If not provided, the program will require a file to be selected using the -b option.
    -b, --b: Opens a file dialog to select a file for processing.
    -h, --help: Help Menu

File Formats Supported

    CSV: Comma-Separated Values
    JSON: JavaScript Object Notation
    XML: Extensible Markup Language
    Excel: Microsoft Excel files (.xlsx)
    SQL: SQL database files (MySQL, PostgreSQL)
    As well as any text or any code
    May be unsupported file formats that are not tested yet

Example

    To process a CSV file directly:

    python cli_reader.py data.csv
    or reader data.csv

    To open a file dialog and select a file:

    python cli_reader.py -b
    or reader -b

Dependencies

    pandas: For data processing and handling.
    prompt_toolkit: For command-line interface functionality.
    colorama: For colored terminal output.
    tabulate: For tabular data formatting.
    openpyxl, xlrd: For Excel file processing.
    sqlite3: For SQLite database operations.

Logging

The application logs errors and other information to a file located in the log directory. The log file is named exception.log.


License

This project is currently not lisenced