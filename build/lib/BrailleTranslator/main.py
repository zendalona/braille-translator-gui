###########################################################################
#    Braile-Translator
#
#    Copyright (C) 2022-2023 Greeshna Sarath <greeshnamohan001@gmail.com>
#    
#    V T Bhattathiripad College, Sreekrishnapuram, Kerala, India
#
#    This project supervised by Zendalona(2022-2023) 
#
#    Project Home Page : www.zendalona.com/braille-translator
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
###########################################################################

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, Pango

from BrailleTranslator import utils
from BrailleTranslator import preferences

# braille translation
import louis

#user guide
import webbrowser

import os

#for undo/redo
import queue

user_preferences_file_path = os.environ['HOME']+'/.braille-translator.cfg'

class BrailleTranslatorWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Braille Translator")

        # User Preferences
        self.pref = preferences.Preferences()
        self.pref.load_preferences_from_file(user_preferences_file_path)

        self.line_limit = 0

        #for both text fields to be vertical and spacing between them
        main_vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, 
        spacing=8)
        self.add(main_vbox)
        
        #create gtk menubar  and placed in top window
        menubar = Gtk.MenuBar()
        self.create_menu(menubar)
        main_vbox.pack_start(menubar, False, False, 0)
        
        """It creates a menu item with the label "About" and assigns it 
        to the variable about_menu_item."""
        about_menu_item = Gtk.MenuItem(label="About")
        about_menu_item.connect("activate", self.show_about_dialog)
        
        help_menu = Gtk.Menu()
        help_menu.append(about_menu_item)
        
        """It creates a menu item with the label "userguide" and assigns 
        it to the variable about_menu_item."""
        user_guide_menu_item = Gtk.MenuItem(label="User Guide")
        user_guide_menu_item.connect("activate", self.open_user_guide)
        help_menu.append(user_guide_menu_item)
        help_menu_item = Gtk.MenuItem(label="Help")
        help_menu_item.set_submenu(help_menu)
        
        menubar.append(help_menu_item)
        
        # Create the about dialog
        self.about_dialog = MyAboutDialog(self)

        box_primary_widgets = Gtk.Box(
            orientation=Gtk.
            Orientation.
            HORIZONTAL,
            spacing=8
            )
        
        main_vbox.pack_start(box_primary_widgets,False,True,0)

        #create language compbox label
        label = Gtk.Label()
        label.set_label("Language")
        box_primary_widgets.pack_start(label, False, False, 0)
        
        """Gtk.ListStore object and assigns it to the instance variable 
        self.table_store for populated language  combobox"""
        self.table_store = Gtk.ListStore(str, str)

        #represents a file path and filename of languge table
        filename_with_path="/usr/share/BrailleTranslator/language-table-dict.txt";
        with open(
        filename_with_path, "r") as file:
            for line in file:
                stripped_line = line.strip()
                self.table_store.append(
                [stripped_line.split(" ")[0], 
                stripped_line.split(" ")[1]]
                )

        #combobox
        self.language_combo1 = Gtk.ComboBox()
        self.language_combo1.set_model(self.table_store)
        renderer_text3 = Gtk.CellRendererText()
        self.language_combo1.pack_start(renderer_text3, True)
        self.language_combo1.add_attribute(renderer_text3, "text", 0)
        self.language_combo1.set_active(self.pref.language)
        #self.language_combo1.set_size_request(200, 40)
        self.language_combo1.connect(
        "changed", self.on_language_changed,
        )
        box_primary_widgets.pack_start(
        self.language_combo1, False, False, 0
        )

        label.set_mnemonic_widget(self.language_combo1)
        
        #for spin button
        label = Gtk.Label("line limit")
        box_primary_widgets.pack_start(label, False, False, 0)
        
        # Create the spin button
        self.spin_button = Gtk.SpinButton()
        
        # Set the minimum and maximum values
        self.spin_button.set_range(1, 100) 
        
        # Set the initial value 
        self.spin_button.set_value(40)
        
        # Set the increment and page increment values
        self.spin_button.set_increments(1, 10)
        #self.set_size_request(225, 40)
        box_primary_widgets.pack_start(
        self.spin_button, False, False, 0
        )
        
        label.set_mnemonic_widget(self.spin_button)
        
        #translation button
        self.translate_button = Gtk.Button(label="Translate")
        self.translate_button.connect("clicked", self.on_translate_clicked)
        
        self.back_translate_button = Gtk.Button(label="Back Translate")
        self.back_translate_button.connect("clicked", self.on_back_translate_clicked)

        box_primary_widgets.pack_start(
        self.translate_button, True, True, 0
        )
        
        box_primary_widgets.pack_start(
        self.back_translate_button, True, True, 0
        )
        #self.translate_button.set_size_request(325, 50)
     
        """draggable separator in between 2 textviews,split allows users 
        to adjust the size allocation between two textviews."""
        input_output_paned = Gtk.Paned()
        input_output_paned.set_orientation(Gtk.Orientation.HORIZONTAL)
        
        #create first textview for input text using gtk textview 
        self.textview1 = Gtk.TextView()
        self.textview1.set_accepts_tab(False)
        
        #tooltips for identifying textviews wia  screen reader
        self.textview1.set_tooltip_text("Input Text") 
        self.textview1.get_buffer().connect('insert-text', 
        self.push_text_to_undobuffer1)

        
        """wrap mode determines how text content is wrapped and displayed 
        within the widget. here,wrap mode allows you to control how 
        long lines of text are displayed within the textview.""" 
        self.textview1.set_wrap_mode(Gtk.WrapMode.WORD_CHAR)
        
        """The theme store allows you to customize the visual appearance 
        of your application.here used to create font color and 
        background color of both textviews"""
        self.theme_store = Gtk.ListStore(str, str, str)
        self.theme_store.append(["Default", "", ""])
        self.theme_store.append(["White on Black", "#FFFFFF", "#000000"])
        self.theme_store.append(["Black on White", "#000000", "#FFFFFF"])
        self.theme_store.append(["Green on Black", "#00FF00", "#000000"])
        self.theme_store.append(["Yellow on Black", "#FFFF00", "#000000"])
        self.theme_store.append(["Up Sky Blue", "#0F2447", "#A0B0CB"])
        self.theme_store.append(["Sharp Green", "#19480D", "#A6C99D"])
        self.theme_store.append(["Broad Yellow", "#322C0B", "#BDB58C"])
        self.theme_store.append(["Tragic Red", "#42190D", "#B79990"])
        self.theme_store.append(["Velvet Orchid", "#340E3E", "#B895C1"])
        self.theme_store.append(["Dollic Pink", "#410E3F", "#C695C4"])
        self.theme_store.append(["Scale Gray", "#1F2325", "#C9CEC5"])
        self.theme_store.append(["Brown Brown", "#2B1406", "#D6B9A8"])


        """Gtk.HBox is a container widget that arranges its child widgets
        horizontally in a single row.here toolbar set to 
        horizontal box"""
        hbox1 = Gtk.HBox()
        hbox1.set_hexpand(True)
        hbox1.set_vexpand(False)
        
        #create font 
        label = Gtk.Label()
        label.set_text("Font ")
        self.font_button = Gtk.FontButton()
        self.font_button.connect(
        "font-set", self.on_font_set, 
        self.textview1
        )
        self.font_button.set_font(self.pref.font_1)

        # calling on_font_set manually because set_font wont trigger "font-set" signal
        self.on_font_set(self.font_button, self.textview1);

        label.set_mnemonic_widget(self.font_button)
        hbox1.pack_start(label,False,True,0)
        hbox1.pack_start(self.font_button,False,True,0)
        
        fixed = Gtk.Fixed()
        hbox1.pack_start(fixed,True,True,0)
        
        #set font color and background color 
        self.font_color = "#ffffff"
        self.background_color = "#000000"
        
        label = Gtk.Label()
        label.set_text("Theme ")
        self.combobox_theme = Gtk.ComboBox()
        self.combobox_theme.set_model(self.theme_store)
        renderer_text = Gtk.CellRendererText()
        self.combobox_theme.pack_start(renderer_text, True)
        self.combobox_theme.add_attribute(renderer_text, "text", 0)
        self.combobox_theme.connect(
        "changed", self.on_theme_changed, self.textview1
        )
        self.combobox_theme.set_active(self.pref.theme_1);
        label.set_mnemonic_widget(self.combobox_theme)
        hbox1.pack_start(label,False,True,0)
        hbox1.pack_start(self.combobox_theme,False,True,0)

        fixed = Gtk.Fixed()
        hbox1.pack_start(fixed,True,True,0)

        #scrolled window for first trxtview
        scrolled_win1 = Gtk.ScrolledWindow()
        scrolled_win1.set_policy(Gtk.PolicyType.NEVER, 
        Gtk.PolicyType.ALWAYS)
        scrolled_win1.add(self.textview1)
        scrolled_win1.set_size_request(500, 500)

        box1 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        box1.set_vexpand(True)
        box1.pack_start(scrolled_win1, True, True, 0)
        box1.pack_start(hbox1, False, True, 0)

        input_output_paned.add1(box1)

        #second textview
        self.textview2 = Gtk.TextView()
        self.textview2.set_wrap_mode(Gtk.WrapMode.WORD_CHAR)
        self.textview2.set_accepts_tab(False)
        
        #tooltips for identifying textviews wia  screen reader
        self.textview2.set_tooltip_text("Output Text")
        self.textview2.get_buffer().connect('insert-text', 
        self.push_text_to_undobuffer2)

   
        hbox2 = Gtk.HBox()
        hbox2.set_hexpand(True)
        hbox2.set_vexpand(False)
        
        #font for second textview
        label = Gtk.Label()
        label.set_text("Font ")
        self.font_button2 = Gtk.FontButton()
        self.font_button2.connect("font-set", 
        self.on_font_set, self.textview2)
        label.set_mnemonic_widget(self.font_button2)
        hbox2.pack_start(label,False,True,0)
        hbox2.pack_start(self.font_button2,False,True,0)
        self.font_button2.set_font(self.pref.font_2)

        # calling on_font_set manually because set_font wont trigger "font-set" signal
        self.on_font_set(self.font_button2, self.textview2);

        fixed = Gtk.Fixed()
        hbox2.pack_start(fixed,True,True,0)
      
        #font and background color for output text
        self.font_color = "#ffffff"
        self.background_color = "#000000"
        
        label = Gtk.Label()
        label.set_text("Theme ")
        
        self.combobox_theme2 = Gtk.ComboBox()
        self.combobox_theme2.set_model(self.theme_store)
        
        renderer_text2 = Gtk.CellRendererText()
        
        self.combobox_theme2.pack_start(renderer_text2, True)
        self.combobox_theme2.add_attribute(renderer_text2, "text", 0)
        self.combobox_theme2.connect(
        "changed", self.on_theme_changed, self.textview2
        )
        self.combobox_theme2.set_active(self.pref.theme_2);
        
        label.set_mnemonic_widget(self.combobox_theme2)
        
        hbox2.pack_start(label,False,True,0)
        hbox2.pack_start(self.combobox_theme2,False,True,0)
        
        fixed = Gtk.Fixed()
        hbox2.pack_start(fixed,True,True,0)
    
        #scrolled window for second textview
        scrolled_win2 = Gtk.ScrolledWindow()
        scrolled_win2.set_policy(Gtk.PolicyType.NEVER, 
        Gtk.PolicyType.ALWAYS)
        scrolled_win2.add(self.textview2)
        scrolled_win2.set_size_request(500, 500)

        box2 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        box2.set_vexpand(True)
        box2.pack_start(scrolled_win2, True, True, 0)
        box2.pack_start(hbox2, False, True, 0)

        input_output_paned.add2(box2)
        main_vbox.pack_start(input_output_paned,False,True,0)
       
        self.connect("key-press-event",self.on_key_press_event)
        
        # Undo/Redo 
        self.undo_queue1 = queue.LifoQueue()
        self.redo_queue1 = queue.LifoQueue()
        self.undo_queue2 = queue.LifoQueue()
        self.redo_queue2 = queue.LifoQueue()
        
        # Add inetial text to undo_queue
        self.push_text_to_undobuffer1()
        self.push_text_to_undobuffer2()
  
        self.show_all()
        self.connect("destroy", self.quit);
        Gtk.main()
        
    #menu function
    def create_menu(self, menubar):

        # Create the "File" menu
        file_menu = Gtk.Menu()

        accel_group = Gtk.AccelGroup()
        self.add_accel_group(accel_group)
            
        new_item = Gtk.MenuItem.new_with_label("New")
        new_item.connect("activate", self.on_new_activated)
        file_menu.append(new_item)
        key,mods=Gtk.accelerator_parse("<Ctrl>N")
        new_item.add_accelerator("activate", accel_group, key, mods, 
        Gtk.AccelFlags.VISIBLE)

        open_item = Gtk.MenuItem.new_with_label("Open")
        open_item.connect("activate", self.on_open_activated)
        file_menu.append(open_item)
        key,mods=Gtk.accelerator_parse("<Ctrl>O")
        open_item.add_accelerator("activate", accel_group, key, mods,  
        Gtk.AccelFlags.VISIBLE)

        save_item = Gtk.MenuItem.new_with_label("Save")
        save_item.connect("activate", self.on_save_activated)
        file_menu.append(save_item)
        key,mods=Gtk.accelerator_parse("<Ctrl>S")
        save_item.add_accelerator("activate", accel_group, key, mods,  
        Gtk.AccelFlags.VISIBLE)

        save_as_item = Gtk.MenuItem.new_with_label("Save As")
        save_as_item.connect("activate", self.on_save_as_activated)
        file_menu.append(save_as_item)
        key,mods=Gtk.accelerator_parse("<Ctrl><shift>S")
        save_as_item.add_accelerator("activate", accel_group, key, mods,  
        Gtk.AccelFlags.VISIBLE)

        save_as_brf_item = Gtk.MenuItem.new_with_label("Save as BRF")
        save_as_brf_item.connect("activate", self.on_save_as_brf_activated)
        file_menu.append(save_as_brf_item)
        #key,mods=Gtk.accelerator_parse("<Ctrl>S")
        #save_as_brf_item.add_accelerator("activate", accel_group, key, mods,
        #Gtk.AccelFlags.VISIBLE)

        file_menu_item = Gtk.MenuItem.new_with_label("File")
        file_menu_item.set_submenu(file_menu)

        # Create the "Edit" menu
        edit_menu = Gtk.Menu()
        
        cut_item = Gtk.MenuItem.new_with_label("Cut")
        cut_item.connect("activate", self.on_cut_activated)
        edit_menu.append(cut_item)
        key,mods=Gtk.accelerator_parse("<Ctrl>X")
        cut_item.add_accelerator("activate", accel_group, key, mods,  
        Gtk.AccelFlags.VISIBLE)

        copy_item = Gtk.MenuItem.new_with_label("Copy")
        copy_item.connect("activate", self.on_copy_activated)
        edit_menu.append(copy_item)
        key,mods=Gtk.accelerator_parse("<Ctrl>C")
        copy_item.add_accelerator("activate", accel_group, key, mods,  
        Gtk.AccelFlags.VISIBLE)

        paste_item = Gtk.MenuItem.new_with_label("Paste")
        paste_item.connect("activate", self.on_paste_activated)
        edit_menu.append(paste_item)
        key,mods=Gtk.accelerator_parse("<Ctrl>P")
        paste_item.add_accelerator("activate", accel_group, key, mods,  
        Gtk.AccelFlags.VISIBLE)

        goto_item = Gtk.MenuItem(label="Goto Line")
        edit_menu.append(Gtk.SeparatorMenuItem())
        edit_menu.append(goto_item)
        # Connect Goto Line menu item to callback function
        goto_item.connect("activate", self.on_goto_line_activate)
        key,mods=Gtk.accelerator_parse("<Ctrl>G")
        goto_item.add_accelerator("activate", accel_group, key, mods,  
        Gtk.AccelFlags.VISIBLE)

        edit_menu.append(Gtk.SeparatorMenuItem())

        find = Gtk.MenuItem(label="Find")
        edit_menu.append(find)
        find.connect("activate", self.on_find_activate)
        key,mods=Gtk.accelerator_parse("<Ctrl>F")
        find.add_accelerator("activate", accel_group, key, mods,  
        Gtk.AccelFlags.VISIBLE)

        find_and_replace = Gtk.MenuItem(label="Find and Replace")
        edit_menu.append(find_and_replace)
        find_and_replace.connect("activate", 
        self.on_find_and_replace_activate)
        key,mods=Gtk.accelerator_parse("<Ctrl>R")
        find_and_replace.add_accelerator(
        "activate", accel_group, key, mods,  
        Gtk.AccelFlags.VISIBLE
        )

        edit_menu.append(Gtk.SeparatorMenuItem())

        undo_menu_item = Gtk.MenuItem(label="Undo")
        edit_menu.append(undo_menu_item)
        undo_menu_item.connect("activate", self.undo)
        key,mods=Gtk.accelerator_parse("<Ctrl>Z")
        undo_menu_item.add_accelerator(
        "activate", accel_group, key, mods,  
        Gtk.AccelFlags.VISIBLE
        )

        redo_menu_item = Gtk.MenuItem(label="Redo")
        edit_menu.append(redo_menu_item)
        redo_menu_item.connect("activate", self.redo)
        key,mods=Gtk.accelerator_parse("<Shift><Ctrl>Z")
        redo_menu_item.add_accelerator(
        "activate", accel_group, key, mods,  
        Gtk.AccelFlags.VISIBLE
        )

        edit_menu_item = Gtk.MenuItem.new_with_label("Edit")
        edit_menu_item.set_submenu(edit_menu)
        
        # Add menu items to the menubar
        menubar.append(file_menu_item)
        menubar.append(edit_menu_item)

    def on_key_press_event(self, widget, event):
        #print("Key press on widget: ", widget)
        #print("          Modifiers: ", event.state)
        #print("      Key val, name: ", event.keyval, 
        #Gdk.keyval_name(event.keyval))

        # check the event modifiers (can also use SHIFTMASK, etc)
        shift = (event.state & Gdk.ModifierType.SHIFT_MASK)
        ctrl = (event.state & Gdk.ModifierType.CONTROL_MASK)
        alt = (event.state & Gdk.ModifierType.MOD1_MASK)

        # see if we recognise a keypress
        if alt and event.keyval == Gdk.KEY_1:
            self.textview1.grab_focus()

        # see if we recognise a keypress
        if alt and event.keyval == Gdk.KEY_2:
            self.textview2.grab_focus()

        # see if we recognise a keypress
        if ctrl and event.keyval == Gdk.KEY_t:
            self.on_translate_clicked(None)

    #new 
    def on_new_activated(self, widget): 
        # Clear the active text view and set focus to it
        if self.textview1.has_focus():
            self.textview1.get_buffer().set_text("")
            self.textview1.grab_focus()
        elif self.textview2.has_focus():
            self.textview2.get_buffer().set_text("")
            self.textview2.grab_focus()
        else:
            # Clear data in both text fields
            self.textview1.get_buffer().set_text("")
            self.textview2.get_buffer().set_text("")

    #open
    def on_open_activated(self, widget):
        focused_textview = self.get_focus()

        dialog = Gtk.FileChooserDialog(
        title="Open", parent=self, 
        action=Gtk.FileChooserAction.OPEN
        )
        
        dialog.add_buttons(
        Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, 
        Gtk.STOCK_OPEN, Gtk.ResponseType.OK
        )
        
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            filename = dialog.get_filename()

            # Load the BRF (Braille Ready Format) to braille view
            # If not BRF, Determine the focused text view and load the file there
            if(filename.endswith(".brf")):
                self.load_text(filename, self.textview2, True)
            else:
                if focused_textview == self.textview2:
                    self.load_text(filename, self.textview2)
                else:
                    self.load_text(filename, self.textview1)
        dialog.destroy()


    def load_text(self, filename, textview, brf=False):
        with open(filename, "r") as file:
            text = file.read()
            buffer = textview.get_buffer()
            if(brf):
                text = utils.braille_ASCII_to_braille_unicode(text)
            buffer.set_text(text)
    
    #save
    def on_save_activated(self, widget):
        dialog = Gtk.FileChooserDialog(
        title="Save",parent=self,
        action=Gtk.FileChooserAction.SAVE,buttons=(Gtk.STOCK_CANCEL, 
        Gtk.ResponseType.CANCEL, Gtk.STOCK_SAVE, Gtk.ResponseType.OK),
        )
        dialog.set_do_overwrite_confirmation(True)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            filename = dialog.get_filename()
            self.save_file(filename)

        dialog.destroy()

    def save_file(self, filename):

        # Get the focused text view
        focused_textview = self.get_focus()
        buffer = focused_textview.get_buffer()

        # Get the text from the buffer
        start_iter = buffer.get_start_iter()
        end_iter = buffer.get_end_iter()
        text = buffer.get_text(start_iter, end_iter, True)

        # Save the text to the specified file
        with open(filename, "w") as file:
            file.write(text)
            
    #save_as
    def on_save_as_activated(self, widget):
        dialog = Gtk.FileChooserDialog(
        title="Save As",
        parent=self,action=Gtk.FileChooserAction.SAVE,
        buttons=(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
        Gtk.STOCK_SAVE, Gtk.ResponseType.OK),
        )
        
        dialog.set_do_overwrite_confirmation(True)
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            filename = dialog.get_filename()
            self.save_file(filename)

        dialog.destroy()

    #save_as_brf
    def on_save_as_brf_activated(self, widget):
        dialog = Gtk.FileChooserDialog(
        title="Save as brf",
        parent=self,action=Gtk.FileChooserAction.SAVE,
        buttons=(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
        Gtk.STOCK_SAVE, Gtk.ResponseType.OK),
        )
        
        dialog.set_do_overwrite_confirmation(True)

        filter_brf = Gtk.FileFilter()
        filter_brf.set_name("BRF (Braille Ready Format)")
        filter_brf.add_pattern("*.brf")
        dialog.add_filter(filter_brf)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            filename = dialog.get_filename()
            self.save_as_brf_file(filename)

        dialog.destroy()

    def save_as_brf_file(self, filename):

        # Only output will be saved as brf
        buffer = self.textview2.get_buffer()

        # Get the text from the buffer
        start_iter = buffer.get_start_iter()
        end_iter = buffer.get_end_iter()
        text = buffer.get_text(start_iter, end_iter, True)

        text_in_brf = utils.braille_unicode_to_braille_ASCII(text)

        # Save the text to the specified file
        with open(filename, "wb") as file:
            file.write(text_in_brf.encode())
            file.write("\n".encode())
            file.write("\n".encode())
            file.write(bytes([26]))
    
    #cut       
    def on_cut_activated(self, widget):
        # Get the focused text view
        focused_textview = self.get_focus()

        # Get the buffer of the focused text view
        buffer = focused_textview.get_buffer()

        # Check if any text is selected in the text view
        if buffer.get_has_selection():
            # Get the selected text range
            start_iter, end_iter = buffer.get_selection_bounds()

            # Extract the selected text
            text = buffer.get_text(start_iter, end_iter, True)

            # Copy the selected text to the clipboard
            clipboard = Gtk.Clipboard.get_default(self.get_display())
            clipboard.set_text(text, -1)

            # Delete the selected text from the buffer
            buffer.delete(start_iter, end_iter)
    
    #copy        
    def on_copy_activated(self, widget):
        # Get the focused text view
        focused_textview = self.get_focus()

        # Get the buffer of the focused text view
        buffer = focused_textview.get_buffer()

        # Check if any text is selected in the text view
        if buffer.get_has_selection():
            # Get the selected text range
            start_iter, end_iter = buffer.get_selection_bounds()

            # Extract the selected text
            text = buffer.get_text(start_iter, end_iter, True)

            # Copy the selected text to the clipboard
            clipboard = Gtk.Clipboard.get_default(self.get_display())
            clipboard.set_text(text, -1)
     
    #paste       
    def on_paste_activated(self, widget):
        # Get the focused text view
        focused_textview = self.get_focus()

        # Get the buffer of the focused text view
        buffer = focused_textview.get_buffer()

        # Get the clipboard content
        clipboard = Gtk.Clipboard.get_default(
        self.get_window().get_display()
        )
        text = clipboard.wait_for_text()

        # Insert the clipboard content at the cursor position
        if text:
            # Get the cursor position in the buffer
            cursor_iter = buffer.get_iter_at_mark(buffer.get_insert())

            # Insert the clipboard content at the cursor position
            buffer.insert(cursor_iter, text)
     
    #find      
    def on_find_activate(self, widget):
        focused_textview = self.get_focus()
        Find(focused_textview).show()
        
    #find and replace
    def on_find_and_replace_activate(self, widget):
        focused_textview = self.get_focus()
        FindAndReplace(focused_textview).show()

    #goto line
    def on_goto_line_activate(self, widget):
        dialog = Gtk.Dialog(title="Goto Line", parent=self, flags=0)
        dialog.add_button(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL)
        dialog.add_button(Gtk.STOCK_OK, Gtk.ResponseType.OK)

        # Create a label
        label = Gtk.Label(label="Enter line number:")
        dialog.vbox.pack_start(label, True, True, 0)

        # Create a spin button for line number input
        adjustment = Gtk.Adjustment(1, 1, 1000, 1, 10, 0)
        spin_button = Gtk.SpinButton()
        spin_button.set_adjustment(adjustment)
        dialog.vbox.pack_start(spin_button, True, True, 0)

        # Get the active text view
        active_textview = self.get_active_textview()

        if active_textview is not None:
            """Get the current line number based on the mouse cursor 
            position"""
            buffer = active_textview.get_buffer()
            insert_mark = buffer.get_insert()
            insert_iter = buffer.get_iter_at_mark(insert_mark)
            line_number = insert_iter.get_line() + 1

            # Set the default line number in the spin button
            spin_button.set_value(line_number)
        dialog.show_all()
        response = dialog.run()

        if response == Gtk.ResponseType.OK:
            line_number = int(spin_button.get_value())

            if active_textview is not None:
                # Move the cursor to the desired line
                buffer = active_textview.get_buffer()
                line_iter = buffer.get_iter_at_line(line_number - 1)
                buffer.place_cursor(line_iter)

                # Scroll the text view to the desired line
                active_textview.scroll_to_iter(line_iter, 0.0, True, 
                0.5, 0.5)

        dialog.destroy()
 
    #focuse active textview
    def get_active_textview(self):
        focus = self.get_focus()
        if focus == self.textview1:
            return self.textview1
        elif focus == self.textview2:
            return self.textview2
        else:
            return None

    #about
    def show_about_dialog(self, widget):
        self.about_dialog.run()
        self.about_dialog.hide()

    #userguide
    def open_user_guide(self,wedget,data=None):
        url = "/path/to/user_guide_file.pdf"
        try:
            webbrowser.get("firefox").open(url, new=2)
        except webbrowser.Error:
            webbrowser.open(url, new=2)

    def on_translate_clicked(self, button):
        # Get the value of the spin button
        line_limit = int(self.spin_button.get_value())

        # Get the text buffer of the first text view
        buffer1 = self.textview1.get_buffer()

        # Check if any text is selected in the text view
        if buffer1.get_has_selection():
            # Case 2: Translate only the selected portion
            start_iter, end_iter = buffer1.get_selection_bounds()
            text1 = buffer1.get_text(start_iter, end_iter, True)
        else:
            # Case 1: Translate the entire content
            text1 = buffer1.get_text(buffer1.get_start_iter(), buffer1.get_end_iter(), True)

        # Get the index of the selected language in the combo box
        language_active = self.language_combo1.get_active()
        table_name = self.table_store[language_active][1]

        table_list = ['unicode.dis']
        table_list.append(table_name)

        # Get the cursor position in the second text view
        buffer2 = self.textview2.get_buffer()
        cursor_mark = buffer2.get_insert()
        cursor_iter = buffer2.get_iter_at_mark(cursor_mark)
        cursor_position = cursor_iter.get_offset()

        # Get the existing text in the second text view
        existing_text = buffer2.get_text(buffer2.get_start_iter(), buffer2.get_end_iter(), True)

        # Translate the text to Braille using the selected table
        braille = louis.translate(table_list, text1)

        # Shape the braille output for printer
        new_text = self.shape_text_with_line_limit(braille[0], line_limit)

        # Check if the second text view is already empty
        if not existing_text:
            # If it's empty, set the text directly translated
            buffer2.set_text(new_text)
        else:
            # otherwise, Provide options to the user
            dialog = Gtk.Dialog(" Choose the Translation Options", self, Gtk.DialogFlags.MODAL | Gtk.DialogFlags.DESTROY_WITH_PARENT)

            button_replace = Gtk.Button.new_with_label("Replace entire content")
            button_insert = Gtk.Button.new_with_label("Insert at cursor point")

            # Add buttons to the dialog with the correct order
            dialog.add_button("Replace entire content", Gtk.ResponseType.YES)
            dialog.add_button("Insert at cursor point", Gtk.ResponseType.NO)
            dialog.add_button(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL)

            dialog.set_default_response(Gtk.ResponseType.CANCEL)

            # Run the dialog and get the response
            response = dialog.run()

            if response == Gtk.ResponseType.YES:
                # Case 1: Replace the entire content
                buffer2.set_text(new_text)
            elif response == Gtk.ResponseType.NO:
                # Case 2: Insert at cursor point
                buffer2.insert(cursor_iter, new_text)

            dialog.destroy()

        # Restore the cursor position in the second text view
        if cursor_position <= len(buffer2.get_text(buffer2.get_start_iter(), buffer2.get_end_iter(), True)):
            cursor_iter = buffer2.get_iter_at_offset(cursor_position)
            buffer2.place_cursor(cursor_iter)

    #line limit        
    def shape_text_with_line_limit(self, input_text, length):
        output_text = ""
        character_count = 0
        for character in input_text:
            if(character_count == length):
                character_count = 1;
                output_text = output_text + "\n"
            else:
                character_count = character_count+1
            output_text = output_text+character
        return output_text
        
    
    def on_back_translate_clicked(self, button):
        # Get the text buffer of the second text view
        buffer2 = self.textview2.get_buffer()

        # Check if any text is selected in the text view
        if buffer2.get_has_selection():
            # Case 2: Back-translate only the selected portion
            start_iter, end_iter = buffer2.get_selection_bounds()
            braille_text = buffer2.get_text(start_iter, end_iter, True)
        else:
            # Case 1: Back-translate the entire content
            braille_text = buffer2.get_text(buffer2.get_start_iter(), buffer2.get_end_iter(), True)

        # Get the index of the selected language in the combo box (if applicable)
        language_active = self.language_combo1.get_active()

        # Get the corresponding Braille table 
        table_name = self.table_store[language_active][1]

        # Define the table_list for Braille-to-text retranslation
        table_list = ['unicode.dis']
        table_list.append(table_name)

        # Implement the back-translation logic using the louis library
        retranslated_result = louis.backTranslate(table_list, braille_text)

        if retranslated_result is not None:
            # Extract the retranslated text from the tuple
            original_text = retranslated_result[0]

            # Check if the first text view is already empty or not
            buffer1 = self.textview1.get_buffer()
            if not buffer1.get_text(buffer1.get_start_iter(), buffer1.get_end_iter(), True):
                # If it's empty, set the text directly transalated
                buffer1.set_text(original_text)
            else:
                # otherwise, Provide options to the user
                dialog = Gtk.Dialog("Choose the Back-Translation Options", self, Gtk.DialogFlags.MODAL | Gtk.DialogFlags.DESTROY_WITH_PARENT)

                button_replace = Gtk.Button.new_with_label("Replace entire content")
                button_insert = Gtk.Button.new_with_label("Insert at cursor point")

                # Add buttons to the dialog with the correct order
                dialog.add_button("Replace entire content", Gtk.ResponseType.YES)
                dialog.add_button("Insert at cursor point", Gtk.ResponseType.NO)
                dialog.add_button(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL)

                dialog.set_default_response(Gtk.ResponseType.CANCEL)

                # Run the dialog and get the response
                response = dialog.run()

                if response == Gtk.ResponseType.YES:
                    # Case 1: Replace the entire content
                    buffer1.set_text(original_text)
                elif response == Gtk.ResponseType.NO:
                    # Case 2: Insert at cursor point
                    cursor_mark = buffer1.get_insert()
                    cursor_iter = buffer1.get_iter_at_mark(cursor_mark)
                    cursor_position = cursor_iter.get_offset()
                    buffer1.insert(cursor_iter, original_text)
                    buffer1.place_cursor(buffer1.get_iter_at_offset(cursor_position + len(original_text)))

                dialog.destroy()

        else:
            print("Back-translation failed. Check the Braille table and input text.")
 

    def set_cursor_color(self, textview, color):
        colors_in_float = Gdk.color_parse(color).to_floats()
        cursor_color_hex = "#" + "".join(["%02x" % (int(color * 255)) 
        for color in colors_in_float])
        
        try:
            cssProvider = Gtk.CssProvider()
            cssProvider.load_from_data(
            (" * {   caret-color: "+cursor_color_hex+";    }").encode
            ('ascii')
            )
        
            style = textview.get_style_context()
            style.add_provider(cssProvider, 
            Gtk.STYLE_PROVIDER_PRIORITY_USER)
        except:
            print("Unnable to set cursor color!")


    #font/background color
    def set_selection_color(self, textview, font_color, background_color):
        color1 = Gdk.color_parse(font_color)
        color2 = Gdk.color_parse(background_color)
        
        selection_color = Gdk.Color((color1.red + color2.red)/2, 
        (color1.green + color2.green)/2 ,
        (color1.blue + color2.blue)/2)
        
        selection_colors_in_float = selection_color.to_floats()
        selection_background_colors_in_float = color2.to_floats()
        selection_color_hex = "#" + "".join(["%02x" % (int(color * 255))
        for color in selection_colors_in_float])
        selection_background_color_hex = "#" + "".join(["%02x" % (
        int(color * 255)) 
        for color in selection_background_colors_in_float])
        
        try:
            cssProvider = Gtk.CssProvider()
            cssProvider.load_from_data(
            (" * selection { color: "
            +selection_color_hex+";  background: "
            +selection_background_color_hex+";}").encode('ascii')
            )
        
            style = textview.get_style_context()
            style.add_provider(cssProvider, Gtk.STYLE_PROVIDER_PRIORITY_USER)
        except:
            print("Unnable to set selection color!")


    def on_language_changed(self,widget):
        self.pref.language = widget.get_active()
        self.pref.save_preferences_to_file(user_preferences_file_path)

    def on_theme_changed(self,widget, textview):
        theme = widget.get_active()
        
        font_color = self.theme_store[theme][1]
        background_color = self.theme_store[theme][2]
        
        if(theme == 0):
            textview.modify_fg(Gtk.StateFlags.NORMAL, None)
            textview.modify_bg(Gtk.StateFlags.NORMAL, None)
            font_color = "#000000" 
            background_color = "#ffffff"
        else:
            textview.modify_fg(Gtk.StateFlags.NORMAL, 
            Gdk.color_parse(font_color))
            textview.modify_bg(Gtk.StateFlags.NORMAL, 
            Gdk.color_parse(background_color ))
        self.set_cursor_color(textview, font_color)
        self.set_selection_color(textview, font_color, background_color)

        if(textview == self.textview1):
            self.pref.theme_1 = theme
        else:
            self.pref.theme_2 = theme
        self.pref.save_preferences_to_file(user_preferences_file_path)

    #font style/size
    def on_font_set(self,widget, textview):
        font = widget.get_font_name();
        pangoFont = Pango.FontDescription(font)
        textview.modify_font(pangoFont)

        if(textview == self.textview1):
            self.pref.font_1 = font
        else:
            self.pref.font_2 = font
        self.pref.save_preferences_to_file(user_preferences_file_path)

    #undo
    def undo(self,wedget,data=None):
        if self.textview1.has_focus():
            if( not self.undo_queue1.empty()):
                text_in_queue = self.undo_queue1.get()
                buffer = self.textview1.get_buffer()
                start_iter, end_iter = buffer.get_bounds()
                text_in_view = buffer.get_text(start_iter, end_iter, True)
                buffer.set_text(text_in_queue)
                self.redo_queue1.put(text_in_view)
        elif self.textview2.has_focus():
            if( not self.undo_queue2.empty()):
                text_in_queue = self.undo_queue2.get()
                buffer = self.textview2.get_buffer()
                start_iter, end_iter = buffer.get_bounds()
                text_in_view = buffer.get_text(start_iter, end_iter, True)
                buffer.set_text(text_in_queue)
                self.redo_queue2.put(text_in_view)

    #redo
    def redo(self,wedget,data=None):
        if self.textview1.has_focus():
            if( not self.redo_queue1.empty()):
                text_in_queue = self.redo_queue1.get()
                buffer = self.textview1.get_buffer()
                start_iter, end_iter = buffer.get_bounds()
                text_in_view = buffer.get_text(start_iter, end_iter, True)
                buffer.set_text(text_in_queue)
                self.undo_queue1.put(text_in_view)
        elif self.textview2.has_focus():
            if( not self.redo_queue2.empty()):
                text_in_queue = self.redo_queue2.get()
                buffer = self.textview2.get_buffer()
                start_iter, end_iter = buffer.get_bounds()
                text_in_view = buffer.get_text(start_iter, end_iter, True)
                buffer.set_text(text_in_queue)
                self.undo_queue2.put(text_in_view)

    #store values in undo buffer
    def push_text_to_undobuffer1(self, data1=None, data2=None, 
    data3=None, data4=None):
        print("Pushing to undo 1")
        buffer = self.textview1.get_buffer()
        start_iter, end_iter = buffer.get_bounds()
        text = buffer.get_text(start_iter, end_iter, True)
        self.undo_queue1.put(text)

    def push_text_to_undobuffer2(self, data1=None, data2=None, 
    data3=None, data4=None):
        print("Pushing to undo 2")
        buffer = self.textview2.get_buffer()
        start_iter, end_iter = buffer.get_bounds()
        text = buffer.get_text(start_iter, end_iter, True)
        self.undo_queue2.put(text)

    def quit(self,widget, data=None):
        self.destroy()
        Gtk.main_quit()

class MyAboutDialog(Gtk.AboutDialog):
    def __init__(self, parent):
        Gtk.AboutDialog.__init__(self, parent=parent)
    
        # Set the relevant properties of the about dialog
        self.set_program_name(
        "BRAILLE TRANSLATOR\n"
         "0.1\n" 
         "Braille Translator is a graphical user interface\n" 
         "which converts any language into Braille using Liblouis.\n"
         "Braille is a system of tactile communication "
         "which allows visually"
         "impaired people to read and write.\n\n"
         "Copyright(C) 2022-2023 GREESHNA SARATH "
         "<greeshnamohan001@gmail.com>\n\n"
         "Supervised by  Zendalona(2022-2023)\n\n"
         "This program is free software you can redistribute it and "
         "or modify\n"
         "it under the terms of GNU General Public License as published\n"
         " by the free software foundation either gpl3 of the license\n"
         "This program is distributed in the hope that it will be useful\n"
         "but without any warranty without even the implied warranty of\n"
         "merchantability or fitness for a particular purpose.\n" 
          "see the GNU General Public License for more details"
          )
        
        #self.set_version("")
        
        self.set_website_label("GNU General Public License,version 0.1" 
        "Visit BrailleTranslator Home page")
        
        self.set_website("http://wwww,zendalona.com//braille-translator")
        self.set_authors(["Greeshna Sarath"])
        self.set_documenters(["Greeshna Sarath"])
        self.set_artists(["Nalin Sathyan" ,"Dr.Saritha Namboodiri", 
        "Subha I N", "Bhavya P V", "K.Sathyaseelan"])  

class Find(Gtk.Window):
    def __init__ (self,textview):
        Gtk.Window.__init__(self, title="Find")
        
        self.textbuffer = textview.get_buffer();
        self.textview = textview;
                
        mark = self.textbuffer.get_insert()
        self.iter = self.textbuffer.get_iter_at_mark(mark)
        self.match_start = self.iter.copy()
        self.match_start.backward_word_start()
        self.match_end = self.iter.copy()
        self.match_end.forward_word_end()
        self.tag = self.textbuffer.create_tag(foreground = "Blue")
        self.vbox = Gtk.VBox()
        self.vbox2 = Gtk.VBox()
        self.entry = Gtk.Entry()
        
        #label
        label = Gtk.Label()
        label.set_text("Search for : ")
        label.set_mnemonic_widget(self.entry)

        hbox = Gtk.HBox()            
        hbox.pack_start(label,True,True,0)
        hbox.pack_start(self.entry,True,True,0)
        label.show()
        self.entry.show()
        hbox.set_hexpand(True)
        hbox.set_vexpand(False)
        self.vbox2.pack_start(hbox, True, True, 0)
        self.vbox.pack_start(self.vbox2, True, True, 0)
        self.context_label = Gtk.Label()
        self.vbox.pack_start(self.context_label, True, True, 0)
        
        # Buttons
        hbox2 = Gtk.HBox()

        button_next = Gtk.Button(label="Next")
        button_next.connect("clicked", self.find_next)
        hbox2.pack_start(button_next,True,True,0)

        button_previous = Gtk.Button(label="Previous")
        button_previous.connect("clicked", self.find_previous)        
        hbox2.pack_start(button_previous,True,True,0)

        button_close = Gtk.Button(label="Close")
        button_close.connect("clicked", self.close)
        hbox2.pack_start(button_close,True,True,0)

        self.vbox.pack_start(hbox2, True, True, 0)
        self.add(self.vbox)
        self.vbox.show_all()

    #close
    def close(self,widget,data=None):
        start,end = self.textbuffer.get_bounds()
        self.textbuffer.remove_all_tags(start,end)
        self.destroy()    

    def trim_context_text(self,text):
        """cut the line if it is too lengthy (more than 10 words)
        without rearranging existing lines. This will avoid the 
        resizing of spell window"""
        new_text = ""
        for line in text.split('\n'):
            if (len(line.split(' ')) > 10):
                new_line = ""
                pos = 1
                for word in line.split(" "):
                    new_line += word
                    pos += 1
                    if (pos % 10 == 0):
                        new_line += '\n'
                    else:
                        new_line += ' '

                new_text += new_line
                if (pos % 10 > 3):
                    new_text += '\n'
            else:
                new_text += line + '\n'
        return new_text
    
    #find_next
    def find_next(self,widget,data=None):
        self.find(True)

    #find_previous
    def find_previous(self,widget,data=None):
        self.find(False)        
       
    #find 
    def find(self,data):
        word = self.entry.get_text()
        start , end = self.textbuffer.get_bounds()
        if (data == True):
            self.match_start.forward_word_end()
            results = self.match_start.forward_search(word, 0, end)
        else:
            self.match_end.backward_word_start()
            results = self.match_end.backward_search(word, 0,start)
        
        if results:
            self.textbuffer.remove_all_tags(start,end)
            self.match_start, self.match_end = results
            self.textbuffer.place_cursor(self.match_start)
            self.textbuffer.apply_tag(
            self.tag,self.match_start, 
            self.match_end
            )
            self.textview.scroll_to_iter(
            self.match_start, 0.2, 
            use_align=False, xalign=0.5, yalign=0.5
            )
            sentence_start=self.match_start.copy()
            sentence_start.backward_sentence_start()
            sentence_end=self.match_start.copy()
            sentence_end.forward_sentence_end()
            sentence = self.textbuffer.get_text(
            sentence_start,
            sentence_end, True
            )
            self.context_label.set_text(self.trim_context_text(sentence))
            self.context_label.grab_focus()
        else:
            self.context_label.set_text("Word {0} Not found".format(word))
            self.context_label.grab_focus()

class FindAndReplace(Find):
    def __init__(self,textview):
        Find.__init__(self,textview)
        self.set_title("Find and Replace")
        self.replace_entry = Gtk.Entry()

        #label
        label = Gtk.Label()
        label.set_text("Replace with : ")
        label.set_mnemonic_widget(self.replace_entry)

        box = Gtk.HBox()            
        box.pack_start(label,True,True,0)
        box.pack_start(self.replace_entry,True,True,0)
        label.show()
        self.replace_entry.show()
        box.set_hexpand(True)
        box.set_vexpand(False)
        
        self.vbox2.pack_start(box,True,True,0)
        self.vbox2.show_all()

        # Buttons
        hbox2 = Gtk.HBox()

        button_replace = Gtk.Button(label="Replace")
        button_replace.connect("clicked", self.replace)
        hbox2.pack_start(button_replace,True,True,0)

        button_replace_all = Gtk.Button(label="Replace All")
        button_replace_all.connect("clicked", self.replace_all)        
        hbox2.pack_start(button_replace_all,True,True,0)

        self.vbox.pack_start(hbox2,True,True,0)
        self.vbox.show_all()
        
    #replace
    def replace(self,widget,data=None):
        replace_word = self.replace_entry.get_text()
        self.textbuffer.delete(self.match_start, self.match_end)
        self.textbuffer.insert(self.match_end,replace_word)
        self.match_start = self.match_end.copy()
        self.find(True)
    
    #replace_all
    def replace_all(self,widget,data=None):
        word = self.entry.get_text()
        replace_word = self.replace_entry.get_text()
        end = self.textbuffer.get_end_iter()
        while(True):
            self.match_start.forward_word_end()
            results = self.match_start.forward_search(word, 0, end)
            if results:
                self.match_start, self.match_end = results
                self.textbuffer.delete(self.match_start, self.match_end)
                self.textbuffer.insert(self.match_end,replace_word)
                self.match_start = self.match_end.copy()
            else:
                break


if __name__ == "__main__":
    win = BrailleTranslatorWindow()
    win.connect("destroy", Gtk.main_quit)

