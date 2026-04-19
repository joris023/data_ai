import numpy as np
import matplotlib.pyplot as plt

def plot_results(results: dict[str, list[float]], runs: int) -> None:
    colors = ['tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple']
    
    plt.figure(figsize=(12, 6))
    for i, (name, rewards) in enumerate(results.items()):
        color = colors[i % len(colors)]
        cumavg = np.cumsum(rewards) / np.arange(1, len(rewards) + 1)
        plt.plot(cumavg, linewidth=2, label=f'{name} cumavg ({np.mean(rewards):.0f})', color=color)
        window = max(1, len(rewards) // 20)
        moving_avg = np.convolve(rewards, np.ones(window)/window, mode='valid')
        plt.plot(range(window - 1, len(rewards)), moving_avg, linewidth=2, linestyle='--', label=f'{name} moving avg ({moving_avg[-1]:.0f})', color=color, alpha=0.7)
    
    plt.xlabel('Scrum Game')
    plt.ylabel('Average end balance per player')
    plt.ylim(30_000, 120_000)
    plt.title(f'Model compare ({runs} games)')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('graph.png', dpi=150)
    plt.show()
