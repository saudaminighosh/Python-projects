from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from kivy.uix.checkbox import CheckBox
import mysql.connector
import re
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.gridlayout import GridLayout
#from KivyCalendar import CalendarWidget
from kivymd.uix.picker import MDDatePicker




class afterLogin(Screen):
    def __init__(self,app_instance,**kwargs):
        super().__init__(name='after_login',**kwargs)
        self.layout=FloatLayout()
        self.add_widget(self.layout)
        # Store the app instance
        self.app=app_instance
        self.l6=Label(text='[color=638C6D]Tim - The Tinnitus Tracker',font_size=40,markup=True,pos_hint={'center_x':0.5,'center_y':0.9})
        self.layout.add_widget(self.l6)
        self.l1=Label(text='[color=638C6D]Hello',font_size=40,markup=True,pos_hint={'center_x':0.5,'center_y':0.8})
        self.layout.add_widget(self.l1)
        self.logout=Button(text='[b]Logout[/b]',markup=True, font_size=30,size_hint=(.1,.07),pos_hint={'center_x':0.1,'center_y':0.9},background_color='#638C6D')
        self.logout.bind(on_press=self.logout2)
        self.layout.add_widget(self.logout)
        self.log_tinnitus_button=Button(text='[b]Log Tinnitus[/b]',markup=True, font_size=30,size_hint=(.1,.07),pos_hint={'center_x':0.5,'center_y':0.5},background_color='#638C6D')
        self.log_tinnitus_button.bind(on_press=self.calender_display)
        self.layout.add_widget(self.log_tinnitus_button)

    def on_pre_enter(self, *args):
        # Retrieve the username from the main App class and update the label
        username = self.app.current_user
        if username:
            self.l1.text=f'[color=638C6D]Hello , {username} !![/color]'
        else:
            self.l1.text='[color=638C6D]Hello !![/color]'
    def logout2(self, *args):
        # This switches the ScreenManager's current screen to 'login_page'
        self.app.current_user = "" 
        self.manager.current = 'login_page'

    def calender_display(self, *args):
        self.manager.current = 'calender_display_page'

class CalendarScreen(Screen):
    def __init__(self, app_instance, **kwargs):
        super().__init__(name='calender_page',**kwargs)
        self.app = app_instance
        self.layout = FloatLayout()
        self.add_widget(self.layout)
        # 1. Title/User Label
        self.title_label = Label(text="Loading Calendar...", font_size=30,pos_hint={'center_x': 0.5, 'center_y': 0.95})
        self.layout.add_widget(self.title_label)
        # 2. 💡 KivyCalendar Widget Implementation
        # The CalendarWidget handles the grid and date display internally
        self.calendar_label = Label(text="Tap to select and mark a date", size_hint=(0.5, 0.1), pos_hint={'center_x': 0.5, 'center_y': 0.5},font_size=30)
        self.layout.add_widget(self.calendar_label)
        # 3. Save Button (for testing marking functionality)
        #self.save_button = Button(text="Mark Selected Date",size_hint=(0.25, 0.07),pos_hint={'center_x': 0.85, 'center_y': 0.95},on_press=self.mark_current_date)
        #self.layout.add_widget(self.save_button)
        self.mark_date_button = Button(text="Open Calendar & Mark Date",size_hint=(0.4, 0.07),pos_hint={'center_x': 0.5, 'center_y': 0.1},on_press=self.show_date_picker)
        self.layout.add_widget(self.mark_date_button)
    
    def show_date_picker(self, instance):
        # Create and open the KivyMD DatePicker
        date_dialog = MDDatePicker()
        
        # Bind the dialog's dismiss (OK button press) event to your save function
        date_dialog.bind(on_save=self.on_date_save)
        
        # This shows the popup calendar
        date_dialog.open()

    def on_date_save(self, instance, date_obj, date_range):
        """Called when a date is selected and the user presses 'OK'."""
        date_str = date_obj.strftime('%Y-%m-%d')
        username = self.app.current_user

        # 1. Save the mark to the database
        if self.app.save_calendar_mark(username, date_str):
            self.calendar_label.text = f"Marked {date_str} successfully!"
            print(f"Marked date {date_str} for user {username}")
        else:
            self.calendar_label.text = "Failed to save mark."
            print("Failed to save mark.")

    def on_pre_enter(self, *args):
        username = self.app.current_user
        self.title_label.text = f"Calendar for {username}"
        
        # Load the marked dates from the database
        self.load_user_calendar_marks(username)

    def load_user_calendar_marks(self, username):
        # Fetch marks from DB (e.g., list of date strings 'YYYY-MM-DD')
        marks_data = self.app.get_calendar_marks(username) 
        # For simplicity, just log them:
        print(f"Loaded {len(marks_data)} marked dates for {username}.")
        # Extract only the date string for marking
        marked_dates = [mark[0].strftime('%Y-%m-%d') for mark in marks_data]

        # 💡 Set the marked dates on the CalendarWidget
        # The CalendarWidget typically uses a property called 'marked_dates' 
        # or similar to highlight dates passed to it.
        try:
            # Assuming KivyCalendar has a method or property for this:
            self.calendar_widget.marked_dates = marked_dates
            # You might need to call a refresh method depending on the exact version
            if hasattr(self.calendar_widget, 'update_calendar'):
                self.calendar_widget.update_calendar()
        except AttributeError as e:
            print(f"CalendarWidget version does not support direct marked_dates property: {e}")
            # Fallback or specific version handling required here

    def mark_current_date(self, instance):
        # 1. Get the currently selected date from the CalendarWidget
        try:
            selected_date = self.calendar_widget.active_date  # Common property name
            # Format the date object to the 'YYYY-MM-DD' string needed for MySQL
            date_str = selected_date.strftime('%Y-%m-%d')
        except AttributeError:
            print("Could not retrieve active date from CalendarWidget.")
            return
        username = self.app.current_user
        # 2. Save the mark to the database
        if self.app.save_calendar_mark(username, date_str):
            print(f"Marked date {date_str} for user {username}")
            # 3. Reload the marks to update the calendar display immediately
            self.load_user_calendar_marks(username)
        else:
            print("Failed to save mark.")

    def logout2(self, *args):
        # Add back button/logout logic to switch screens
        self.app.current_user = "" 
        self.manager.current = 'login_page'


class afterSignUp(Screen):
    def __init__(self, **kwargs):
        super().__init__(name='after_signup',**kwargs)
        self.layout=FloatLayout()
        self.add_widget(self.layout)
        self.l3=Label(text='[color=638C6D][b]Account created !![/b]',font_size=40,markup=True,pos_hint={'center_x':0.5,'center_y':0.6})
        self.layout.add_widget(self.l3)
        self.back_to_login_button=Button(text='[b]Back to login Page[/b]',markup=True, font_size=30,size_hint=(.1,.07),pos_hint={'center_x':0.5,'center_y':0.5},background_color='#638C6D')
        self.back_to_login_button.bind(on_press=self.logout2)
        self.logout=Button(text='[b]Logout[/b]',markup=True, font_size=30,size_hint=(.1,.07),pos_hint={'center_x':0.1,'center_y':0.9},background_color='#638C6D')
        self.logout.bind(on_press=self.logout2)
        self.layout.add_widget(self.logout)
    def logout2(self, *args):
        # This switches the ScreenManager's current screen to 'login_page'
        self.manager.current = 'login_page'

class LoginScreen(Screen):
    def __init__(self, app_instance, **kwargs):
        super().__init__(name='login_page', **kwargs)
        # Store a reference to the main App class to call its methods (like sign and log)
        self.app = app_instance
        # Define the main layout for this screen
        self.window = FloatLayout()
        self.add_widget(self.window) # This FloatLayout is the content of the LoginScreen
        # Initialize all widgets to None (as you did in your original build)
        self.l1 = self.l2 = self.l3 = self.l4 = self.l5 = self.l6 = self.l7 = self.l8 = None
        self.login = self.signup = self.login3 = self.signup2 = self.backButton = self.logout = None
        self.input1 = self.input2 = self.input3 = None
        self.check = self.warning = None
        # Call the initial front page setup
        self.front_page(None)

    def front_page(self, x):
        # Clear all previous widgets
        self.window.clear_widgets()
        # Your original front_page logic to build the initial screen
        self.l1 = Label(text='[color=638C6D][b]Welcome ![/b]',font_size=70,markup=True,pos_hint={'center_x':0.5,'center_y':0.7})
        self.window.add_widget(self.l1)
        self.login = Button(text='[b]Login[/b]',markup=True, font_size=40,size_hint=(.2,.1),pos_hint={'center_x':0.5,'center_y':0.55},background_color='#638C6D')
        self.login.bind(on_press=self.login2)
        self.window.add_widget(self.login)
        self.l2 = Label(text='[color=638C6D][b]OR[/b]',font_size=45,markup=True,pos_hint={'center_x':0.5,'center_y':0.45})
        self.window.add_widget(self.l2)
        self.signup = Button(text='[b]Sign Up[/b]',markup=True, font_size=40,size_hint=(.2,.1),pos_hint={'center_x':0.5,'center_y':0.35},background_color='#638C6D')
        self.signup.bind(on_press=self.register)
        self.window.add_widget(self.signup)

    def register(self, x):
        self.window.clear_widgets()
        # Re-build the register screen UI (simplified for brevity, use your full original code)
        self.backButton=Button(text='[b]Back to Login Page[/b]',markup=True, font_size=20,size_hint=(.18,.05),pos_hint={'center_x':0.1,'center_y':0.9},background_color='#638C6D')
        self.backButton.bind(on_press=self.front_page)
        self.window.add_widget(self.backButton)
        
        self.l3=Label(text='[color=638C6D][b]Enter Username:[/b]',font_size=45,markup=True,pos_hint={'center_x':0.3,'center_y':0.7})
        self.window.add_widget(self.l3)
        self.input1=TextInput(multiline=False, padding_y=(30,30), size_hint=(0.4, 0.1),pos_hint={"center_x": 0.7, "center_y": 0.7}, font_size=30)
        self.window.add_widget(self.input1)
        
        # ... add all other register widgets (l4, input2, check, l5, l7, input3, l8)
        self.l4=Label(text='[color=638C6D][b]Enter Password:[/b]',font_size=45,markup=True,pos_hint={'center_x':0.3,'center_y':0.59})
        self.window.add_widget(self.l4)
        self.input2=TextInput(multiline=False, padding_y=(30,30), size_hint=(0.4, 0.1),pos_hint={"center_x": 0.7, "center_y": 0.57}, font_size=30, password=True)
        self.window.add_widget(self.input2)
        self.check = CheckBox(size_hint=(0.1,0.1),pos_hint={"center_x": 0.51, "center_y": 0.49},color='#000000')
        self.check.bind(active=self.on_checkbox_active)
        self.window.add_widget(self.check)
        self.l5=Label(text='[color=000000]Show Password',font_size=25,markup=True,pos_hint={'center_x':0.6,'center_y':0.49})
        self.window.add_widget(self.l5)
        self.l7=Label(text='[color=638C6D][b]Re-Enter Password:[/b]',font_size=45,markup=True,pos_hint={'center_x':0.3,'center_y':0.41})
        self.window.add_widget(self.l7)
        self.input3=TextInput(multiline=False, padding_y=(30,30), size_hint=(0.4, 0.1),pos_hint={"center_x": 0.7, "center_y": 0.39}, font_size=30, password=True)
        self.window.add_widget(self.input3)
        #self.signup2=Button(text='[b]Signup[/b]',markup=True, font_size=40,size_hint=(.2,.1),pos_hint={'center_x':0.5,'center_y':0.1},background_color='#638C6D')
        #self.signup2.bind(on_press=self.sign)
        #self.window.add_widget(self.signup2)
        self.l8=Label(text='[color=4C585B]-Username must contain only alphabets & numbers\n-Username length must be greater than 3 and less than 11\n-Password length must be greater than 5 and less than 13\n-Password must contain atleast 1 uppercase letter, 1 lowercase letter,\n1 digit and atleast one of these characters {!,@,#,$,%,^,&,*}',font_size=16,markup=True,pos_hint={'center_x':0.22,'center_y':0.21})
        self.window.add_widget(self.l8)

        self.signup2=Button(text='[b]Signup[/b]',markup=True, font_size=40,size_hint=(.2,.1),pos_hint={'center_x':0.5,'center_y':0.1},background_color='#638C6D')
        # Call the App's sign logic, passing the inputs
        self.signup2.bind(on_press=lambda *args: self.app.sign(
            self.input1.text, self.input2.text, self.input3.text, self.warning
        ))
        self.window.add_widget(self.signup2)
        
        # The App's sign method must update the warning label
        self.warning = Label(text='', font_size=30, markup=True, pos_hint={'center_x': 0.5, 'center_y': 0.30})
        self.window.add_widget(self.warning)
        
    def login2(self, x):
        self.window.clear_widgets()
        # Re-build the login screen UI (simplified for brevity)
        self.backButton=Button(text='[b]Back to Signup Page[/b]',markup=True, font_size=20,size_hint=(.18,.05),pos_hint={'center_x':0.1,'center_y':0.9},background_color='#638C6D')
        self.backButton.bind(on_press=self.front_page)
        self.window.add_widget(self.backButton)
        
        self.l3=Label(text='[color=638C6D][b]Enter Username:[/b]',font_size=45,markup=True,pos_hint={'center_x':0.3,'center_y':0.7})
        self.window.add_widget(self.l3)
        self.input1=TextInput(multiline=False, padding_y=(30,30), size_hint=(0.4, 0.1),pos_hint={"center_x": 0.7, "center_y": 0.7}, font_size=30)
        self.window.add_widget(self.input1)
        
        self.l4=Label(text='[color=638C6D][b]Enter Password:[/b]',font_size=45,markup=True,pos_hint={'center_x':0.3,'center_y':0.59})
        self.window.add_widget(self.l4)
        self.input2=TextInput(multiline=False, padding_y=(30,30), size_hint=(0.4, 0.1),pos_hint={"center_x": 0.7, "center_y": 0.57}, font_size=30, password=True)
        self.window.add_widget(self.input2)
        
        # ... add other login widgets (checkbox, l5)
        self.check = CheckBox(size_hint=(0.1,0.1),pos_hint={"center_x": 0.51, "center_y": 0.49},color='#000000')
        self.check.bind(active=self.on_checkbox_active)
        self.window.add_widget(self.check)
        self.l5=Label(text='[color=000000]Show Password',font_size=25,markup=True,pos_hint={'center_x':0.6,'center_y':0.49})
        self.window.add_widget(self.l5)

        self.login3=Button(text='[b]Login[/b]',markup=True, font_size=40,size_hint=(.2,.1),pos_hint={'center_x':0.5,'center_y':0.1},background_color='#638C6D')
        # Call the App's log logic, passing the inputs
        self.login3.bind(on_press=lambda *args: self.app.log(
            self.input1.text, self.input2.text, self.warning
        ))
        self.window.add_widget(self.login3)

        # The App's log method must update the warning label
        self.warning = Label(text='', font_size=30, markup=True, pos_hint={'center_x': 0.5, 'center_y': 0.30})
        self.window.add_widget(self.warning)

    # Note: Keep the on_checkbox_active method here as it only affects input2
    def on_checkbox_active(self, check, value):
        # ... (your original logic) ...
        if value:
            self.input2.password=False
        else:
            self.input2.password=True
    
    def on_pre_enter(self):
        # Ensure the front page is displayed when coming back from 'afterLogin'
        self.front_page(None)    

class Chat(App):
    #user=[]
    #pas=[]
    def build(self):
        #self.l6=None
        #self.warning = None
        self.user = []
        self.pas = []
        self.current_user = ""
        Window.clearcolor='#D9DFC6'

        # 1. Create the ScreenManager
        self.sm = ScreenManager()

        # 2. Create the LoginScreen and AfterLoginScreen
        self.login_screen = LoginScreen(app_instance=self)
        self.after_login_screen = afterLogin(app_instance=self)
        self.after_signup_screen= afterSignUp()
        self.calender_screen= CalendarScreen(app_instance=self)

        # 3. Add the screens to the manager
        self.sm.add_widget(self.login_screen)
        self.sm.add_widget(self.after_login_screen)
        self.sm.add_widget(self.after_signup_screen)
        self.sm.add_widget(self.calender_screen)
        
        # 4. Set the initial screen
        self.sm.current = 'login_page'

        # Your database connection setup (keep it simple in build)
        self._setup_database()
        return self.sm

    def _setup_database(self):
        # Define database
        mydb = mysql.connector.connect(
            host='localhost',
            user='root',
            passwd='password123'
        )
        c = mydb.cursor()
        c.execute("CREATE DATABASE IF NOT EXISTS chat_app")
        c.execute("USE chat_app")
        c.execute("""CREATE TABLE if not exists customers(name VARCHAR(50) PRIMARY KEY, password VARCHAR(50))""")
        c.execute("""
        CREATE TABLE if not exists calendar_marks(
            username VARCHAR(50),
            marked_date DATE,
            comment VARCHAR(255),
            PRIMARY KEY (username, marked_date),
            FOREIGN KEY (username) REFERENCES customers(name))""")
        mydb.commit()
        mydb.close()

        '''mydb=mysql.connector.connect(
            host='localhost',
            user='root',
            passwd='password123'
        )
        #Create cursor for Database
        c=mydb.cursor()
        
        #Create an actual DB
        c.execute("CREATE DATABASE IF NOT EXISTS chat_app")
        
        #Check to see if DataBase works
        #c.execute("SHOW DATABASES")
        
        #for db in c:
        #    print(db)
        
        
        #Create a table
        
        c.execute("USE chat_app")
        c.execute("""CREATE TABLE if not exists customers(name VARCHAR(50), password VARCHAR(50))""")
        mydb.commit()
        mydb.close()'''
        
        '''self.l1=Label(text='[color=638C6D][b]Welcome ![/b]',font_size=70,markup=True,pos_hint={'center_x':0.5,'center_y':0.7})
        self.window.add_widget(self.l1)
        self.login=Button(text='[b]Login[/b]',markup=True, font_size=40,size_hint=(.2,.1),pos_hint={'center_x':0.5,'center_y':0.55},background_color='#638C6D')
        self.login.bind(on_press=self.login2)
        self.window.add_widget(self.login)
        self.l2=Label(text='[color=638C6D][b]OR[/b]',font_size=45,markup=True,pos_hint={'center_x':0.5,'center_y':0.45})
        self.window.add_widget(self.l2)
        self.signup=Button(text='[b]Sign Up[/b]',markup=True, font_size=40,size_hint=(.2,.1),pos_hint={'center_x':0.5,'center_y':0.35},background_color='#638C6D')
        self.signup.bind(on_press=self.register)
        self.window.add_widget(self.signup)'''

    # Sign method adapted to accept parameters and update the warning label
    def sign(self, username, password, re_password, warning_label):
        # --- Your original validation logic goes here ---
        # ... (Your flags and regex checks) ...
        #flag1 = 0
        #flag2 = 0
        
        if len(username) == 0:
            warning_label.text = '[color=FF0000]Username is empty ! Please Try Again'
            return
    
        if len(password) == 0:
            warning_label.text = '[color=FF0000]Password is empty ! Please Try Again'
            return

        if len(re_password) == 0:
            warning_label.text = '[color=FF0000]Please Re-enter the password'
            return
    
        if password != re_password:
            warning_label.text = '[color=FF0000]Passwords are not matching ! Please Try Again'
            return
        
        is_valid_credentials = True

        # Check Lengths
        if not (4 <= len(username) <= 15 and 6 <= len(password) <= 12):
            is_valid_credentials = False

        # Check Username format (alphabets, numbers, or underscore)
        if is_valid_credentials:
            if not re.match("^[a-zA-Z0-9_]+$", username):
                is_valid_credentials = False

        # Check Password complexity
        if is_valid_credentials:
            lc = re.search("[a-z]", password)
            uc = re.search("[A-Z]", password)
            num = re.search("[0-9]", password)
            # Check for special characters: !, @, #, $, %, ^, &, *
            sc = re.search("[!@#$%^&*_]", password)

            # Check for spaces (your original code checked for spaces and broke validation)
            if re.search(r"\s", password):
                is_valid_credentials = False
        
            if not (lc and uc and num and sc):
                is_valid_credentials = False

        # If credentials fail any checks
        if not is_valid_credentials:
            warning_label.text = '[color=FF0000]Credentials are not valid ! Please Try Again'
            return
        
        # --- Database Check for Existing User ---
        try:
            mydb = mysql.connector.connect(
            host='localhost', user='root', passwd='password123', database='chat_app')
            c = mydb.cursor()
        
            # Check if username already exists
            sql_command = "SELECT name FROM customers WHERE customers.name=%s"
            c.execute(sql_command, (username,))
            rec = c.fetchall()
        
            if rec:
                warning_label.text = '[color=FF0000]Username is already taken ! Please Try with a Different one'
                mydb.close()
                return
            
            # --- Insert into Database (If all checks pass) ---
            sql_command = "INSERT INTO customers (name,password) VALUES (%s,%s)"
            c.execute(sql_command, (username, password))
            mydb.commit()
        
            # Update app's temporary lists (optional, if you still rely on them)
            self.user.append(username)
            self.pas.append(password)

            mydb.close()
            self.current_user = username
            # Clear any previous warning and switch to the next screen
            warning_label.text = ''
            self.sm.current = 'after_signup'

        except mysql.connector.Error as err:
            # Handle database connection or execution errors
            warning_label.text = f'[color=FF0000]Database Error: {err}'
            if 'mydb' in locals() and mydb.is_connected():
                mydb.close()

    # Log method adapted to accept parameters and update the warning label
    def log(self, username, password, warning_label):
        if not username:
            warning_label.text = '[color=FF0000]Username is empty !'
            return
        if not password:
            warning_label.text = '[color=FF0000]Password is empty !'
            return

        mydb = mysql.connector.connect(
            host='localhost', user='root', passwd='password123', database='chat_app'
        )
        c = mydb.cursor()
        
        # Check if username exists
        sql_command = "SELECT password FROM customers WHERE customers.name=%s"
        c.execute(sql_command, (username,))
        rec = c.fetchone()
        
        if not rec:
            warning_label.text = '[color=FF0000]Username is not registered. Please sign in first.'
        elif rec[0] == password:
            # Login Success! Change the screen
            self.current_user = username
            self.sm.current = 'after_login'
        else:
            warning_label.text = '[color=FF0000]Wrong Password. Please try again.'

        mydb.close()

    def get_calendar_marks(self, username):
        #Fetches all marked dates and comments for the current user.
        try:
            mydb = mysql.connector.connect(
                host='localhost', user='root', passwd='password123', database='chat_app')
            c = mydb.cursor()
            
            sql = "SELECT marked_date, comment FROM calendar_marks WHERE username = %s"
            c.execute(sql, (username,))
            marks = c.fetchall()
            
            mydb.close()
            # Returns a list of tuples: [(date_obj, 'comment'), ...]
            return marks
        except mysql.connector.Error as err:
            print(f"Error retrieving calendar marks: {err}")
            return []
        
    def save_calendar_mark(self, username, date_str, comment=""):
        """Saves a single marked date for the current user."""
        try:
            mydb = mysql.connector.connect(
                host='localhost', user='root', passwd='password123', database='chat_app')
            c = mydb.cursor()
            
            sql = "INSERT INTO calendar_marks (username, marked_date, comment) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE comment = %s"
            values = (username, date_str, comment, comment)
            c.execute(sql, values)
            
            mydb.commit()
            mydb.close()
            return True
        except mysql.connector.Error as err:
            print(f"Error saving calendar mark: {err}")
            return False
        
    # No need for separate logSuccess/regSuccess methods anymore, 
    # the ScreenManager handles the entire UI transition.            

        '''x=0
        self.backButton=None
        self.l3=None
        self.input1=None
        self.l4=None
        self.input2=None
        self.check=None
        self.l5=None
        self.l7=None
        self.input3=None
        self.signup2=None
        self.l8=None
        self.login3=None
        self.warning=None
        self.front_page(x)
        return self.window
    
    def front_page(self,x):
        if self.backButton: self.window.remove_widget(self.backButton)
        if self.l3: self.window.remove_widget(self.l3)
        if self.input1: self.window.remove_widget(self.input1)
        if self.l4: self.window.remove_widget(self.l4)
        if self.input2: self.window.remove_widget(self.input2)
        if self.check: self.window.remove_widget(self.check)
        if self.l5: self.window.remove_widget(self.l5)
        if self.l7: self.window.remove_widget(self.l7)
        if self.input3: self.window.remove_widget(self.input3)
        if self.signup2: self.window.remove_widget(self.signup2)
        if self.l8: self.window.remove_widget(self.l8)
        if self.login3: self.window.remove_widget(self.login3)
        if self.warning: self.window.remove_widget(self.warning)
        if self.l6: self.window.remove_widget(self.l6)
        self.l1=Label(text='[color=638C6D][b]Welcome ![/b]',font_size=70,markup=True,pos_hint={'center_x':0.5,'center_y':0.7})
        self.window.add_widget(self.l1)
        self.login=Button(text='[b]Login[/b]',markup=True, font_size=40,size_hint=(.2,.1),pos_hint={'center_x':0.5,'center_y':0.55},background_color='#638C6D')
        self.login.bind(on_press=self.login2)
        self.window.add_widget(self.login)
        self.l2=Label(text='[color=638C6D][b]OR[/b]',font_size=45,markup=True,pos_hint={'center_x':0.5,'center_y':0.45})
        self.window.add_widget(self.l2)
        self.signup=Button(text='[b]Sign Up[/b]',markup=True, font_size=40,size_hint=(.2,.1),pos_hint={'center_x':0.5,'center_y':0.35},background_color='#638C6D')
        self.signup.bind(on_press=self.register)
        self.window.add_widget(self.signup)    
    
    def register(self,x):
        self.window.remove_widget(self.l1)
        self.window.remove_widget(self.login)
        self.window.remove_widget(self.l2)
        self.window.remove_widget(self.signup)
        self.backButton=Button(text='[b]Back to Login Page[/b]',markup=True, font_size=20,size_hint=(.18,.05),pos_hint={'center_x':0.1,'center_y':0.9},background_color='#638C6D')
        self.backButton.bind(on_press=self.front_page)
        self.window.add_widget(self.backButton)
        self.l3=Label(text='[color=638C6D][b]Enter Username:[/b]',font_size=45,markup=True,pos_hint={'center_x':0.3,'center_y':0.7})
        self.window.add_widget(self.l3)
        self.input1=TextInput(multiline=False, padding_y=(30,30), size_hint=(0.4, 0.1),pos_hint={"center_x": 0.7, "center_y": 0.7}, font_size=30)
        self.window.add_widget(self.input1)
        self.l4=Label(text='[color=638C6D][b]Enter Password:[/b]',font_size=45,markup=True,pos_hint={'center_x':0.3,'center_y':0.59})
        self.window.add_widget(self.l4)
        self.input2=TextInput(multiline=False, padding_y=(30,30), size_hint=(0.4, 0.1),pos_hint={"center_x": 0.7, "center_y": 0.57}, font_size=30, password=True)
        self.window.add_widget(self.input2)
        self.check = CheckBox(size_hint=(0.1,0.1),pos_hint={"center_x": 0.51, "center_y": 0.49},color='#000000')
        self.check.bind(active=self.on_checkbox_active)
        self.window.add_widget(self.check)
        self.l5=Label(text='[color=000000]Show Password',font_size=25,markup=True,pos_hint={'center_x':0.6,'center_y':0.49})
        self.window.add_widget(self.l5)
        self.l7=Label(text='[color=638C6D][b]Re-Enter Password:[/b]',font_size=45,markup=True,pos_hint={'center_x':0.3,'center_y':0.41})
        self.window.add_widget(self.l7)
        self.input3=TextInput(multiline=False, padding_y=(30,30), size_hint=(0.4, 0.1),pos_hint={"center_x": 0.7, "center_y": 0.39}, font_size=30, password=True)
        self.window.add_widget(self.input3)
        self.signup2=Button(text='[b]Signup[/b]',markup=True, font_size=40,size_hint=(.2,.1),pos_hint={'center_x':0.5,'center_y':0.1},background_color='#638C6D')
        self.signup2.bind(on_press=self.sign)
        self.window.add_widget(self.signup2)
        self.l8=Label(text='[color=4C585B]-Username must contain only alphabets & numbers\n-Username length must be greater than 3 and less than 11\n-Password length must be greater than 5 and less than 13\n-Password must contain atleast 1 uppercase letter, 1 lowercase letter,\n1 digit and atleast one of these characters {!,@,#,$,%,^,&,*}',font_size=16,markup=True,pos_hint={'center_x':0.22,'center_y':0.21})
        self.window.add_widget(self.l8)
    
    def login2(self,x):
        self.window.remove_widget(self.l1)
        self.window.remove_widget(self.login)
        self.window.remove_widget(self.l2)
        self.window.remove_widget(self.signup)
        if self.backButton: self.window.remove_widget(self.backButton)
        if self.l3: self.window.remove_widget(self.l3)
        if self.input1: self.window.remove_widget(self.input1)
        if self.l4: self.window.remove_widget(self.l4)
        if self.input2: self.window.remove_widget(self.input2)
        if self.check: self.window.remove_widget(self.check)
        if self.l5: self.window.remove_widget(self.l5)
        if self.l7: self.window.remove_widget(self.l7)
        if self.input3: self.window.remove_widget(self.input3)
        if self.signup2: self.window.remove_widget(self.signup2)
        if self.l8: self.window.remove_widget(self.l8)
        if self.login3: self.window.remove_widget(self.login3)
        if self.warning: self.window.remove_widget(self.warning)
        self.backButton=Button(text='[b]Back to Signup Page[/b]',markup=True, font_size=20,size_hint=(.18,.05),pos_hint={'center_x':0.1,'center_y':0.9},background_color='#638C6D')
        self.backButton.bind(on_press=self.front_page)
        self.window.add_widget(self.backButton)
        self.l3=Label(text='[color=638C6D][b]Enter Username:[/b]',font_size=45,markup=True,pos_hint={'center_x':0.3,'center_y':0.7})
        self.window.add_widget(self.l3)
        self.input1=TextInput(multiline=False, padding_y=(30,30), size_hint=(0.4, 0.1),pos_hint={"center_x": 0.7, "center_y": 0.7}, font_size=30)
        self.window.add_widget(self.input1)
        self.l4=Label(text='[color=638C6D][b]Enter Password:[/b]',font_size=45,markup=True,pos_hint={'center_x':0.3,'center_y':0.59})
        self.window.add_widget(self.l4)
        self.input2=TextInput(multiline=False, padding_y=(30,30), size_hint=(0.4, 0.1),pos_hint={"center_x": 0.7, "center_y": 0.57}, font_size=30, password=True)
        self.window.add_widget(self.input2)
        self.check = CheckBox(size_hint=(0.1,0.1),pos_hint={"center_x": 0.51, "center_y": 0.49},color='#000000')
        self.check.bind(active=self.on_checkbox_active)
        self.window.add_widget(self.check)
        self.l5=Label(text='[color=000000]Show Password',font_size=25,markup=True,pos_hint={'center_x':0.6,'center_y':0.49})
        self.window.add_widget(self.l5)
        self.login3=Button(text='[b]Login[/b]',markup=True, font_size=40,size_hint=(.2,.1),pos_hint={'center_x':0.5,'center_y':0.1},background_color='#638C6D')
        self.login3.bind(on_press=self.log)
        self.window.add_widget(self.login3)
        
    def on_checkbox_active(self,check,value):
        if value:
            self.input2.password=False
        else:
            self.input2.password=True
            
    def sign(self,x):
        flag1=0
        flag2=0
        if len(self.input1.text)==0:
            if self.warning: self.window.remove_widget(self.warning)
            self.warning=Label(text='[color=FF0000]Username is empty ! Please Try Again',font_size=30,markup=True,pos_hint={'center_x':0.5,'center_y':0.30})
            self.window.add_widget(self.warning)
            flag1=1
            flag2=1
        elif len(self.input2.text)==0:
            if self.warning: self.window.remove_widget(self.warning)
            self.warning=Label(text='[color=FF0000]Password is empty ! Please Try Again',font_size=30,markup=True,pos_hint={'center_x':0.5,'center_y':0.30})
            self.window.add_widget(self.warning)
            flag1=1
            flag2=1
        elif len(self.input3.text)==0:
            if self.warning: self.window.remove_widget(self.warning)
            self.warning=Label(text='[color=FF0000]Please Re-enter the password',font_size=30,markup=True,pos_hint={'center_x':0.5,'center_y':0.30})
            self.window.add_widget(self.warning)
            flag1=1
            flag2=1
        else:
            if len(self.input1.text)>=4 and len(self.input1.text)<=10 and len(self.input2.text)>=6 and len(self.input2.text)<=12:
                for i in range(len(self.input1.text)):
                    if self.input1.text[i].isalpha()==True:
                        continue
                    elif self.input1.text[i].isdigit()==True:
                        continue
                    elif self.input1.text[i]=='_':
                        continue
                    else:
                        flag1=1
                        break
                lc=0
                uc=0
                sc=0
                num=0
                sp_ch=['!','@','#','$','%','^','&','*']
                for i in range(len(self.input2.text)):
                    if self.input2.text[i]==" ":
                        flag1=1
                        break
                    elif re.search("[a-z]",self.input2.text[i]):
                        lc=1
                    elif re.search("[A-Z]",self.input2.text[i]):
                        uc=1
                    elif any(char in sp_ch for char in self.input2.text[i]):
                        sc=1
                    elif re.search("[0-9]",self.input2.text[i]):
                        num=1
                if lc==0 or uc==0 or sc==0 or num==0:
                    flag1=1
            else:
                flag1=1 
        if flag1==1 and flag2==0:
            if self.warning: self.window.remove_widget(self.warning)
            self.warning=Label(text='[color=FF0000]Credentials are not valid ! Please Try Again',font_size=30,markup=True,pos_hint={'center_x':0.5,'center_y':0.30})
            self.window.add_widget(self.warning)
        elif flag1==0 and flag2==0:
            if self.input2.text==self.input3.text:
                tmp1=0
                for i in range(len(self.user)):
                    if self.user[i]==self.input1.text:
                        tmp1=1
                        flag1=1
                        break
                #Need to use db query to search username
                mydb=mysql.connector.connect(
                host='localhost',
                user='root',
                passwd='password123',
                database = 'chat_app',)
                
                #Create cursor for Database
                c=mydb.cursor()
        
                sql_command="SELECT name FROM customers WHERE customers.name=%s"
                c.execute(sql_command,(self.input1.text,))
                rec=c.fetchall()
                if rec:
                    tmp1=1
                    flag1=1
                if tmp1==1:
                    if self.warning: self.window.remove_widget(self.warning)
                    self.warning=Label(text='[color=FF0000]Username is already taken ! Please Try with a Different one',font_size=30,markup=True,pos_hint={'center_x':0.5,'center_y':0.30})
                    self.window.add_widget(self.warning)        
            else:
                flag1=1
                if self.warning: self.window.remove_widget(self.warning)
                self.warning=Label(text='[color=FF0000]Passwords are not matching ! Please Try Again',font_size=30,markup=True,pos_hint={'center_x':0.5,'center_y':0.30})
                self.window.add_widget(self.warning)
        if flag1==0 and flag2==0:
            mydb=mysql.connector.connect(
            host='localhost',
            user='root',
            passwd='password123',
            database = 'chat_app',
        )
            #Create cursor for Database
            c=mydb.cursor()
            
            #Add a record
            
            sql_command="INSERT INTO customers (name,password) VALUES (%s,%s)"
            values=(self.input1.text,self.input2.text)
          
            c.execute(sql_command,values)
              
            
            #Execute SQL command
            #c.execute(sql_command1,values)
            
            
            #Commit our changes
            mydb.commit()
            
            #Close connection
            mydb.close()
            
            self.user.append(self.input1.text)
            self.pas.append(self.input2.text)
            self.regSuccess()
            
    def regSuccess(self):
        if self.warning: self.window.remove_widget(self.warning)
        if self.backButton: self.window.remove_widget(self.backButton)
        self.window.remove_widget(self.l3)
        self.window.remove_widget(self.input1)
        self.window.remove_widget(self.l4)
        self.window.remove_widget(self.input2)
        self.window.remove_widget(self.check)
        self.window.remove_widget(self.l5)
        self.window.remove_widget(self.l7)
        self.window.remove_widget(self.input3)
        self.window.remove_widget(self.l8)
        self.window.remove_widget(self.signup2)
        self.l3=Label(text='[color=638C6D][b]Account created !![/b]',font_size=40,markup=True,pos_hint={'center_x':0.5,'center_y':0.6})
        self.window.add_widget(self.l3)
        self.logout=Button(text='[b]Logout[/b]',markup=True, font_size=30,size_hint=(.1,.07),pos_hint={'center_x':0.5,'center_y':0.45},background_color='#638C6D')
        self.logout.bind(on_press=self.logout2)
        self.window.add_widget(self.logout)

    def log(self,x):
        tmp3=0
        tmp4=0
        if self.input1.text=="":
            self.l6=Label(text='[color=FF0000]Username is empty !',font_size=40,markup=True,pos_hint={'center_x':0.5,'center_y':0.30})
            self.window.add_widget(self.l6)
        elif self.input2.text=="":
            if self.l6: self.window.remove_widget(self.l6)
            self.l6=Label(text='[color=FF0000]Password is empty !',font_size=40,markup=True,pos_hint={'center_x':0.5,'center_y':0.30})
            self.window.add_widget(self.l6)
        else:
            for i in range(len(self.user)):
                if self.user[i]==self.input1.text:
                    tmp3=1
                    x=i
                    break
            mydb=mysql.connector.connect(
                host='localhost',
                user='root',
                passwd='password123',
                database = 'chat_app',)
                
                #Create cursor for Database
            c=mydb.cursor()
            
            #SQLQ to check whether username is already registered or not
            sql_command="SELECT name FROM customers WHERE customers.name=%s"
            c.execute(sql_command,(self.input1.text,))
            rec=c.fetchall()
            if rec:
                tmp3=1
            if tmp3==0:
                if self.l6: self.window.remove_widget(self.l6)
                self.l6=Label(text='[color=FF0000]Username is not registered. Please sign in first.',font_size=40,markup=True,pos_hint={'center_x':0.5,'center_y':0.30})
                self.window.add_widget(self.l6)
            else:
                mydb=mysql.connector.connect(
                host='localhost',
                user='root',
                passwd='password123',
                database = 'chat_app',)
                
                #Create cursor for Database
                c=mydb.cursor()
                #SQLQ to check whether password matches with the given username
                sql_command="SELECT password FROM customers WHERE customers.name=%s"
                c.execute(sql_command,(self.input1.text,))
                rec=c.fetchall()
                if rec[0][0]==self.input2.text:
                    tmp4=1    
                if tmp4==0:
                    if self.l6: self.window.remove_widget(self.l6)
                    self.l6=Label(text='[color=FF0000]Wrong Password. Please try again.',font_size=40,markup=True,pos_hint={'center_x':0.5,'center_y':0.30})
                    self.window.add_widget(self.l6)
                else:
                    self.window.remove_widget(self.l3)
                    self.window.remove_widget(self.input1)
                    self.window.remove_widget(self.l4)
                    self.window.remove_widget(self.input2)
                    self.window.remove_widget(self.check)
                    self.window.remove_widget(self.l5)
                    self.window.remove_widget(self.login3)
                    if self.l6: self.window.remove_widget(self.l6)
                    if self.backButton: self.window.remove_widget(self.backButton)
                    self.l6=Label(text='[color=638C6D]Welcome Back!!',font_size=40,markup=True,pos_hint={'center_x':0.5,'center_y':0.4})
                    self.window.add_widget(self.l6)
                    self.logout=Button(text='[b]Logout[/b]',markup=True, font_size=30,size_hint=(.1,.07),pos_hint={'center_x':0.5,'center_y':0.45},background_color='#638C6D')
                    self.logout.bind(on_press=self.logout2)
                    self.window.add_widget(self.logout)
                    self.logSucess()

    def logSucess(self):
        self.window.remove_widget(self.l3)
        self.window.remove_widget(self.input1)
        self.window.remove_widget(self.l4)
        self.window.remove_widget(self.input2)
        self.window.remove_widget(self.check)
        self.window.remove_widget(self.l5)
        self.window.remove_widget(self.login3)
        if self.l6: self.window.remove_widget(self.l6)
        if self.backButton: self.window.remove_widget(self.backButton)
        self.l6=Label(text='[color=638C6D]Welcome Back!!',font_size=40,markup=True,pos_hint={'center_x':0.5,'center_y':0.4})
        self.window.add_widget(self.l6)
        self.logout=Button(text='[b]Logout[/b]',markup=True, font_size=30,size_hint=(.1,.07),pos_hint={'center_x':0.5,'center_y':0.45},background_color='#638C6D')
        self.logout.bind(on_press=self.logout2)
        self.window.add_widget(self.logout)
                
    def logout2(self,x):
        if self.l3: self.window.remove_widget(self.l3)
        if self.logout: self.window.remove_widget(self.logout)
        if self.l6: self.window.remove_widget(self.l6)
        self.l1=Label(text='[color=638C6D][b]Welcome ![/b]',font_size=70,markup=True,pos_hint={'center_x':0.5,'center_y':0.7})
        self.window.add_widget(self.l1)
        self.login=Button(text='[b]Login[/b]',markup=True, font_size=40,size_hint=(.2,.1),pos_hint={'center_x':0.5,'center_y':0.55},background_color='#638C6D')
        self.login.bind(on_press=self.login2)
        self.window.add_widget(self.login)
        self.l2=Label(text='[color=638C6D][b]OR[/b]',font_size=45,markup=True,pos_hint={'center_x':0.5,'center_y':0.45})
        self.window.add_widget(self.l2)
        self.signup=Button(text='[b]Sign Up[/b]',markup=True, font_size=40,size_hint=(.2,.1),pos_hint={'center_x':0.5,'center_y':0.35},background_color='#638C6D')
        self.signup.bind(on_press=self.register)
        self.window.add_widget(self.signup)'''
        
if __name__=="__main__":
    Chat().run()