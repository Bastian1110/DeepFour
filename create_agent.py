from stable_baselines3 import DQN, PPO
from Connect4 import Connect4Env
from time import time


def create_ppo_agent():
    print("Training new Connect 4 PPO agent")
    print("Loading environment")
    env = Connect4Env()

    print("Training agent with Single Agent Self Play")
    start = time()
    model = PPO("MlpPolicy", env, verbose=1)
    model.learn(total_timesteps=2_500_000)

    end = time()

    model.save("./models/ppo_connect_four")
    print(f"Agent trained in {(end - start) / 60} minutes")


def create_dqn_agent():
    print("Training new Connect 4 DQN agent")
    print("Loading environment")
    env = Connect4Env()

    print("Training agent with Single Agent Self Play")
    start = time()
    model = DQN(
        "MlpPolicy",
        env,
        verbose=1,
        learning_rate=0.0005,
        buffer_size=10000,
        exploration_fraction=0.1,
        exploration_final_eps=0.02,
    )
    model.learn(total_timesteps=25_000_000)

    end = time()

    model.save("./models/dqn_connect_four")
    print(f"Agent trained in {(end - start) / 60} minutes")


create_dqn_agent()
