from statemachine import State, Transition
from nx import *


def is_valid(available_states, test_state):
    for state in available_states:
        if state == test_state:
            return True
    raise ValueError('Zła wartość')


# define states for a master (way of passing args to class)
master_options = [
    {"name": "Stacja niegotowa do pracy",
     "initial": True,
     "value": "Stacja niegotowa do pracy"}, #0

    {"name": "Proces sprawdzania liczby obiektów",
     "initial": False,
     "value": "Proces sprawdzania liczby obiektów"}, #1

    {"name": "Uruchomienie taśmy 1",
     "initial": False,
     "value": "Uruchomienie taśmy 1"}, #2

    {"name": "Proces sprawdzania kompletności",
     "initial": False,
     "value": "Proces sprawdzania kompletności"}, #3

    {"name": "Stacja oczekuje na wykrycie obiektu",
     "initial": False,
     "value": "Stacja oczekuje na wykrycie obiektu"}, #4

    {"name": "Obiekt wykryty na taśmie 2",
     "initial": False,
     "value": "Obiekt wykryty na taśmie 2"}] #5

slave_options = [
    {"name": "Proces sprawdzania kompletności",
     "initial": True,
     "value": "Proces sprawdzania kompletności"}, #0

    {"name": "Test wagi pudełka",
     "initial": False,
     "value": "Test wagi pudełka"}, #1

    {"name": "Interwencja pracownika",
     "initial": False,
     "value": "Interwencja pracownika"}, #2

    {"name": "Pudełko jest gotowe do wysyłki",
     "initial": False,
     "value": "Pudełko jest gotowe do wysyłki"}, #3

    {"name": "Pudełko jest wadliwe",
     "initial": False,
     "value": "Pudełko jest wadliwe"}] #4

# create State objects for a master
# ** -> unpack dict to args
master_states = [State(**opt) for opt in master_options]
slave_states = [State(**opt) for opt in slave_options]

# valid transitions for a master (indices of states from-to)
master_form_to = [
    [0, [1]],
    [1, [2, 4]],
    [2, [3, 0]],
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

# create transitions for a master (as a dict)
master_transitions = {}

for indices in master_form_to:
    from_idx, to_idx_tuple = indices  # unpack list of two elements into separate from_idx and to_idx_tuple
    for to_idx in to_idx_tuple:  # iterate over destinations from a source state
        op_identifier = "m_{}_{}".format(from_idx, to_idx)  # parametrize identifier of a transition

        # create transition object and add it to the master_transitions dict
        transition = Transition(master_states[from_idx], master_states[to_idx], identifier=op_identifier)
        master_transitions[op_identifier] = transition

        # add transition to source state
        master_states[from_idx].transitions.append(transition)

slave_transitions = {}

for indices in slave_form_to:
    from_idx, to_idx_tuple = indices  # unpack list of two elements into separate from_idx and to_idx_tuple
    for to_idx in to_idx_tuple:  # iterate over destinations from a source state
        op_identifier = "m_{}_{}".format(from_idx, to_idx)  # parametrize identifier of a transition

        # create transition object and add it to the master_transitions dict
        transition = Transition(slave_states[from_idx], slave_states[to_idx], identifier=op_identifier)
        slave_transitions[op_identifier] = transition

        # add transition to source state
        slave_states[from_idx].transitions.append(transition)


# create paths from transitions (exemplary)
master_path_1 = ["m_0_1", "m_1_2", "m_2_3", "m_3_0"]
master_path_2 = ["m_0_1", "m_1_4", "m_4_5", "m_5_1"]
master_path_3 = ["m_0_1", "m_1_2", "m_2_0"]

slave_path_1 = ["m_0_1", "m_1_2", "m_2_3"]
slave_path_2 = ["m_0_1", "m_1_3"]
slave_path_3 = ["m_0_1", "m_1_2", "m_2_4"]

master_paths = [master_path_1, master_path_2, master_path_3]
slave_paths = [slave_path_1, slave_path_2, slave_path_3]

current_master_state = 0
current_slave_state = 0
transitions_to_slave = [3]
transitions_to_master = [3, 4]
current_display = 'master'


print('                    PROJEKT')
print('-------------------------------------------------')
print(' Proces pakowania obiektów na linii produkcyjnej')
print('-------------------------------------------------')

while True:
    for transition in transitions_to_slave:
        if current_master_state == transition:
            current_display = 'slave'
            print('\n-------------------------------------------------')
            print('Przejście do podprocesu sprawdzania kompletności')
            print('-------------------------------------------------')
            current_master_state = 0
            draw_master_graph(master_states[current_master_state].value)

    for transition in transitions_to_master:
        if current_slave_state == transition:
            current_display = 'master'
            print('\n-------------------------------------------------')
            print('Przejście do procesu głównego')
            print('-------------------------------------------------')
            current_slave_state = 0
            draw_slave_graph(slave_states[current_slave_state].value)

    if current_display == 'master':
        print('\nAktualny stan:')
        print(f'[{current_master_state}] {master_states[current_master_state].value}')
        draw_master_graph(master_states[current_master_state].value)
        print('\nDostępne stany:')
        available_states = master_form_to[current_master_state][1]
        for state in available_states:
            print(f'[{state}] {master_states[state].value}')

        while True:
            try:
                bufor = int(input('\nWybierz numer stanu do którego chcesz przejść: '))
                is_valid(available_states, bufor)
                current_master_state = bufor
                break
            except ValueError:
                print('BŁĄD: Podaj dopuszczalny stan')

    elif current_display == 'slave':
        print('\nAktualny stan:')
        print(f'[{current_slave_state}] {slave_states[current_slave_state].value}')
        draw_slave_graph(slave_states[current_slave_state].value)
        print('\nDostępne stany:')
        available_states = slave_form_to[current_slave_state][1]
        for state in available_states:
            print(f'[{state}] {slave_states[state].value}')

        while True:
            try:
                bufor = int(input('\nWybierz numer stanu do którego chcesz przejść: '))
                is_valid(available_states, bufor)
                current_slave_state = bufor
                break
            except ValueError:
                print('BŁĄD: Podaj dopuszczalny stan')