import random
import heapq
import matplotlib.pyplot as plt
#test
class Task:
    def __init__(self, idx, r, p, q):
        self.idx = idx
        self.r = r
        self.p = p
        self.q = q
        self.remaining_p = p  # for preemptive version

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
    # Generate a small instance
    tasks = generate_instance(n=6, Z=42)

    # Create a visualization of task parameters
    fig, ax = plt.subplots(figsize=(10, 2 + len(tasks)))
    for i, task in enumerate(tasks):
        y = i * 10
        # Mark release time
        ax.plot([task.r, task.r], [y, y + 9], color='black', linestyle='--')
        # Execution period
        ax.broken_barh([(task.r, task.p)], (y, 9), facecolors='tab:blue')
        # Delivery period
        ax.broken_barh([(task.r + task.p, task.q)], (y, 9), facecolors='tab:orange', alpha=0.6)
        # Labels
        ax.text(task.r + task.p / 2, y + 4.5, f"T{task.idx}", ha='center', va='center', color='white')
        ax.text(task.r + task.p + task.q / 2, y + 4.5, f"+q", ha='center', va='center', color='black', fontsize=8)

    ax.set_xlabel("Czas")
    ax.set_yticks([task.idx * 10 + 4.5 for task in tasks])
    ax.set_yticklabels([f"Zadanie {task.idx}" for task in tasks])
    ax.set_title("Wizualizacja instancji problemu RPQ (r, p, q)")
    ax.grid(True)
    plt.tight_layout()
    plt.show()


# --- Simulated Annealing for 1|rj, qj|Cmax ---
import math
import copy

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

    # Plot final schedule
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