import numpy as np
import matplotlib.pyplot as plt

def plot_results(results: dict[str, list[float]], runs: int):
    colors = ['tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple']
    
    plt.figure(figsize=(12, 6))
    for i, (name, rewards) in enumerate(results.items()):
        color = colors[i % len(colors)]
        window = max(1, len(rewards) // 20)
        moving_avg = np.convolve(rewards, np.ones(window)/window, mode='valid')
        plt.plot(rewards, alpha=0.1, color=color)
        plt.plot(range(window - 1, len(rewards)), moving_avg, linewidth=2, label=f'{name} (avg: {np.mean(rewards):.0f})', color=color)
    
    plt.xlabel('Game')
    plt.ylabel('Gemiddeld eindbalans per speler')
    plt.ylim(45_000, 110_000)
    plt.title(f'Model Vergelijking ({runs} games)')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('comparison.png', dpi=150)
    plt.show()
    print(f"Grafiek opgeslagen als comparison.png")
