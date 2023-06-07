import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, Pango
import louis


class MyWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Braille Translator")
        
        #for both text fields to be vertical and spacing between them

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        self.add(vbox)
        
     
        #create gtk menubar  and placed in top window
        
        menubar = Gtk.MenuBar()
        self.create_menu(menubar)
        vbox.pack_start(menubar, False, False, 0)
        
        
        about_menu_item = Gtk.MenuItem(label="About")
        about_menu_item.connect("activate", self.show_about_dialog)
        
        help_menu = Gtk.Menu()
        help_menu.append(about_menu_item)
        
        help_menu_item = Gtk.MenuItem(label="Help")
        help_menu_item.set_submenu(help_menu)
        
        menubar.append(help_menu_item)
        
        # Create the about dialog
        self.about_dialog = MyAboutDialog(self)
        
        
        
        #grid layout allows you to align and organize widgets in a structured manner.specify the position of each widget within the grid
        
        self.grid = Gtk.Grid()
        self.grid.set_column_spacing(8)
        vbox.pack_start(self.grid, True, True, 0)
        
        #create first textview for input text using gtk textview 

        self.textview1 = Gtk.TextView()
        
        # wrap mode determines how text content is wrapped and displayed within the widget. here,wrap mode allows you to control how long lines of text are displayed within the textview. 
        
        self.textview1.set_wrap_mode(Gtk.WrapMode.WORD_CHAR)
        
        #The theme store allows you to customize the visual appearance of your application.here used to create font color and background color of both textviews
        
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


        # Gtk.HBox is a container widget that arranges its child widgets horizontally in a single row.here toolbar set to horizontal box
        hbox1 = Gtk.HBox()
        hbox1.set_hexpand(True)
        hbox1.set_vexpand(False)
        
        label = Gtk.Label()
        label.set_text("Font ")
        self.font_button = Gtk.FontButton()
        self.font_button.connect("font-set", self.on_font_set, self.textview1)
        label.set_mnemonic_widget(self.font_button)
        hbox1.pack_start(label,False,True,0)
        hbox1.pack_start(self.font_button,False,True,0)
        
        fixed = Gtk.Fixed()
        hbox1.pack_start(fixed,True,True,0)
        
        
        self.font_color = "#ffffff"
        self.background_color = "#000000"
        
        label = Gtk.Label()
        label.set_text("Theme ")
        self.combobox_theme = Gtk.ComboBox()
        self.combobox_theme.set_model(self.theme_store)
        renderer_text = Gtk.CellRendererText()
        self.combobox_theme.pack_start(renderer_text, True)
        self.combobox_theme.add_attribute(renderer_text, "text", 0)
        self.combobox_theme.connect("changed", self.on_theme_changed, self.textview1)
        label.set_mnemonic_widget(self.combobox_theme)
        hbox1.pack_start(label,False,True,0)
        hbox1.pack_start(self.combobox_theme,False,True,0)

        fixed = Gtk.Fixed()
        hbox1.pack_start(fixed,True,True,0)


        scrolled_win1 = Gtk.ScrolledWindow()
        scrolled_win1.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.ALWAYS)
        scrolled_win1.add(self.textview1)
        scrolled_win1.set_size_request(500, 500)

        box1 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        box1.set_vexpand(True)
        box1.pack_start(hbox1, False, True, 0)
        box1.pack_start(scrolled_win1, True, True, 0)

        self.grid.attach(box1, 0, 0, 1, 1)

        self.textview2 = Gtk.TextView()
        self.textview2.set_wrap_mode(Gtk.WrapMode.WORD_CHAR)

        
        hbox2 = Gtk.HBox()
        hbox2.set_hexpand(True)
        hbox2.set_vexpand(False)
        
        label = Gtk.Label()
        label.set_text("Font ")
        self.font_button2 = Gtk.FontButton()
        self.font_button2.connect("font-set", self.on_font_set, self.textview2)
        label.set_mnemonic_widget(self.font_button2)
        hbox2.pack_start(label,False,True,0)
        hbox2.pack_start(self.font_button2,False,True,0)

        fixed = Gtk.Fixed()
        hbox2.pack_start(fixed,True,True,0)
        
        self.font_color = "#ffffff"
        self.background_color = "#000000"
        
        label = Gtk.Label()
        label.set_text("Theme ")
        self.combobox_theme2 = Gtk.ComboBox()
        self.combobox_theme2.set_model(self.theme_store)
        renderer_text2 = Gtk.CellRendererText()
        self.combobox_theme2.pack_start(renderer_text2, True)
        self.combobox_theme2.add_attribute(renderer_text2, "text", 0)
        self.combobox_theme2.connect("changed", self.on_theme_changed, self.textview2)
        label.set_mnemonic_widget(self.combobox_theme2)
        hbox2.pack_start(label,False,True,0)
        hbox2.pack_start(self.combobox_theme2,False,True,0)
        
        fixed = Gtk.Fixed()
        hbox2.pack_start(fixed,True,True,0)
        

        scrolled_win2 = Gtk.ScrolledWindow()
        scrolled_win2.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.ALWAYS)
        scrolled_win2.add(self.textview2)
        scrolled_win2.set_size_request(500, 500)

        box2 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        box2.set_vexpand(True)
        box2.pack_start(hbox2, False, True, 0)
        box2.pack_start(scrolled_win2, True, True, 0)

        self.grid.attach(box2, 1, 0, 1, 1)

        box1 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        self.grid.attach(box1, 0, 1, 1, 1)

        self.table_names = [(0, 'en-us-g1.ctb'), (1, 'hi-in-g1.ctb'), (2, 'ml-in-g1.ctb')]

        self.language_combo1 = Gtk.ComboBoxText()
        self.language_combo1.append_text("English")
        self.language_combo1.append_text("Hindi")
        self.language_combo1.append_text("Malayalam")
        self.language_combo1.set_active(0)
        self.language_combo1.set_size_request(225, 40)
        self.language_combo1.connect("changed", self.on_combo_changed)
        box1.pack_start(self.language_combo1, False, False, 0)

        self.translate_button = Gtk.Button(label="Translate")
        self.translate_button.connect("clicked", self.on_translate_clicked)
        box1.pack_end(self.translate_button, False, False, 0)
        self.translate_button.set_size_request(225, 40)
        
        

    def create_menu(self, menubar):

        # Create the "File" menu
        file_menu = Gtk.Menu()
        
     
        new_item = Gtk.MenuItem.new_with_label("New")
        new_item.connect("activate", self.on_new_activated)
        file_menu.append(new_item)

        open_item = Gtk.MenuItem.new_with_label("Open")
        open_item.connect("activate", self.on_open_activated)
        file_menu.append(open_item)

        save_item = Gtk.MenuItem.new_with_label("Save")
        save_item.connect("activate", self.on_save_activated)
        file_menu.append(save_item)

        save_as_item = Gtk.MenuItem.new_with_label("Save As")
        save_as_item.connect("activate", self.on_save_as_activated)
        file_menu.append(save_as_item)

        file_menu_item = Gtk.MenuItem.new_with_label("File")
        file_menu_item.set_submenu(file_menu)

        # Create the "Edit" menu
        edit_menu = Gtk.Menu()

        cut_item = Gtk.MenuItem.new_with_label("Cut")
        cut_item.connect("activate", self.on_cut_activated)
        edit_menu.append(cut_item)

        copy_item = Gtk.MenuItem.new_with_label("Copy")
        copy_item.connect("activate", self.on_copy_activated)
        edit_menu.append(copy_item)

        paste_item = Gtk.MenuItem.new_with_label("Paste")
        paste_item.connect("activate", self.on_paste_activated)
        edit_menu.append(paste_item)
        
        goto_item = Gtk.MenuItem(label="Goto Line")
        edit_menu.append(Gtk.SeparatorMenuItem())
        edit_menu.append(goto_item)
         # Connect Goto Line menu item to callback function
        goto_item.connect("activate", self.on_goto_line_activate)

        

        edit_menu_item = Gtk.MenuItem.new_with_label("Edit")
        edit_menu_item.set_submenu(edit_menu)
        
        
        
        # Add menu items to the menubar
        menubar.append(file_menu_item)
        menubar.append(edit_menu_item)

    def on_new_activated(self, widget): 
		
        # Clear the active text view and set focus to it
        if self.textview1.has_focus():
            self.textview1.get_buffer().set_text("")
            self.textview1.focus()
        elif self.textview2.has_focus():
            self.textview2.get_buffer().set_text("")
            self.textview2.focus()
        else:
            # Clear data in both text fields
            self.textview1.get_buffer().set_text("")
            self.textview2.get_buffer().set_text("")
            

    def on_open_activated(self, widget):

        dialog = Gtk.FileChooserDialog(title="Open", parent=self, action=Gtk.FileChooserAction.OPEN)
        dialog.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK)
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            filename = dialog.get_filename()
        
            # Determine the focused text view and load the file there
            focused_textview = self.get_focus()
            if focused_textview == self.textview1:
                self.load_text(filename, self.textview1)
            elif focused_textview == self.textview2:
                self.load_text(filename, self.textview2)
        
        dialog.destroy()


    def load_file(self, filename):
        # Load the contents of the file and set it to the active text view
        if self.textview1.has_focus():
            self.load_text(filename, self.textview1)
        elif self.textview2.has_focus():
            self.load_text(filename, self.textview2)

    def load_text(self, filename, textview):
        with open(filename, "r") as file:
            text = file.read()
            buffer = textview.get_buffer()
            buffer.set_text(text)
            
    def on_save_activated(self, widget):
        dialog = Gtk.FileChooserDialog(title="Save",parent=self,action=Gtk.FileChooserAction.SAVE,buttons=(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_SAVE, Gtk.ResponseType.OK),)
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
    
            
    def on_save_as_activated(self, widget):
        dialog = Gtk.FileChooserDialog(title="Save As",parent=self,action=Gtk.FileChooserAction.SAVE,buttons=(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_SAVE, Gtk.ResponseType.OK),)
        dialog.set_do_overwrite_confirmation(True)
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            filename = dialog.get_filename()
            self.save_file(filename)

        dialog.destroy()
        
    def save_as_file(self, filename):
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
            
    def on_paste_activated(self, widget):
        # Get the focused text view
        focused_textview = self.get_focus()

        # Get the buffer of the focused text view
        buffer = focused_textview.get_buffer()

        # Get the clipboard content
        clipboard = Gtk.Clipboard.get_default(self.get_window().get_display())
        text = clipboard.wait_for_text()

        # Insert the clipboard content at the cursor position
        if text:
            # Get the cursor position in the buffer
            cursor_iter = buffer.get_iter_at_mark(buffer.get_insert())

            # Insert the clipboard content at the cursor position
            buffer.insert(cursor_iter, text)
    
            
            
            
            
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
            # Get the current line number based on the mouse cursor position
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
                active_textview.scroll_to_iter(line_iter, 0.0, True, 0.5, 0.5)

        dialog.destroy()

    def get_active_textview(self):
        focus = self.get_focus()
        if focus == self.textview1:
            return self.textview1
        elif focus == self.textview2:
            return self.textview2
        else:
            return None

    
    
    
    def show_about_dialog(self, widget):
        self.about_dialog.run()
        self.about_dialog.hide()
    
    
    def on_combo_changed(self, combo):
        language_id = combo.get_active()
        language_file = self.table_names[language_id][1]
        louis.translateStringToFile(language_file, self.textview1.get_buffer(), self.textview2.get_buffer())


    def on_translate_clicked(self, button):  #write button or widget
        
        # Rest of the code...
        buffer1 = self.textview1.get_buffer()
        text1 = ""

        # Check if any text is selected in the text view
        if buffer1.get_has_selection():
            # Get the selected text range
            start_iter, end_iter = buffer1.get_selection_bounds()

            # Extract the selected text
            text1 = buffer1.get_text(start_iter, end_iter, True)
        else:
            text1 = buffer1.get_text(buffer1.get_start_iter(), buffer1.get_end_iter(), True)

        # Get the index of the selected language in the combo box
        c = self.language_combo1.get_active()

        # Select the corresponding table based on the index
        if c == 0:  # English
            table = ['unicode.dis', 'en-us-g1.ctb']
        elif c == 1:  # Hindi
            table = ['unicode.dis', 'hi-in-g1.ctb']
        elif c == 2:  # Malayalam
            table = ['unicode.dis', 'ml-in-g1.ctb']

        # Get the cursor position in the second text view
        buffer2 = self.textview2.get_buffer()
        cursor_mark = buffer2.get_insert()
        cursor_iter = buffer2.get_iter_at_mark(cursor_mark)
        cursor_position = cursor_iter.get_offset()

        # Get the existing text in the second text view
        existing_text = buffer2.get_text(buffer2.get_start_iter(), buffer2.get_end_iter(), True)

        # Translate the text to Braille using the selected table
        braille = louis.translate(table, text1)

        # Set the text of the second text view to the Braille translation
        buffer2.set_text(existing_text + braille[0])

        # Restore the cursor position in the second text view
        if cursor_position <= len(buffer2.get_text(buffer2.get_start_iter(), buffer2.get_end_iter(), True)):
            cursor_iter = buffer2.get_iter_at_offset(cursor_position)
            buffer2.place_cursor(cursor_iter)
            
            

    def set_cursor_color(self, textview, color):
	    colors_in_float = Gdk.color_parse(color).to_floats()
	    cursor_color_hex = "#" + "".join(["%02x" % (int(color * 255)) for color in colors_in_float])
		
	    try:
		    cssProvider = Gtk.CssProvider()
		    cssProvider.load_from_data((" * {   caret-color: "+cursor_color_hex+";    }").encode('ascii'))
		
		    style = textview.get_style_context()
		    style.add_provider(cssProvider, Gtk.STYLE_PROVIDER_PRIORITY_USER)
	    except:
		    print("Unnable to set cursor color!")

    def set_selection_color(self, textview, font_color, background_color):
	    color1 = Gdk.color_parse(font_color)
	    color2 = Gdk.color_parse(background_color)
	    
	    selection_color = Gdk.Color((color1.red + color2.red)/2, (color1.green + color2.green)/2 ,(color1.blue + color2.blue)/2)
	    
	    selection_colors_in_float = selection_color.to_floats()
	    
	    selection_background_colors_in_float = color2.to_floats()
	    
	    selection_color_hex = "#" + "".join(["%02x" % (int(color * 255)) for color in selection_colors_in_float])
	    
	    selection_background_color_hex = "#" + "".join(["%02x" % (int(color * 255)) for color in selection_background_colors_in_float])
	    
	    try:
		    cssProvider = Gtk.CssProvider()
		    cssProvider.load_from_data((" * selection { color: "+selection_color_hex+";  background: "+selection_background_color_hex+";}").encode('ascii'))
		
		    style = textview.get_style_context()
		    style.add_provider(cssProvider, Gtk.STYLE_PROVIDER_PRIORITY_USER)
	    except:
		    print("Unnable to set selection color!")

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
		    textview.modify_fg(Gtk.StateFlags.NORMAL, Gdk.color_parse(font_color))
		    textview.modify_bg(Gtk.StateFlags.NORMAL, Gdk.color_parse(background_color ))
	    self.set_cursor_color(textview, font_color)
	    self.set_selection_color(textview, font_color, background_color)


    def on_font_set(self,widget, textview):
	    font = widget.get_font_name();
	    pangoFont = Pango.FontDescription(font)
	    textview.modify_font(pangoFont)
	    

class MyAboutDialog(Gtk.AboutDialog):
    def __init__(self, parent):
        Gtk.AboutDialog.__init__(self, parent=parent)
    
        # Set the relevant properties of the about dialog
        self.set_program_name("BRAILLE TRANSLATOR\n 0.1 \n\nBraille Translator is a graphical user interface \n which converts any language into Braille using Liblouis.\n Braille is a system of tactile communication which allows visually impaired people to read and write.  \n\n   Copyright(C) 2022-2023 GREESHNA SARATH <greeshnamohan001@gmail.com>\n\n   Supervised by  Zendalona(2022-2023)\n\n This program is free software you can redistribute it and or modify \nit under the terms of GNU General Public License as published by the free software foundation \n either gpl3 of the license.This program is distributed in the hope that it will be useful,\n but without any warranty without even the implied warranty of merchantability or fitness for a particular purpose.\n see the GNU General Public License for more details") 
        
        #self.set_version("")
        
        self.set_website_label("GNU General Public License,version 0.1\n\n" "Visit BRAILLE TRANSLATOR Home page")
        
        self.set_website("http://wwww,zendalona.com//BRAILLE-TRANSLATOR")
        self.set_authors(["Greeshna Sarath"])
        self.set_documenters(["Greeshna Sarath"])
        self.set_artists(["Nalin Sathyan" ,"Dr.Saritha Namboodiri", "Subha I N", "Bhavya P V", "K.Sathyaseelan"])  


win = MyWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()