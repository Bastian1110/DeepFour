from Connect4 import Connect4Env
from stable_baselines3 import DQN


def random_play(episodes=100):
    total_time_steps = 0
    for e in range(episodes):
        print(f"Episode : {e} of {episodes}")
        env = Connect4Env()
        obs, _ = env.reset()
        done = False
        time_steps = 0

        while not done:
            print("Board :")
            print("Actual Player :", env.current_player)
            print(obs)
            action = env.action_space.sample()
            obs, reward, done, _, info = env.step(action)
            print(f"Action: {action}, Reward: {reward}, Info: {info}")
            time_steps += 1
        total_time_steps += time_steps
        print(f"Total time steps taken : {time_steps}")
        print("=" * 15)
    print(f"Average timesteps per game : {total_time_steps / episodes}")


# Super usefull function that works for debugging Connect 4 functionality
def manual_play():
    env = Connect4Env()
    obs = env.reset()
    done = False

    while not done:
        print("Board :")
        print("Actual Player :", env.current_player)
        print(obs)
        action = int(input("Enter your action: "))
        obs, reward, done, _, info = env.step(action)
        print(f"Action: {action}, Reward: {reward}, Info: {info}")


def random_play_agent(agent_path, episodes=100):
    model = DQN.load(agent_path)
    env = Connect4Env()

    for e in range(episodes):
        print(f"Episode : {e} of {episodes}")
        obs, _ = env.reset()
        done = False

        while not done:
            print("Board :")
            print("Actual Player :", env.current_player)
            print(obs)
            action, _ = model.predict(obs)
            print("Agent Action", action)
            obs, reward, done, _, info = env.step(action)
            print(f"Action: {action}, Reward: {reward}, Info: {info}")


def play_with_agent(agent_path):
    model = DQN.load(agent_path)
    env = Connect4Env()
    obs = env.reset()
    done = False

    while not done:
        print("Board :")
        print("Actual Player :", env.current_player)
        print(obs)
        if env.current_player == 2:
            action, _ = model.predict(obs)
            print("Agent Action", action)
        else:
            action = int(input("Enter your action: "))
        obs, reward, done, _, info = env.step(action)
        print(f"Action: {action}, Reward: {reward}, Info: {info}")


# random_play(episodes=1000)
manual_play()
# play_with_agent("./models/ppo_connect_four")
# random_play_agent("./models/ppo_connect_four", episodes=1)
