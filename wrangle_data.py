import pandas as pd

# function for wrangling data in both exploratory and explanatory visualisations.
def wrangle_data(df: pd.DataFrame):
    employment_order = ["Not employed", "Part-time", "Self-employed", "Employed", "Full-time", "Retired", "Other", "Not available"]
    employment_type = pd.CategoricalDtype(employment_order, True)
    df["EmploymentStatus"] = df["EmploymentStatus"].astype(employment_type)

    # make IncomeRange ordinal
    income_range_order = ["Not displayed", "Not employed", "$0", "$1-24,999", "$25,000-49,999", "$50,000-74,999", "$75,000-99,999", "$100,000+"]
    income_range_type = pd.CategoricalDtype(income_range_order, True)
    df["IncomeRange"] = df["IncomeRange"].astype(income_range_type)

    # Get interest amount (Note: Interest rate is haram)
    df["InterestAmount"] = df["LoanOriginalAmount"] * df["BorrowerRate"]

    # Summarize Loan status
    def summaryLoansStatus( status ):
        if status == "FinalPaymentInProgress": # merge FinalPaymentInProgress and Current
            return "Current"

        elif status.startswith("Past Due"):  # merge all "Past Due" categories
            return "Paid late"

        else:
            return status
    df["LoanStatusSummarized"] = df["LoanStatus"].apply(summaryLoansStatus)

    # BorrowerStatus feature engineer
    bad_status = ['Paid late', 'Defaulted', 'Chargedoff']
    df["BorrowerStatus"] = 'Good'
    df.loc[ df["LoanStatusSummarized"].isin(bad_status) ,"BorrowerStatus"] = 'Messed up'

    # These are the listing categories provided from the data dictionary
    ListingCategories = ['Not Available', 'Debt Consolidation', 'Home', 'Improvement', 'Business', 'Personal Loan', 'Student Use', 'Auto', 'Other', 'Baby&Adoption', 'Boat', 'Cosmetic', 'Procedure', 'Engagement Ring', 'Green Loans', 'Household Expenses', 'Large Purchases', 'Medical/Dental', 'Motorcycle', 'RV', 'Taxes', 'Vacation', 'Wedding Loans']
    
    # Transform representation of listing categories from numbers to strings
    df["ListingCategory"] = [ ListingCategories[i] for i in df["ListingCategory (numeric)"] ]

    # Remove the time from the dates
    # turn this (yyyy-mm-dd 00:00:00) to this (yyyy-mm-dd)
    df["LoanDate"] = df["LoanOriginationDate"].apply(lambda x: x.split(" ")[0] )
    return df