import gymnasium as gym
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from IPython.display import HTML

# Parameters
env = gym.make('FrozenLake-v1', is_slippery=False)
n_states = env.observation_space.n
n_actions = env.action_space.n
q_table = np.zeros((n_states, n_actions))
alpha = 0.1  # Learning rate
gamma = 0.9  # Discount factor
epsilon = 1.0  # Exploration rate
epsilon_min = 0.01
epsilon_decay = 0.995
n_episodes = 100000
max_steps = 1000  # Max steps per episode

# Training the Q-learning agent
for episode in range(n_episodes):
    state, _ = env.reset()  # Extract the initial state
    done = False
    steps = 0
    while not done and steps < max_steps:
        if np.random.rand() < epsilon:
            action = env.action_space.sample()  # Explore
        else:
            action = np.argmax(q_table[state])  # Exploit

        next_state, reward, done, truncated, _ = env.step(action)
        q_table[state, action] = q_table[state, action] + alpha * (reward + gamma * np.max(q_table[next_state, :]) - q_table[state, action])
        state = next_state
        steps += 1

    epsilon = max(epsilon_min, epsilon * epsilon_decay)

print('Training complete.')
print(q_table)
# Evaluate the trained agent
def evaluate_policy(env, q_table, n_episodes=10):
    frames = []
    total_rewards = 0
    for episode in range(n_episodes):
        state, _ = env.reset()  # Extract the initial state
        done = False
        steps = 0
        while not done and steps < max_steps:
            action = np.argmax(q_table[state])
            next_state, reward, done, truncated, _ = env.step(action)
            frames.append(env.render())
            state = next_state
            total_rewards += reward
            steps += 1
    return frames, total_rewards / n_episodes

# Evaluate and collect frames
env = gym.make('FrozenLake-v1', is_slippery=False, render_mode='human')
frames, avg_reward = evaluate_policy(env, q_table, n_episodes=10)
# Extract the state value function from the Q-table
state_value_function = np.max(q_table, axis=1)

# Print the state value function in a tabular format
print("State Value Function:")
print("----------------------")
for state in range(n_states):
    print(f"State {state}: {state_value_function[state]:.2f}")
# Print the average reward
print(f'Average reward over 10 episodes: {avg_reward}')

# Function to update the frame for animation
def update_frame(num, frames, ax):
    ax.clear()
    ax.imshow(frames[num])
    ax.set_xticks([])
    ax.set_yticks([])

# Create a figure for plotting
fig, ax = plt.subplots()
ani = animation.FuncAnimation(fig, update_frame, fargs=(frames, ax), frames=len(frames), interval=100)

# Display the animation
HTML(ani.to_jshtml())

# Save animation
ani.save('frozen_lake_animation-determ.mp4', fps=30)