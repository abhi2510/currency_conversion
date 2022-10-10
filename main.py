from app import CurrencyConversion

if __name__ == '__main__':
    data = CurrencyConversion.get_data("M.N.I8.W1.S1.S1.T.N.FA.F.F7.T.EUR._T.T.N", "GP")
    print(data)