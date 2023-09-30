from flask import Flask, jsonify, request
from Connect4 import Connect4Env
from stable_baselines3 import DQN
from stable_baselines3 import PPO
from flask_cors import CORS

env = Connect4Env()
app = Flask("Connect 4")
CORS(app)
model = DQN.load("./models/dqn_connect_four")


@app.route("/reset")
def get_reset_env():
    _obs, _ = env.reset()
    return jsonify({"message": "env reseted"}), 200


@app.route("/game-state")
def get_game_state():
    return jsonify(env.jsonify_game_state()), 200


@app.route("/agent-action")
def get_agent_action():
    try:
        obs = env._get_obs()
        action, _ = model.predict(obs)
        _obs, _reward, done, _truncated, info = env.step(action)
        return jsonify({"info": info, "done": done}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route("/make-action", methods=["POST"])
def post_make_action():
    try:
        data = request.get_json()
        action = data["action"]
        _obs, _reward, done, _truncated, info = env.step(action)
        return jsonify({"info": info, "done": done}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400


if __name__ == "__main__":
    app.run(port=8082, debug=True)
