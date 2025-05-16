from scraping import get_fixture

if __name__ == "__main__":
    date, opponent = get_fixture()
    print(date)
    print(opponent)
    if date and opponent:
        print(f"The next fixture is against {opponent} on {date}")
    else:
        print("It didn't work")