from Connect4 import Connect4Env
from stable_baselines3 import PPO


def random_play(episodes=100):
    for e in range(episodes):
        print(f"Episode : {e} of {episodes}")
        env = Connect4Env()
        obs, _ = env.reset()
        done = False

        while not done:
            print("Board :")
            print("Actual Player :", env.current_player)
            print(obs)
            action = env.action_space.sample()
            obs, reward, done, _, info = env.step(action)
            print(f"Action: {action}, Reward: {reward}, Info: {info}")
        print("=" * 15)


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
        obs, reward, done, info = env.step(action)
        print(f"Action: {action}, Reward: {reward}, Info: {info}")


def play_with_agent(agent_path):
    model = PPO.load(agent_path)
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


# random_play()
# manual_play()
play_with_agent("./models/ppo_connect_four")
