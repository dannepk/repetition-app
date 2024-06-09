from datetime import timedelta
import sys
import gi
import os
import time
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw, Gio

def load_file_content(file_path, description):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = description + "\n" + file.read()
        return content
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        return ""

class MainWindow(Gtk.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_default_size(800, 600)
        self.set_title("Repetition")

        self.box1 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.set_child(self.box1)

        self.button = Gtk.Button(label="Display Questions")
        self.box1.append(self.button)
        self.button.connect('clicked', self.load_questions)

        # Create a button to save content
        self.save_button = Gtk.Button(label="Save Content")
        self.box1.append(self.save_button)
        self.save_button.connect("clicked", self.on_save_button_clicked)

        # Create scrolled window object
        self.scrolledWindow = Gtk.ScrolledWindow()
        self.scrolledWindow.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        self.scrolledWindow.set_hexpand(True)
        self.scrolledWindow.set_vexpand(True)

        # Create text view
        self.textView = Gtk.TextView()
        self.textView.set_wrap_mode(Gtk.WrapMode.WORD)
        self.textView.set_bottom_margin(20)

        self.scrolledWindow.set_child(self.textView)
        self.box1.append(self.scrolledWindow)

    def load_questions(self, button):
        # Load initial text content into the TextView
        buffer = self.textView.get_buffer()

        # Selecting files to be displayed
        dir_path = "/home/daniel/Desktop/repetition/files"
        files = os.listdir(dir_path)
        now = time.time()
        one_day_ago = now - timedelta(days=1).total_seconds()
        seven_days_ago = now - timedelta(days=7).total_seconds()
        thirty_one_days_ago = now - timedelta(days=31).total_seconds()
        text = ""
        for filename in files:
            if filename.endswith(".txt"):
                file_path = os.path.join(dir_path, filename)
                if os.path.isfile(file_path):
                    file_creation_time = os.path.getctime(file_path)
                    if abs(file_creation_time - one_day_ago) < 86400:
                        text += load_file_content(file_path, "1 day ago")
                    elif abs(file_creation_time - seven_days_ago) < 86400:
                        text += load_file_content(file_path, '7 days ago')
                    elif abs(file_creation_time - thirty_one_days_ago) < 86400:
                        text += load_file_content(file_path, '31 days ago')
        buffer.set_text(text)

    def on_save_button_clicked(self, widget):
        dialog = Gtk.FileChooserDialog(
            title="Save File",
            transient_for=self,
            action=Gtk.FileChooserAction.SAVE,
        )
        dialog.add_buttons(
            "Cancel", Gtk.ResponseType.CANCEL,
            "Save", Gtk.ResponseType.OK
        )

        initial_dir = Gio.File.new_for_path("/home/daniel/Desktop/repetition/files")
        dialog.set_current_folder(initial_dir)

        dialog.connect("response", self.on_file_dialog_response)
        dialog.show()

    def on_file_dialog_response(self, dialog, response):
        if response == Gtk.ResponseType.OK:
            file_path = dialog.get_file().get_path()
            if os.path.exists(file_path):
                confirm_dialog = Gtk.MessageDialog(
                    transient_for=self,
                    modal=True,
                    buttons=Gtk.ButtonsType.OK_CANCEL,
                    message_type=Gtk.MessageType.WARNING,
                    text="File already exists. Do you want to overwrite it?"
                )
                confirm_response = confirm_dialog.run()
                confirm_dialog.destroy()
                if confirm_response == Gtk.ResponseType.OK:
                    self.save_content_to_file(file_path)
            else:
                self.save_content_to_file(file_path)
        dialog.destroy()

    def save_content_to_file(self, file_path):
        buffer = self.textView.get_buffer()
        start_iter = buffer.get_start_iter()
        end_iter = buffer.get_end_iter()
        text = buffer.get_text(start_iter, end_iter, False)

        try:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(text)
            print(f"File saved successfully to {file_path}")
        except Exception as e:
            print(f"An error occurred while saving the file: {e}")

class MyApp(Adw.Application):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.connect('activate', self.on_activate)
        self.win = None

    def on_activate(self, app):
        if not self.win:
            self.win = MainWindow(application=app)
        self.win.present()

app = MyApp(application_id="com.example.GtkApplication")
app.run(sys.argv)
