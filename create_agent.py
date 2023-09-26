from stable_baselines3 import PPO
from Connect4 import Connect4Env
from time import time


print("Training new UNO agent")
print("Loading environment")
env = Connect4Env()

print("Training agent with Single Agent Self Play")
start = time()
model = PPO("MlpPolicy", env, verbose=1)
model.learn(10_000_00)
end = time()

model.save("./models/ppo_connect_four")
print(f"Agent trained in {(end - start) / 60} minutes")
