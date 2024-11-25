from flask import Flask, request, jsonify
import pandas as pd
import numpy as np
import requests

app = Flask(__name__)

# 초기 데이터: pandas DataFrame으로 관리
data = pd.DataFrame({
    "id": [1, 2, 3],
    "name": ["Alice", "Bob", "Charlie"],
    "age": [25, 30, 35]
})

# 자동 증가 ID
next_id = data["id"].max() + 1 if not data.empty else 1


@app.route('/users', methods=['GET'])
def get_users():
    """모든 사용자 조회"""
    return jsonify(data.to_dict(orient="records"))


@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """특정 사용자 조회"""
    user = data[data["id"] == user_id]
    if user.empty:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user.iloc[0].to_dict())


@app.route('/users', methods=['POST'])
def create_user():
    """새 사용자 추가"""
    global data, next_id
    user = request.json
    if not user.get("name") or not user.get("age"):
        return jsonify({"error": "Invalid input"}), 400

    new_user = {
        "id": next_id,
        "name": user["name"],
        "age": user["age"]
    }
    next_id += 1
    data = pd.concat([data, pd.DataFrame([new_user])], ignore_index=True)
    return jsonify(new_user), 201


@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    """사용자 정보 수정"""
    global data
    user = data[data["id"] == user_id]
    if user.empty:
        return jsonify({"error": "User not found"}), 404

    update_data = request.json
    data.loc[data["id"] == user_id, "name"] = update_data.get("name", user["name"].values[0])
    data.loc[data["id"] == user_id, "age"] = update_data.get("age", user["age"].values[0])
    return jsonify(data[data["id"] == user_id].iloc[0].to_dict())


@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """사용자 삭제"""
    global data
    if data[data["id"] == user_id].empty:
        return jsonify({"error": "User not found"}), 404

    data = data[data["id"] != user_id]
    return jsonify({"message": "User deleted"}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
