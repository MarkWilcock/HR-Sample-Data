import csv
import random
import pandas as pd
import numpy as np
from datetime import date, timedelta, datetime
from dateutil.relativedelta import relativedelta
from openpyxl import load_workbook

from load_lists import generate_absence_reasons

current_date = datetime.today().date()  


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

# --- weighted random helpers (vectorized) ---------------------------------- #

def random_grade_weighted_vec(n: int) -> list[int]:
    """Return a list of random grade keys (1-7) with custom weighted probabilities."""
    choices = [1, 2, 3, 4, 5, 6, 7]
    weights = [5, 10, 20, 30, 20, 10, 5]
    return random.choices(choices, weights=weights, k=n)

def random_department_weighted_vec(n: int) -> list[int]:
    """Return a list of random department keys (1-8) with custom weighted probabilities."""
    choices = [1, 2, 3, 4, 5, 6, 7, 8]
    weights = [5, 10, 15, 20, 20, 15, 10, 5]
    return random.choices(choices, weights=weights, k=n)

def random_division_weighted_vec(n: int) -> list[int]:
    """Return a list of random division keys (1-5) with custom weighted probabilities."""
    choices = [1, 2, 3, 4, 5]
    weights = [5, 10, 15, 20, 50]
    return random.choices(choices, weights=weights, k=n)


def random_dob_vec(n: int) -> list[date]:
    """Return a list of random dates of birth within bounds, sampled from a normal distribution."""
    mean_dob = pd.Timestamp(MEAN_DOB)
    dob_min = pd.Timestamp(DOB_MIN)
    dob_max = pd.Timestamp(DOB_MAX)
    dobs = []
    while len(dobs) < n:
        batch = mean_dob + pd.to_timedelta(np.random.normal(0, STD_DAYS, n), unit='D')
        batch = batch[(batch >= dob_min) & (batch <= dob_max)]
        dobs.extend([d.date() for d in batch])
    return dobs[:n]

def generate_join_date_vec(dobs: list[date]) -> list[date]:
    """Return a list of join dates, each at least 21 years after the corresponding DOB and not after today."""
    join_dates = []
    for dob in dobs:
        min_join = dob + relativedelta(years=21)
        if min_join > current_date:
            min_join = current_date
        delta_days = (current_date - min_join).days
        join_date = min_join + timedelta(days=random.randint(0, delta_days))
        join_dates.append(join_date)
    return join_dates

def generate_leave_date_vec(join_dates: list[date]) -> list[date | None]:
    """Return a list of leave dates, each up to 25 years after join date, or None if more than 6 months in the future."""
    leave_dates = []
    for join_date in join_dates:
        max_leave_date = join_date + relativedelta(years=25)
        delta_days = (max_leave_date - join_date).days
        leave_date = join_date + timedelta(days=random.randint(0, delta_days))
        if leave_date > current_date + relativedelta(months=6):
            leave_date = None
        leave_dates.append(leave_date)
    return leave_dates

# --- main DataFrame generation --------------------------------------------- #

def generate_employee_df(n_records: int) -> pd.DataFrame:
    """Generate a DataFrame of synthetic employee data with weighted random attributes."""
    df = pd.DataFrame({
        "EmployeeId": [f"E-{i+1:05d}" for i in range(n_records)],
        "Gender": np.random.choice(["Male", "Female"], size=n_records, p=[0.6, 0.4]),
    })
    df["First Name"] = df["Gender"].apply(lambda g: random.choice(MALE_NAMES if g == "Male" else FEMALE_NAMES))
    df["Last Name"] = np.random.choice(SURNAMES, size=n_records)
    df["Status"] = np.random.choice(["Permanent Role", "Growth Role"], size=n_records, p=[0.7, 0.3])
    df["Vacancy Type"] = np.random.choice(["Replacement", "New"], size=n_records, p=[0.8, 0.2])
    df["Grade Key"] = random_grade_weighted_vec(n_records)
    df["Department Key"] = random_department_weighted_vec(n_records)
    df["Workforce Planning A Key"] = random_division_weighted_vec(n_records)
    df["FTE"] = np.random.choice([0.5, 1], size=n_records, p=[0.1, 0.9])
    dobs = random_dob_vec(n_records)
    df["Birth Date"] = [d.isoformat() for d in dobs]
    join_dates = generate_join_date_vec(dobs)
    df["Join Date"] = [d.isoformat() for d in join_dates]
    leave_dates = generate_leave_date_vec(join_dates)
    df["Leave Date"] = [d.isoformat() if d else None for d in leave_dates]
    df["Reason For Leaving"] = np.random.choice(
            ["Resignation", "Retirement", "End Of Contract", "Mutual Agreement", "Redundancy", "Unsatisfactory Probation", "Dismissal"],
            size=n_records, p=[0.1, 0.05, 0.3, 0.1, 0.3, 0.05, 0.1]
        )
    )
    df["Rating How"] =  np.where(
        pd.to_datetime(df["Leave Date"]) <= pd.Timestamp("2023-12-31"),
        "-Not Applicable-",
        np.random.choice(["On Track", "High", "Exceptional"], size=n_records, p=[0.7, 0.2, 0.1])
    )
    df["Rating What"] =  np.where(
        pd.to_datetime(df["Leave Date"]) <= pd.Timestamp("2023-12-31"),
        "-Not Applicable-",
        np.random.choice(["On Track", "High", "Exceptional"], size=n_records, p=[0.7, 0.2, 0.1])
    )

    df["Absence Rate"] = np.random.uniform(0.0, 0.1, size=n_records)
    return df

# --- output CSV ------------------------------------------------------------ #


df = generate_employee_df(N_RECORDS)
file_path = "./outputs/employee.csv"
df.to_csv(file_path, index=False)

print(f"Sample data generated and saved to {file_path}")
print("Sample data generation complete.")

# Display first 10 rows for user preview
print(df.head(5))

