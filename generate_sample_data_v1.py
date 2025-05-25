import csv
import random
import pandas as pd
from datetime import date, timedelta, datetime
from dateutil.relativedelta import relativedelta

# --- source data ----------------------------------------------------------- #

MALE_NAMES = [
    "Aaron", "Adam", "Ahmed", "Aiden", "Alfie", "Ali", "Andreas", "Andrew", "Anthony",
    "Archie", "Arthur", "Bartosz", "Benjamin", "Brandon", "Cameron", "Callum", "Charles",
    "Charlie", "Connor", "Daniel", "David", "Dominic", "Dylan", "Edward", "Elliot",
    "Emil", "Erik", "Ethan", "Felix", "Finley", "Filip", "Freddie", "Gabriel", "George",
    "Harry", "Hassan", "Henry", "Hugo", "Jack", "Jake", "Jakub", "James", "Jamie",
    "Jan", "Jayden", "Jasper", "John", "Joseph", "Joseph", "Joshua", "Julian", "Kacper",
    "Kristian", "Kyle", "Leo", "Lewis", "Liam", "Luka", "Lucas", "Louis", "Lukas",
    "Luke", "Marek", "Marek", "Mark", "Martin", "Mariusz", "Mason", "Mateusz", "Matteo",
    "Matthew", "Max", "Michael", "Milo", "Mohammed", "Nathan", "Nico", "Noah", "Omar",
    "Oscar", "Oscar", "Owen", "Patryk", "Paul", "Pavel", "Peter", "Philip", "Richard",
    "Riley", "Robert", "Roman", "Ryan", "Samuel", "Sebastian", "Simon", "Smith", "Stefan",
    "Stephen", "Sven", "Taylor", "Theo", "Thomas", "Thompson", "Toby", "Tomas", "Tyler",
    "Vincent", "Walker"
]

FEMALE_NAMES = [
    "Abigail", "Adanna", "Agata", "Aisha", "Aleksandra", "Alice", "Alice", "Amina", "Ama", "Amelia", "Anna", "Anna",
    "Aurora", "Ayana", "Bethany", "Camille", "Charlotte", "Chinara", "Chloe", "Clara", "Daisy", "Eleanor", "Elena",
    "Elisa", "Ella", "Emily", "Emma", "Erin", "Eshe", "Eva", "Evie", "Farah", "Fatima", "Fatimah", "Florence",
    "Francesca", "Freya", "Georgia", "Giulia", "Grace", "Hannah", "Harriet", "Holly", "Huda", "Ifunanya", "Imani",
    "Imogen", "Isabella", "Jana", "Jasmine", "Jessica", "Julia", "Katarina", "Katie", "Kinga", "Kristina", "Kwamboka",
    "Lauren", "Layla", "Lea", "Leah", "Lenka", "Lily", "Lola", "Lucia", "Lucy", "Maddison", "Madison", "Magdalena",
    "Makena", "Maja", "Maria", "Mariam", "Martina", "Martha", "Matilda", "Megan", "Mia", "Michaela", "Millie",
    "Molly", "Nadia", "Natalia", "Nia", "Ngozi", "Nina", "Noor", "Olivia", "Paulina", "Petra", "Phoebe", "Poppy",
    "Rania", "Rosie", "Ruby", "Sade", "Salma", "Samira", "Samantha", "Sana", "Sara", "Scarlett", "Sienna", "Simona",
    "Sofia", "Sofia", "Sophie", "Summer", "Sumaya", "Tariro", "Tereza", "Viktoria", "Victoria", "Veronika", "Yasmin",
    "Yetunde", "Zahra", "Zoe", "Zuri", "Zuzanna"
]

SURNAMES = [
    "Abebe", "Adams", "Adebayo", "Allen", "Armstrong", "Arnold", "Atkinson", "Austin",
    "Bailey", "Baker", "Baldwin", "Barnes", "Barnett", "Barker", "Bates", "Baxter",
    "Bell", "Bennett", "Benson", "Berry", "Bishop", "Black", "Booth", "Bradley",
    "Brooks", "Brown", "Burns", "Burgess", "Butler", "Campbell", "Carroll", "Carter",
    "Chapman", "Chen", "Chukwu", "Clark", "Cole", "Cook", "Cooper", "Cox", "Cross",
    "Curtis", "Davies", "Dean", "Diallo", "Dixon", "Douglas", "Dunn", "Edwards",
    "Ellis", "Evans", "Fisher", "Fleming", "Fletcher", "Ford", "Foster", "Fox",
    "Francis", "Frost", "Gibbs", "Gibson", "Gordon", "Graham", "Grant", "Gray",
    "Green", "Hall", "Hamilton", "Harper", "Harris", "Harrison", "Hart", "Harvey",
    "Hawkins", "Henderson", "Higgins", "Hill", "Holland", "Holmes", "Holt", "Howard",
    "Hudson", "Hughes", "Hunt", "Hunter", "James", "Johnson", "Jones", "Jordan",
    "Kamau", "Kelly", "Khan", "Kim", "King", "Knight", "Lane", "Lawrence", "Lewis",
    "Marshall", "Mason", "Matthews", "Mensah", "Miller", "Mills", "Mitchell", "Moore",
    "Morgan", "Morris", "Morrison", "Murray", "Mwangi", "Ndlovu", "Nelson", "Newton",
    "Nguyen", "Nicholson", "Nkosi", "Okafor", "Owen", "Palmer", "Parker", "Parsons",
    "Patel", "Payne", "Pearce", "Pearson", "Perry", "Phillips", "Porter", "Price",
    "Reed", "Reid", "Reynolds", "Richardson", "Roberts", "Rose", "Rowe", "Russell",
    "Sanders", "Saunders", "Scott", "Shaw", "Simpson", "Singh", "Smith", "Spencer",
    "Stevens", "Stephens", "Stewart", "Stone", "Tanaka", "Taylor", "Thomas", "Thompson",
    "Turner", "Wallace", "Walsh", "Walters", "Ward", "Warren", "Watson", "Webb",
    "Wells", "West", "White", "Williams", "Wilson", "Wong", "Wood", "Woods", "Wright",
    "Yamamoto", "Young", "Zhang"
]

# --- configuration --------------------------------------------------------- #

N_RECORDS      = 1000
MEAN_DOB       = date(1982, 1, 1)
STD_YEARS      = 10                               # ≈ one decade
STD_DAYS       = int(STD_YEARS * 365.25)          # convert to days
DOB_MIN        = date(1960, 1, 1)
DOB_MAX        = date(2003, 12, 31)

today = date(2025, 5, 24)

# Function to generate join date
def generate_join_date(dob) -> date:
    min_join = dob + relativedelta(years=21)
    if min_join > today:
        # If somehow date exceeds today (shouldn't happen with given DOB range), set min_join to today
        min_join = today
    delta_days = (today - min_join).days
    join_date = min_join + timedelta(days=random.randint(0, delta_days))
    return join_date

# Function to generate join date
def generate_leave_date(join_date) -> date | None:
    max_leave_date = join_date + relativedelta(years=25)
    delta_days = (max_leave_date - join_date).days
    leave_date = join_date + timedelta(days=random.randint(0, delta_days))
    if leave_date > today + relativedelta(months=6):
        # If leave date is more than 6 months in the future, set it to None 
        leave_date = None
    
    return leave_date

def random_grade_weighted() -> int:
    """Return a random integer 1-7 with custom probabilities"""
    choices = [1, 2, 3, 4, 5, 6, 7]
    weights = [5, 10, 20, 30, 20, 10, 5]
    return random.choices(choices, weights=weights, k=1)[0]

def random_department_weighted() -> int:
    """Return a random integer 1-8 with custom probabilities"""
    choices = [1, 2, 3, 4, 5, 6, 7, 8]
    weights = [5, 10, 15, 20, 20, 15, 10, 5]
    return random.choices(choices, weights=weights, k=1)[0]

def random_division_weighted() -> int:
    """Return a random integer 1-8 with custom probabilities"""
    choices = [1, 2, 3, 4, 5]
    weights = [5, 10, 15, 20, 50]
    return random.choices(choices, weights=weights, k=1)[0]

# --- helpers --------------------------------------------------------------- #

def random_dob() -> date:
    """Return a DOB within bounds, sampled from ~N(mean, std)."""
    while True:
        offset_days = int(random.gauss(0, STD_DAYS))
        candidate   = MEAN_DOB + timedelta(days=offset_days)
        if DOB_MIN <= candidate <= DOB_MAX:
            return candidate

# --- generate records ------------------------------------------------------ #

rows = []
for i in range(N_RECORDS):
    employee_id = f"E-{i+1:05d}"
    gender = random.choices(["Male", "Female"], weights=[0.6, 0.4], k=1)[0]
    first  = random.choice(MALE_NAMES if gender == "Male" else FEMALE_NAMES)
    last   = random.choice(SURNAMES)
    grade_key = random_grade_weighted()
    department_key = random_department_weighted()
    division_key = random_division_weighted()
    fte = random.choices([0.5, 1], weights=[0.1, 0.9], k=1)[0]
    dob_date = random_dob() 
    join_date = generate_join_date(dob_date)
    leave_date = generate_leave_date(join_date)
    dob_str    = dob_date.isoformat()
    rows.append(
        [employee_id, first, last, gender, grade_key, department_key, division_key, fte,
         dob_date.isoformat(), 
         join_date.isoformat(), 
         leave_date.isoformat() if leave_date else None
         ]) 

# --- output CSV ------------------------------------------------------------ #

file_path = "./outputs/employee.csv"
column_names = ["EmployeeId", "First Name", "Last Name", "Gender", "Grade Key", "Department Key", "Division Key", "FTE", "Birth Date", "Join Date", "Leave Date"]
with open(file_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(column_names)
    writer.writerows(rows)

print(f"Sample data generated and saved to {file_path}")
print("Sample data generation complete.")   

# Display first 10 rows for user preview
df_preview = pd.DataFrame(rows, columns=column_names).head(10)
print(df_preview.head(5))
