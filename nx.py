import networkx as nx
import matplotlib.pyplot as plt


master_color = []
slave_color = []

master_cords = {"Stacja niegotowa do pracy": (0, 0),
                "Proces sprawdzania liczby obiektów": (0, -0.15),
                "Uruchomienie taśmy 1": (-0.5, -0.25),
                "Proces sprawdzania kompletności": (-0.5, -0.1),
                "Stacja oczekuje na wykrycie obiektu": (0.5, -0.25),
                "Obiekt wykryty na taśmie 2": (0.5, -0.1)
                }

master_options = {'node_color': master_color,
                  'edge_color': 'black',
                  'node_size': 20000,
                  'width': 0.9,
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
                ("Uruchomienie taśmy 1", "Stacja niegotowa do pracy"),
                ("Proces sprawdzania kompletności", "Stacja niegotowa do pracy")
                ]

master_nodes = ["Stacja niegotowa do pracy",  # 1
                "Proces sprawdzania liczby obiektów",  # 2
                "Uruchomienie taśmy 1",  # 3
                "Proces sprawdzania kompletności",  # 4
                "Stacja oczekuje na wykrycie obiektu",  # 5
                "Obiekt wykryty na taśmie 2"  # 6
                ]

slave_cords = {"Proces sprawdzania kompletności": (0, 0),
               "Test wagi pudełka": (0, -1),
               "Interwencja pracownika": (0, -2),
               "Pudełko jest gotowe do wysyłki": (-0.01, -1.5),
               "Pudełko jest wadliwe": (0, -3)
               }

slave_options = {'node_color': slave_color,
                 'edge_color': 'black',
                 'node_size': 16000,
                 'width': 0.9,
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

# master_labels = {("Stacja niegotowa do pracy", "Proces sprawdzania liczby obiektów"): "Wykryto pudełko na taśmie 1",
#                  ("Proces sprawdzania liczby obiektów",
#                   "Uruchomienie taśmy 1"): "Doliczono do zadanej liczby obiektów w pudełka",
#                  ("Proces sprawdzania liczby obiektów",
#                   "Stacja oczekuje na wykrycie obiektu"): "Brak zadanej liczby obiektów w pudełku",
#                  ("Uruchomienie taśmy 1",
#                   "Proces sprawdzania kompletności"): "Przetransportowano do punktu sprawdzenia kompletności",
#                  ("Stacja oczekuje na wykrycie obiektu", "Obiekt wykryty na taśmie 2"): "Wykryto obielt na taśmie 2",
#                  ("Obiekt wykryty na taśmie 2", "Proces sprawdzania liczby obiektów"): "Przeniesiono onbiekt do puedłka",
#                  ("Uruchomienie taśmy 1", "Stacja niegotowa do pracy"): "Powrót do stanu początkowego",
#                  ("Proces sprawdzania kompletności", "Stacja niegotowa do pracy"): "Powrót do stanu początkowego"
#                  }

a = nx.DiGraph()  # Proces główny
b = nx.DiGraph()  # Proces podrzędny

a.add_edges_from(master_edges)
a.add_nodes_from(master_nodes)

b.add_edges_from(slave_edges)
b.add_nodes_from(slave_nodes)


def draw_master_graph(current_state):
    plt.ion()
    plt.figure('Proces główny', figsize=(13, 9))
    for node in a:
        if node == current_state:
            master_color.append('#FFA500')
        else:
            master_color.append('#C0C0C0')
    nx.draw(a, **master_options)
    plt.show()
    master_color.clear()
    plt.pause(1)


def draw_slave_graph(current_state):
    plt.ion()
    plt.figure('Proces podrzędny', figsize=(13, 9))
    for node in b:
        if node == current_state:
            slave_color.append('#FFA500')
        else:
            slave_color.append('#C0C0C0')

    nx.draw(b, **slave_options)
    plt.show()
    slave_color.clear()
    plt.pause(1)
