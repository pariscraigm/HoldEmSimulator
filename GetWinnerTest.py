from getWinner import*


def main():

    test_is_flush()
    test_is_royal()

def test_is_flush():

    assert flush(["AS", "10S", "5S", "2S", "9S"])
    assert flush(["AD", "10S", "5S", "2S", "9S"]) == False
    assert flush(["AS", "10S", "5S", "2S", "9D"]) == False


def test_is_royal():

    assert is_royal(["AS", "KS", "QS", "JS", "10S"])
    assert is_royal(["AS", "10S", "5S", "2S", "9S"]) == False
    assert is_royal(["AS", "10S", "KS", "QS", "9S"]) == False


def test_is_royal_flush():
    return


def test_get_winner():
    return 0

if __name__ == "__main__":
    main()