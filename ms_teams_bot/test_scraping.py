from scraping2 import get_fixture

if __name__ == "__main__":
    date, opponent, pitch = get_fixture()
    if date and opponent and pitch:
        print(f"The next fixture is against {opponent} on {date}, {pitch}")
    else:
        print("It didn't work")