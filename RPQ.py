import random
import heapq
import matplotlib.pyplot as plt

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