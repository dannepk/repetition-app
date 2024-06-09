import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk

class ScrolledTextWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="Scrolled Text Widget Example")
        self.set_default_size(800, 600)

        # Create a ScrolledWindow
        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)

        # Create a TextView
        self.text_view = Gtk.TextView()
        self.text_view.set_wrap_mode(Gtk.WrapMode.WORD)

        # Add the TextView to the ScrolledWindow
        scrolled_window.append(self.text_view)

        # Add the ScrolledWindow to the main window
        self.append(scrolled_window)

        # Create a Button to load content into the TextView
        load_button = Gtk.Button(label="Load Text")
        load_button.connect("clicked", self.on_load_button_clicked)

        # Create a VBox to hold the button and the scrolled window
        vbox = Gtk.VBox(spacing=6)
        vbox.pack_start(load_button, False, False, 0)
        vbox.pack_start(scrolled_window, True, True, 0)

        self.add(vbox)

    def on_load_button_clicked(self, widget):
        # Load text content into the TextView
        buffer = self.text_view.get_buffer()
        text = "This is an example of a scrolled text widget in GTK using PyGObject.\n" * 10
        buffer.set_text(text)

if __name__ == "__main__":
    win = ScrolledTextWindow()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()
