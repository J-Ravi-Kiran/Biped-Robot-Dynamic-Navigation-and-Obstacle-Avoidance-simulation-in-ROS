import re
import matplotlib.pyplot as plt
import numpy as np

def generate_automated_graphs(filename="auto100trials.docx"):
    print(f"Reading data from {filename}...")
    
    try:
        with open(filename, 'r') as file:
            log_text = file.read()
    except FileNotFoundError:
        print(f"ERROR: Could not find '{filename}'. Make sure you saved your terminal text into this file!")
        return

    # --- EXTRACT DATA USING REGULAR EXPRESSIONS ---
    task_times = [float(x) for x in re.findall(r'Task Time:\s+([\d.]+)\s*s', log_text)]
    path_lengths = [float(x) for x in re.findall(r'Path Length:\s+([\d.]+)\s*m', log_text)]
    sidesteps = [int(x) for x in re.findall(r'Sidesteps:\s+(\d+)', log_text)]
    
    # Count Successes and Failures
    successes = len(task_times)
    failures = len(re.findall(r'FAILED', log_text))
    total_trials = successes + failures

    if total_trials == 0:
        print("No trial data found in the text file. Check your formatting.")
        return

    print(f"Successfully processed {total_trials} total trials ({successes} successes, {failures} failures).")
    
    # Create an array for the X-axis mapping only the successful runs
    successful_trials_x = np.arange(1, successes + 1)

    # --- GRAPH 1: System Reliability (Dual Axis Line Chart) ---
    fig, ax1 = plt.subplots(figsize=(12, 6))

    color = 'tab:blue'
    ax1.set_xlabel('Successful Trial Number', fontweight='bold')
    ax1.set_ylabel('Task Completion Time (s)', color=color, fontweight='bold')
    ax1.plot(successful_trials_x, task_times, color=color, marker='o', markersize=4, linewidth=1.5, label='Time (s)')
    ax1.tick_params(axis='y', labelcolor=color)
    
    # Clean up X-axis ticks for a large dataset like 100 runs
    ax1.set_xticks(np.arange(0, successes + 1, 10))
    ax1.grid(True, linestyle='--', alpha=0.6)

    ax2 = ax1.twinx()  
    color = 'tab:red'
    ax2.set_ylabel('Path Length (m)', color=color, fontweight='bold')
    ax2.plot(successful_trials_x, path_lengths, color=color, marker='s', markersize=4, linestyle='dashed', linewidth=1.5, alpha=0.7, label='Path (m)')
    ax2.tick_params(axis='y', labelcolor=color)

    plt.title(f'Bipedal Navigation Consistency Across {successes} Successful Trials', fontweight='bold', fontsize=14)
    fig.tight_layout()
    plt.savefig('100_system_reliability.png', dpi=300)
    print("Saved: 100_system_reliability.png")

    # --- GRAPH 2: Controller Reactivity (Scatter Plot) ---
    plt.figure(figsize=(10, 6))
    plt.scatter(sidesteps, task_times, color='purple', s=50, alpha=0.6, edgecolors='black')

    # Add a subtle trendline
    if successes > 1:
        z = np.polyfit(sidesteps, task_times, 1)
        p = np.poly1d(z)
        plt.plot(sidesteps, p(sidesteps), "r--", alpha=0.8, linewidth=2, label='Linear Trend')

    plt.title('Impact of Obstacle Avoidance on Task Duration', fontweight='bold', fontsize=14)
    plt.xlabel('Sidestep Frequency (Count)', fontweight='bold')
    plt.ylabel('Task Completion Time (s)', fontweight='bold')
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.legend()
    plt.tight_layout()
    plt.savefig('100_controller_reactivity.png', dpi=300)
    print("Saved: 100_controller_reactivity.png")

    # --- GRAPH 3: Success Rate (Pie Chart) ---
    plt.figure(figsize=(8, 8))
    labels = [f'Success ({successes})', f'Failure/Collapse ({failures})']
    sizes = [successes, failures]
    colors = ['#4CAF50', '#F44336']
    explode = (0, 0.1)  # "Explode" the failure slice slightly to highlight it

    plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%',
            shadow=True, startangle=140, textprops={'fontsize': 12, 'weight': 'bold'})
    plt.title(f'System Reliability Over {total_trials} Automated Trials', fontweight='bold', fontsize=16)
    plt.tight_layout()
    plt.savefig('100_success_rate.png', dpi=300)
    print("Saved: 100_success_rate.png")
    
    # --- PRINT SUMMARY METRICS FOR ACADEMIC TABLE ---
    print("\n" + "="*40)
    print(" SUMMARY METRICS FOR 95 SUCCESSFUL TRIALS")
    print("="*40)
    print(f"Task Time (s):   Mean = {np.mean(task_times):.2f} (SD = {np.std(task_times):.2f}) | Range: {np.min(task_times):.2f} - {np.max(task_times):.2f}")
    print(f"Path Length (m): Mean = {np.mean(path_lengths):.3f} (SD = {np.std(path_lengths):.3f}) | Range: {np.min(path_lengths):.3f} - {np.max(path_lengths):.3f}")
    print(f"Sidesteps:       Mean = {np.mean(sidesteps):.1f}  (SD = {np.std(sidesteps):.1f})  | Range: {np.min(sidesteps)} - {np.max(sidesteps)}")
    print("="*40 + "\n")

    plt.show()

if __name__ == "__main__":
    generate_automated_graphs()
