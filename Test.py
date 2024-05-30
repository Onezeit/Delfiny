import matplotlib.pyplot as plt

# Usunięcie powtórzonych wartości i zaktualizowanie danych
odleglosc = [
    3.535533906, 6.519202405, 9.513148795, 12.509996, 15.50806242, 18.50675552,
    21.50581317, 24.50510151, 27.50454408, 30.50409809, 33.50373114, 36.5034245,
    39.50316443
]

moc_szerokopasmowo = [
    -2.914932, -8.043912, -10.79002, -12.60352, -13.89179, -14.94128,
    -15.82638, -16.51187, -17.10078, -17.55781, -18.04621, -18.34623,
    -18.67425
]

# Rysowanie wykresu
plt.figure(figsize=(10, 6))
plt.plot(odleglosc, moc_szerokopasmowo, 'o-', color='b')
plt.scatter(odleglosc, moc_szerokopasmowo, color='b')
plt.xlabel('Odległość [m]')
plt.ylabel('Moc odbierana szerokopasmowo [dBm]')
plt.title('Zmiany odbieranej mocy szerokopasmowo w funkcji odległości od anteny nadawczej')
plt.grid(True)
plt.show()

