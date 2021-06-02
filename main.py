from statemachine import State, Transition
from nx import *


def is_valid(available_states, test_state):
    for state in available_states:
        if state == test_state:
            return True
    raise ValueError('Zła wartość')


master_states = ["Stacja niegotowa do pracy",
                  "Proces sprawdzania liczby obiektów",
                  "Uruchomienie taśmy 1",
                  "Proces sprawdzania kompletności",
                  "Stacja oczekuje na wykrycie obiektu",
                  "Obiekt wykryty na taśmie 2"]

slave_states = ["Proces sprawdzania kompletności",
                 "Test wagi pudełka",
                 "Interwencja pracownika",
                 "Pudełko jest gotowe do wysyłki",
                 "Pudełko jest wadliwe"]

master_form_to = [
    [0, [1]],
    [1, [2, 4]],
    [2, [3]],
    [3, [0]],
    [4, [5]],
    [5, [1]]
]

slave_form_to = [
    [0, [1]],
    [1, [2, 3]],
    [2, [3, 4]],
    [3, []],
    [4, []]
]

master_events = {(0, 1): "Wykrycie pudełka na taśmie 1",
                 (1, 2): "Doliczenie do zadanej liczby obiektów w pudełku",
                 (1, 4): "Niedoliczenie do zadanej liczby obiektów w pudełku",
                 (2, 3): "Przetransportowanie do punktu sprawdzenia kompletności",
                 (4, 5): "Wykrycie obiektu na taśmie 2",
                 (5, 1): "Przeniesionie obiektu do pudełka",
                 (3, 0): "Powrót do stanu początkowego"
                 }

slave_events = {(0, 1): "Przetransportowanie pudełka na wagę",
                (1, 2): "Wykrycie nieprawidłowej wagi pudełka",
                (1, 3): "Poprawne przejście testu wagi",
                (2, 3): "Zatwierdzenie procesu pakowania",
                (2, 4): "Potwierdzenie błędu procesu pakowania"
                }

current_master_state = 0
current_slave_state = 0
transitions_to_slave = [3]
transitions_to_master = [3, 4]
current_display = 'master'

#Sprawdzanie przykładowej tranzycji
check_model(a, "Obiekt wykryty na taśmie 2", "Stacja niegotowa do pracy")

print('                    PROJEKT')
print('-------------------------------------------------')
print(' Proces pakowania obiektów na linii produkcyjnej')
print('-------------------------------------------------')

while True:
    for transition in transitions_to_slave:
        if current_master_state == transition and current_display == 'master':
            current_display = 'slave'
            print('\nAktualny stan:')
            print(f'[{current_master_state}] {master_states[current_master_state]}')
            print('\n-------------------------------------------------')
            print('Przejście do podprocesu sprawdzania kompletności')
            print('-------------------------------------------------')
            current_slave_state = 0
            draw_graph(master_states[current_master_state], slave_states[current_slave_state])

    for transition in transitions_to_master:
        if current_slave_state == transition and current_display == 'slave':
            current_display = 'master'
            print('\nAktualny stan:')
            print(f'[{current_slave_state}] {slave_states[current_slave_state]}')
            print('\n-------------------------------------------------')
            print('Przejście do procesu głównego')
            print('-------------------------------------------------')
            current_master_state = 0
            draw_graph(master_states[current_master_state], slave_states[current_slave_state])

    if current_display == 'master':
        print('\nAktualny stan:')
        print(f'[{current_master_state}] {master_states[current_master_state]}')
        draw_graph(master_states[current_master_state], slave_states[current_slave_state])
        print('\nDostępne zdarzenia:')
        available_states = master_form_to[current_master_state][1]
        for state in available_states:
            print(f'[{state}] {master_events[current_master_state, state]}')

        while True:
            try:
                bufor = int(input('\nWybierz numer zdarzenia do którego chcesz przejść: '))
                is_valid(available_states, bufor)
                current_master_state = bufor
                break
            except ValueError:
                print('BŁĄD: Podaj dopuszczalne zdarzenie')

    elif current_display == 'slave':
        print('\nAktualny stan:')
        print(f'[{current_slave_state}] {slave_states[current_slave_state]}')
        draw_graph(master_states[current_master_state], slave_states[current_slave_state])
        print('\nDostępne zdarzenia:')
        available_states = slave_form_to[current_slave_state][1]
        for state in available_states:
            print(f'[{state}] {slave_events[current_slave_state, state]}')

        while True:
            try:
                bufor = int(input('\nWybierz numer zdarzenia do którego chcesz przejść: '))
                is_valid(available_states, bufor)
                current_slave_state = bufor
                break
            except ValueError:
                print('BŁĄD: Podaj dopuszczalne zdarzenie')