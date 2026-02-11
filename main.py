import pandas as pd

# Loading and Fixing Structure
def load_data(file_path):
    df_raw = pd.read_excel(file_path, engine="xlrd")
    
    cleaned_rows = []

    for row in df_raw.iloc[:, 0]:
        parts = row.split(",")

        # Find email position
        email_index = next((i for i, p in enumerate(parts) if "@" in p), None)

        if email_index is None:
            continue

        name = ",".join(parts[:email_index]).strip()
        email = parts[email_index].strip()
        signup_date = parts[email_index + 1].strip() if len(parts) > email_index + 1 else ""
        plan = parts[email_index + 2].strip() if len(parts) > email_index + 2 else ""
        notes = ",".join(parts[email_index + 3:]).strip() if len(parts) > email_index + 3 else ""

        cleaned_rows.append([name, email, signup_date, plan, notes])

    df = pd.DataFrame(
        cleaned_rows,
        columns=["name", "email", "signup_date", "plan", "notes"]
    )

    return df

# Basic Cleaning
def basic_cleaning(df):
    # Strip whitespace
    df = df.apply(lambda x: x.str.strip())

    # Lowercase emails
    df["email"] = df["email"].str.lower()

    # Standardize name capitalization
    df["name"] = df["name"].str.title()

    return df

# Standardize Dates
def standardize_dates(df):
    df["signup_date"] = pd.to_datetime(
        df["signup_date"],
        errors="coerce",
        dayfirst=True
    )

    df["signup_date"] = " " + df["signup_date"].dt.strftime("%Y-%m-%d")

    return df

# Separate Low Quality Leads
def separate_low_quality(df):
    condition = (
        df["name"].str.contains("test", case=False, na=False) |
        df["notes"].str.contains("ignore", case=False, na=False) |
        ~df["email"].str.contains("@", na=False) |
        df["signup_date"].isna()
    )

    quarantine_df = df[condition].copy()
    clean_df = df[~condition].copy()

    return clean_df, quarantine_df

# Dedup + Multi-Plan Logic
def handle_duplicates(df):
    df["signup_date"] = pd.to_datetime(
        df["signup_date"],
        errors="coerce"
    )

    # Count how many times email appears
    email_counts = df["email"].value_counts()

    # Flag multi-plan users
    df["is_multi_plan"] = df["email"].map(email_counts) > 1

    # Sort by latest date first
    df = df.sort_values("signup_date", ascending=False)

    # Keep only latest signup per email
    df = df.drop_duplicates(subset="email", keep="first")

    # Convert date back to string format
    df["signup_date"] = " " + df["signup_date"].dt.strftime("%Y-%m-%d")

    return df

# EXECUTION
def main():
    df = load_data("signup.xls")

    df = basic_cleaning(df)
    df = standardize_dates(df)

    clean_df, quarantine_df = separate_low_quality(df)

    final_df = handle_duplicates(clean_df)

    # Export files
    final_df.to_csv("members_final.csv", index=False)
    quarantine_df.to_csv("quarantine.csv", index=False)

    print("members_final.csv created")
    print("quarantine.csv created")


if __name__ == "__main__":
    main()
