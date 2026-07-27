# External reference: statistics page /practice/23742/
# Accepted submission: 43299870
# Source: http://cs101.openjudge.cn/practice/solution/43299870/
# License: not declared on the submission page; no license is inferred.

def is_palindrome(date):
    date_str = str(date)
    return date_str == date_str[::-1]

def generate_palindrome_dates(start_date, end_date):
    palindrome_dates = []
    for year in range(1000, 10000):
        for month in {1,3,5,7,8,10,12}:
            for day in range(1, 32):
                date = year * 10000 + month * 100 + day
                if start_date <= date <= end_date and is_palindrome(date):
                    palindrome_dates.append(str(date))
        for month in {4,6,9,11}:
            for day in range(1, 31):
                date = year * 10000 + month * 100 + day
                if start_date <= date <= end_date and is_palindrome(date):
                    palindrome_dates.append(str(date))
        for month in {2}:
            for day in range(1, 30):
                date = year * 10000 + month * 100 + day
                if start_date <= date <= end_date and is_palindrome(date):
                    palindrome_dates.append(str(date))
    return palindrome_dates

start_date = 10000101
end_date=int(input())
palindrome_dates = generate_palindrome_dates(start_date, end_date)

print(" ".join(palindrome_dates))
