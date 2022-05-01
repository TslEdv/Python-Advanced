import sqlite3


# open the connection to the database
connection = sqlite3.connect("C:\\Users\\User\\HW2database1.db")
cursor = connection.cursor()


def create_tables():
    """
    Creates tables Provider and Canteen
    """
    # sql command to create table Provider
    sql_command = """
    CREATE TABLE IF NOT EXISTS Provider ( 
    ID INTEGER PRIMARY KEY, 
    ProviderName TEXT NOT NULL,
    UNIQUE (ProviderName)
    );"""

    cursor.execute(sql_command)

    # sql command to create table Canteen
    sql_command = """
    CREATE TABLE IF NOT EXISTS Canteen ( 
    ID INTEGER PRIMARY KEY, 
    ProviderID INTEGER,
    Name TEXT NOT NULL,
    Location TEXT NOT NULL,
    time_open INTEGER,
    time_closed INTEGER,
    FOREIGN KEY(ProviderID) REFERENCES Provider(ID),
    UNIQUE (Name)
    );"""

    cursor.execute(sql_command)


def add_providers():
    """
    Adds the list of providers to table Provider
    """
    providers = ["Rahva Toit",
                 "Baltic Restaurants Estonia AS",
                 "TTÜ Sport OÜ",
                 "bitStop Kohvik OÜ"]

    # iterates through the list of providers and adds the provider,
    # if the provider already exists, ignores the command
    for provider in providers:
        insert_command = """
        INSERT OR IGNORE INTO Provider (ProviderName) VALUES ("{name}") 
        ;"""
        insert_command = insert_command.format(name=provider)
        cursor.execute(insert_command)

    connection.commit()


def add_only_it_college():
    """
    Adds IT college canteen to table Canteen
    """

    # inserts the canteen if it already does not exist
    insert_command = """
    INSERT OR IGNORE INTO Canteen (ProviderID, Name, Location, time_open, time_closed)
    VALUES (
    (SELECT ID FROM Provider WHERE ProviderName="bitStop Kohvik OÜ"), 
    "bitStop KOHVIK", 
    "IT College, Raja 4c", 
    930, 
    1600)
    ;"""
    cursor.execute(insert_command)
    connection.commit()


def add_other_canteens():
    """
    Adds the list of canteens to table Canteen
    """

    # list of canteens with data formatted as provider name, name, location, time open, time closed
    canteen_data = [
        ("Rahva Toit", "Economics- and social science building canteen", "Akadeemia tee 3, SOC- building", 830, 1830),
        ("Rahva Toit", "Library canteen", "Akadeemia tee 1/Ehitajate tee 7", 830, 1900),
        ("Baltic Restaurants Estonia AS", "Main building Deli cafe", "Ehitajate tee 5, U01 building", 900, 1630),
        ("Baltic Restaurants Estonia AS", "Main building Daily lunch restaurant", "Ehitajate tee 5, U01 building", 900,
         1630),
        ("Rahva Toit", "U06 building canteen", "U06 building canteen", 900, 1600),
        ("Baltic Restaurants Estonia AS", "Natural Science building canteen", "Akadeemia tee 15, SCI building", 900,
         1600),
        ("Baltic Restaurants Estonia AS", "ICT building canteen", "Raja 15/Mäepealse 1", 900, 1600),
        ("TTÜ Sport OÜ", "Sports building canteen", "Männiliiva 7, S01 building", 1100, 2000)]

    # iterates through the list of canteens and adds the canteen,
    # if the canteen already exists, ignores the command
    for c in canteen_data:
        insert_command = """
        INSERT OR IGNORE INTO Canteen (ProviderID, Name, Location, time_open, time_closed) 
        VALUES (
        (SELECT ID FROM Provider WHERE ProviderName="{providerid}"), 
        "{name}",
        "{location}",
        "{timeopen}",
        "{timeclosed}")
        ;"""
        insert_command = insert_command.format(providerid=c[0], name=c[1], location=c[2], timeopen=c[3],
                                               timeclosed=c[4])
        cursor.execute(insert_command)

    connection.commit()


def query_all_providers():
    """
    Queries all providers
    """

    # queries all providers and prints them out
    cursor.execute("SELECT * FROM Provider")
    result = cursor.fetchall()
    for r in result:
        print(r)


def query_1615_1800():
    """
    Queries for the canteens that are open in the time frame 16:15-18:00
    """

    # query for the canteens where the closing time is at 6 or later
    # and if the opening time is at 16:15 or earlier
    # then print out the results
    select_command = """
    SELECT Name, Location, time_open, time_closed 
    FROM Canteen
    WHERE time_open <= 1615 AND time_closed >= 1800
    ;"""
    cursor.execute(select_command)
    print("Libraries open at 16:15-18:00")
    result = cursor.fetchall()
    for r in result:
        print(r)


def query_rahva_toit():
    """
    Query all the canteens that belong to Provider called Rahva Toit
    """

    # if the canteen's provider's name matches to Rahva Toit print it out
    select_command = """
    SELECT Name, Location, time_open, time_closed
    FROM Canteen
    INNER JOIN Provider
    ON Provider.ID = Canteen.ProviderID
    WHERE Provider.ProviderName = "Rahva Toit"
    ;"""
    cursor.execute(select_command)
    print("Canteens serviced by Rahva Toit:")
    result = cursor.fetchall()
    for r in result:
        print(r)


# Executing all the functions
create_tables()
add_providers()
add_only_it_college()
add_other_canteens()
query_all_providers()
query_1615_1800()
query_rahva_toit()

# closing the connection
connection.close()
