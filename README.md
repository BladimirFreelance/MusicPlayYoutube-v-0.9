This is a software project for Windows that plays YouTube broadcasts in the background. As the project evolves, new features and code will be added. This is an update to the pilot version.

Version 0.9

Changes:
Added a window for modifying and adding channels, which can be accessed by right-clicking on the application icon.
I will also release a compiled version with an installer that includes everything necessary for the application to work. Install and enjoy.

The program itself remains minimized in the system tray without any control elements. By right-clicking on the icon, you can access the exit menu, terminate the program, or open the Channels window to configure or add your own. It includes a database file of pre-set channels.

Open source information:
A database has been added. The code will create a database file named "channels.db" if it doesn't exist and will add a default link and name.

To add your own icon in the main.py code, you need to change the line self.tray_icon.setIcon(QtGui.QIcon(resource_path("YourIcon.png"))). The file with your icon should be located in the same directory as the main.py file.
Added the file channels_window.py, which is the window for selecting and changing channels.

It's also important to install all dependencies before compiling:
A key dependency is pip install yt-dlp, which needs to be executed in the terminal.

To compile into an executable file, use the command: pyinstaller -F --icon=favicon.ico --noconsole --add-data "design.png;." --add-data "green_circle.png;." --add-data "red_circle.png;." --add-data "left.png;." --add-data "right.png;." --add-data "play.png;." --add-data "stop.png;." main.py, and also install VLC Media Player from the official website on your computer.

Development and testing were conducted in the PyCharm environment.
