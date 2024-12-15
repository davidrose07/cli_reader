import sys, os
import signal
from prompt_toolkit.application import Application, get_app
from prompt_toolkit.buffer import Buffer
from prompt_toolkit.layout import Layout, HSplit, ScrollablePane
from prompt_toolkit.layout.containers import Window, WindowAlign
from prompt_toolkit.layout.controls import FormattedTextControl, BufferControl
from prompt_toolkit.layout.dimension import D
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.formatted_text import FormattedText
from prompt_toolkit.styles import Style



class CLIManager:
    def __init__(self, data, file=None):
        self.data = data
        self.file = file
        self.search_query = ""
        self.application = None  # Initialize application as None
        

        # Define styles
        self.style = Style.from_dict({
            'result': 'fg:ansigreen',
            'header': 'fg:ansicyan bold',
            'separator': 'fg:ansiyellow bold',
        })

    def filter_data(self, query, data):
        return [row for row in data if query.lower() in str(row).lower()]

    def colored_text(self, text, style):
        return (style, text)

    def get_filtered_results_text(self):
        if self.data == None:
            with open(self.file, 'r') as file:
                self.data = file.read()
        
        filtered_data = self.filter_data(self.search_query, self.data)
        #column_widths = [max(len(str(value)) +4 for value in column) for column in zip(*self.data, self.column_names)]
        results = []
        for row in filtered_data:
            """ row_text = []
            for values in row:
                row_text.append(self.colored_text(str(values), 'fg:ansigreen'))
            results.extend(row_text) """
            results.append(self.colored_text(row, 'fg:ansigreen'))
        return FormattedText(results) if results else FormattedText([('fg:ansigreen', "No results found")])

    def update_results(self, buffer):
        self.search_query = buffer.text.strip()
        self.application.invalidate()

    """ def get_header_text(self):
        column_widths = [max(len(str(value)) + 4 for value in column) for column in zip(*self.data, self.column_names)]
        header = []
        for name, width in zip(self.column_names, column_widths):
            header.append(self.colored_text(name.ljust(width), 'fg:ansicyan bold'))
        header.append(('', '\n'))
        return FormattedText(header) """

    def run(self):
        #header_text = self.get_header_text()


        """ def header_func():
            separator = self.colored_text('*' * 56, 'fg:ansiyellow bold')
            return FormattedText([separator, ('', '\n')] + list(header_text)) """

        #header_window = Window(content=FormattedTextControl(header_func), height=D(min=2))
        results_window = Window(
            content=FormattedTextControl(
                text=self.get_filtered_results_text),
                #get_cursor_position=lambda: Point(0, self.row_position)),
            always_hide_cursor=True)
        #scrollable_results = ScrollablePane(results_window)
        search_buffer = Buffer(on_text_changed=lambda buffer: self.update_results(buffer))
        search_window = Window(content=BufferControl(buffer=search_buffer), height=1, align=WindowAlign.LEFT)

        root_container = HSplit([
            #header_window,
            results_window,
            #scrollable_results,
            Window(height=D.exact(1)),
            search_window,
        ])

        layout = Layout(root_container)
        kb = KeyBindings()

        @kb.add("c-c")
        def exit_(event):
            raise KeyboardInterrupt
        
        """ @kb.add("up")
        def scroll_up(event):
            event.app.layout.focus(results_window)
            index = results_window.get_vertical_scroll()
            if index > 0:
                index -= 1
                self.application.invalidate()

        @kb.add("down")
        def scroll_down(event):
            event.app.layout.focus(results_window)
            index = results_window.get_vertical_scroll()
            index += 1
            self.application.invalidate() """            
        
        
        self.application = Application(layout=layout, key_bindings=kb, full_screen=True, style=self.style)

        # Signal handler for clean exit on Control+C
        def signal_handler(sig, frame):
            if self.application and self.application.is_running:
                self.application.exit()
            sys.exit(0)

        signal.signal(signal.SIGINT, signal_handler)

        try:
            self.application.run()
        except KeyboardInterrupt:
            self.exit()

    def exit(self):
        if self.application and self.application.is_running:
            self.application.exit()
            os.system('reset')
            print("Application exited.")

    

    def __del__(self):
        self.exit()
        print("Exit CLI Manager")
