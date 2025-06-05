import random
import heapq
import matplotlib.pyplot as plt
import math
import copy
import time
import csv
class Task:
    def __init__(self, idx, r, p, q):
        self.idx = idx
        self.r = r
        self.p = p
        self.q = q
        self.remaining_p = p  

def generate_instance(n, Z, X=29):
    random.seed(Z)
    tasks = []
    p_list = [random.randint(1, 29) for _ in range(n)]
    A = sum(p_list)
    for j in range(n):
        r = random.randint(1, A)
        q = random.randint(1, X)
        tasks.append(Task(j, r, p_list[j], q))
    return tasks

if __name__ == "__main__":
    
    tasks = generate_instance(n=6, Z=42)

    
    fig, ax = plt.subplots(figsize=(10, 2 + len(tasks)))
    for i, task in enumerate(tasks):
        y = i * 10
        
        ax.plot([task.r, task.r], [y, y + 9], color='black', linestyle='--')
        
        ax.broken_barh([(task.r, task.p)], (y, 9), facecolors='tab:blue')
        
        ax.broken_barh([(task.r + task.p, task.q)], (y, 9), facecolors='tab:orange', alpha=0.6)
        
        ax.text(task.r + task.p / 2, y + 4.5, f"T{task.idx}", ha='center', va='center', color='white')
        ax.text(task.r + task.p + task.q / 2, y + 4.5, f"+q", ha='center', va='center', color='black', fontsize=8)

    ax.set_xlabel("Czas")
    ax.set_yticks([task.idx * 10 + 4.5 for task in tasks])
    ax.set_yticklabels([f"Zadanie {task.idx}" for task in tasks])
    ax.set_title("Wizualizacja instancji problemu RPQ (r, p, q)")
    ax.grid(True)
    plt.tight_layout()
    plt.show()

def visualize_results(csv_file='wyniki_symulowanego_wyzarzania.csv'):
    import pandas as pd
    import seaborn as sns

    df = pd.read_csv(csv_file)

    plt.figure(figsize=(12, 6))
    sns.lineplot(data=df, x='T_init', y='Cmax', hue='alpha', style='max_iter', markers=True, dashes=False)
    plt.title("Wpływ parametrów SA na Cmax")
    plt.xlabel("Temperatura początkowa (T_init)")
    plt.ylabel("Cmax")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    plt.figure(figsize=(12, 6))
    sns.lineplot(data=df, x='T_init', y='Czas', hue='alpha', style='max_iter', markers=True, dashes=False)
    plt.title("Wpływ parametrów SA na czas wykonania")
    plt.xlabel("Temperatura początkowa (T_init)")
    plt.ylabel("Czas [s]")
    plt.grid(True)
    plt.tight_layout()
    plt.show()


visualize_results()




def calculate_cmax_order(tasks_order):
    S = [0] * len(tasks_order)
    C = [0] * len(tasks_order)
    S[0] = tasks_order[0].r
    C[0] = S[0] + tasks_order[0].p
    Cmax = C[0] + tasks_order[0].q
    for j in range(1, len(tasks_order)):
        S[j] = max(tasks_order[j].r, C[j - 1])
        C[j] = S[j] + tasks_order[j].p
        Cmax = max(Cmax, C[j] + tasks_order[j].q)
    return Cmax, S

def simulated_annealing(tasks, T_init=1000, alpha=0.95, stopping_T=1e-3, max_iter=1000):
    current_solution = tasks[:]
    best_solution = current_solution[:]
    best_cost, _ = calculate_cmax_order(best_solution)
    T = T_init
    while T > stopping_T:
        for _ in range(max_iter):
            i, j = random.sample(range(len(tasks)), 2)
            new_solution = current_solution[:]
            new_solution[i], new_solution[j] = new_solution[j], new_solution[i]
            new_cost, _ = calculate_cmax_order(new_solution)
            current_cost, _ = calculate_cmax_order(current_solution)
            delta = new_cost - current_cost
            if delta < 0 or random.random() < math.exp(-delta / T):
                current_solution = new_solution
                if new_cost < best_cost:
                    best_cost = new_cost
                    best_solution = new_solution
        T *= alpha
    return best_solution, best_cost

if __name__ == "__main__":
    tasks = generate_instance(n=6, Z=42)
    final_order, final_cmax = simulated_annealing(tasks)
    print("Najlepsza kolejność:", [task.idx for task in final_order])
    print("Cmax:", final_cmax)

    
    fig, ax = plt.subplots(figsize=(10, 2 + len(final_order)))
    _, start_times = calculate_cmax_order(final_order)
    for i, (task, start) in enumerate(zip(final_order, start_times)):
        y = i * 10
        ax.broken_barh([(start, task.p)], (y, 9), facecolors='tab:green')
        ax.broken_barh([(start + task.p, task.q)], (y, 9), facecolors='tab:orange', alpha=0.6)
        ax.text(start + task.p / 2, y + 4.5, f"T{task.idx}", ha='center', va='center', color='white')
    ax.set_xlabel("Czas")
    ax.set_yticks([i * 10 + 4.5 for i in range(len(final_order))])
    ax.set_yticklabels([f"Zadanie {task.idx}" for task in final_order])
    ax.set_title("Symulowane wyżarzanie - harmonogram RPQ")
    ax.grid(True)
    plt.tight_layout()
    plt.show()


# Eksperymenty z parametrami symulowanego wyżarzania
def run_experiments():
    param_grid = {
        'T_init': [10, 100, 1000, 10000],
        'alpha': [0.85, 0.90, 0.95],
        'max_iter': [100, 500, 1000]
    }

    with open('wyniki_symulowanego_wyzarzania.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Z', 'T_init', 'alpha', 'max_iter', 'Cmax', 'Czas'])

        for Z in [1, 42, 123]:
            for T_init in param_grid['T_init']:
                for alpha in param_grid['alpha']:
                    for max_iter in param_grid['max_iter']:
                        tasks = generate_instance(n=20, Z=Z)
                        start_time = time.time()
                        solution, cmax = simulated_annealing(tasks, T_init=T_init, alpha=alpha, max_iter=max_iter)
                        elapsed_time = time.time() - start_time
                        writer.writerow([Z, T_init, alpha, max_iter, cmax, elapsed_time])

run_experiments()