import networkx as nx
import matplotlib.pyplot as plt


def write_label(x, y, text):
    plt.text(x, y, text,
             color='green',
             fontsize=7,
             weight='bold',
             horizontalalignment='center',
             verticalalignment='center',
             bbox={'facecolor': 'white', 'alpha': 1, 'pad': 0, 'lw': 0})


def draw_graph(current_master_state, current_slave_state):
    plt.ion()
    plt.clf()
    plt.figure('Procesy', figsize=(12, 8))
    for node in a:
        if node == current_master_state:
            master_color.append('#FFA500')
        else:
            master_color.append('#C0C0C0')
    for node in b:
        if node == current_slave_state:
            slave_color.append('#FFA500')
        else:
            slave_color.append('#C0C0C0')
    nx.draw(a, **master_settings)
    nx.draw(b, **slave_settings)

    write_label(0,     -1,    "Wykrycie pudełka\nna taśmie 1")
    write_label(-0.25, -1.75, "Doliczenie do\nzadanej liczby obiektów\nw pudełku")
    write_label(0.25,  -1.75, "Niedoliczenie do\nzadanej liczby obiektów\nw pudełku")
    write_label(-0.5,  -1.5,  "Przetransportowanie\ndo punktu sprawdzenia\nkompletności")
    write_label(0.5,   -1.5,  "Wykrycie obiektu\nna taśmie 2")
    write_label(0.25,  -1.25, "Przeniesionie obiektu\ndo pudełka")
    write_label(-0.25, -0.75, "Powrót do\nstanu początkowego")

    write_label(1.25, -0.25, "Przetransportowanie\npudełka na wagę")
    write_label(1.5,  -1,    "Wykrycie\nnieprawidłowej\nwagi pudełka")
    write_label(1.25, -0.75, "Poprawne przejście\ntestu wagi")
    write_label(1.25, -1.25, "Zatwierdzenie\nprocesu pakowania")
    write_label(1.5,  -2,    "Potwierdzenie\nbłędu procesu\npakowania")

    plt.show()
    master_color.clear()
    slave_color.clear()
    plt.pause(0.1)


master_color = []
slave_color = []

master_cords = {"Stacja niegotowa do pracy": (0, -0.5),
                "Proces sprawdzania liczby obiektów": (0, -1.5),
                "Uruchomienie taśmy 1": (-0.5, -2),
                "Proces sprawdzania kompletności": (-0.5, -1),
                "Stacja oczekuje na wykrycie obiektu": (0.5, -2),
                "Obiekt wykryty na taśmie 2": (0.5, -1)
                }

master_settings = {'node_color': master_color,
                   'edge_color': 'black',
                   'node_size': 5000,
                   'width': 1,
                   'with_labels': True,
                   'pos': master_cords,
                   'node_shape': '8',
                   'font_size': 7,
                   }

master_edges = [("Stacja niegotowa do pracy", "Proces sprawdzania liczby obiektów"),
                ("Proces sprawdzania liczby obiektów", "Uruchomienie taśmy 1"),
                ("Proces sprawdzania liczby obiektów", "Stacja oczekuje na wykrycie obiektu"),
                ("Uruchomienie taśmy 1", "Proces sprawdzania kompletności"),
                ("Stacja oczekuje na wykrycie obiektu", "Obiekt wykryty na taśmie 2"),
                ("Obiekt wykryty na taśmie 2", "Proces sprawdzania liczby obiektów"),
                ("Proces sprawdzania kompletności", "Stacja niegotowa do pracy")
                ]

master_nodes = ["Stacja niegotowa do pracy",  # 1
                "Proces sprawdzania liczby obiektów",  # 2
                "Uruchomienie taśmy 1",  # 3
                "Proces sprawdzania kompletności",  # 4
                "Stacja oczekuje na wykrycie obiektu",  # 5
                "Obiekt wykryty na taśmie 2"  # 6
                ]

slave_cords = {"Proces sprawdzania kompletności": (1, 0),
               "Test wagi pudełka": (1.5, -0.5),
               "Interwencja pracownika": (1.5, -1.5),
               "Pudełko jest gotowe do wysyłki": (1, -1),
               "Pudełko jest wadliwe": (1.5, -2.5)
               }

slave_settings = {'node_color': slave_color,
                  'edge_color': 'black',
                  'node_size': 5000,
                  'width': 1,
                  'with_labels': True,
                  'pos': slave_cords,
                  'node_shape': '8',
                  'font_size': 7,
                  }

slave_edges = {("Proces sprawdzania kompletności", "Test wagi pudełka"),
               ("Test wagi pudełka", "Interwencja pracownika"),
               ("Test wagi pudełka", "Pudełko jest gotowe do wysyłki"),
               ("Interwencja pracownika", "Pudełko jest gotowe do wysyłki"),
               ("Interwencja pracownika", "Pudełko jest wadliwe")
               }

slave_nodes = ["Proces sprawdzania kompletności",  # 1
               "Test wagi pudełka",  # 2
               "Interwencja pracownika",  # 3
               "Pudełko jest gotowe do wysyłki",  # 4
               "Pudełko jest wadliwe"  # 5
               ]

a = nx.DiGraph()  # Proces główny
b = nx.DiGraph()  # Proces podrzędny

a.add_edges_from(master_edges)
a.add_nodes_from(master_nodes)

b.add_edges_from(slave_edges)
b.add_nodes_from(slave_nodes)