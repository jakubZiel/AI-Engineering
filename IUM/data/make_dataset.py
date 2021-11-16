import json


def load_json_data(file_path):
    file = open(file_path, "r")
    lines = file.readlines()

    objects = []

    for line in lines:
        objects.append(json.loads(line))

    return objects

base_path = "/media/jzielins/SD/sem6/IUM/IUM/data/raw"

users = load_json_data(base_path +  "/users.jsonl", "r")
sessions = load_json_data(base_path + "/sessions.jsonl", "r")
products = load_json_data(base_path + "/products.jsonl", "r")
deliveries = load_json_data(base_path + "/deliveries.jsonl", "r")
