from flask import Flask, jsonify, request
from Lobby import Lobby


app = Flask(__name__)

server_lobby = Lobby()


@app.route('/game')
def game():
    new_game = server_lobby.rooms[request.form['room_name']].game
    return jsonify(new_game.to_dict())


@app.route('/setup_card', methods=['POST'])
def setup_card():
    new_game = server_lobby.rooms[request.form['room_name']].game
    game_player_id = int(request.form['game_player_id'])
    game_player = new_game.game_players[int(game_player_id)]

    file = int(request.form['file'])
    rank = int(request.form['rank'])
    card_name = request.form['card_name']

    game_player.do_put_card_on_setup(file, rank, card_name)
    return jsonify(new_game.to_dict_for_player(game_player_id))


@app.route('/start_game', methods=['POST'])
def start_game():
    new_game = server_lobby.rooms[request.form['room_name']].game
    new_game.start_game()
    return jsonify(new_game.to_dict())


@app.route('/card_move', methods=['POST'])
def card_move():
    new_game = server_lobby.rooms[request.form['room_name']].game
    game_player_id = int(request.form['game_player_id'])
    game_player = new_game.game_players[int(game_player_id)]

    card_name = request.form['card_name']
    direction1 = request.form['direction1']
    direction2 = request.form.get('direction2', None)

    game_player.card_move(card_name, direction1, direction2)
    return jsonify(new_game.to_dict_for_player(game_player_id))


@app.route('/use_virus_checker', methods=['POST'])
def use_virus_checker():
    new_game = server_lobby.rooms[request.form['room_name']].game
    game_player_id = int(request.form['game_player_id'])
    game_player = new_game.game_players[int(game_player_id)]

    file = int(request.form['file'])
    rank = int(request.form['rank'])

    game_player.use_virus_checker(file, rank)
    return jsonify(new_game.to_dict_for_player(game_player_id))


@app.route('/place_line_boost', methods=['POST'])
def place_line_boost():
    new_game = server_lobby.rooms[request.form['room_name']].game
    game_player_id = int(request.form['game_player_id'])
    game_player = new_game.game_players[int(game_player_id)]

    file = int(request.form['file'])
    rank = int(request.form['rank'])

    game_player.place_line_boost(file, rank)
    return jsonify(new_game.to_dict_for_player(game_player_id))


@app.route('/detach_line_boost', methods=['POST'])
def detach_line_boost():
    new_game = server_lobby.rooms[request.form['room_name']].game
    game_player_id = int(request.form['game_player_id'])
    game_player = new_game.game_players[int(game_player_id)]

    file = int(request.form['file'])
    rank = int(request.form['rank'])

    game_player.detach_line_boost(file, rank)
    return jsonify(new_game.to_dict_for_player(game_player_id))


@app.route('/install_firewall', methods=['POST'])
def install_firewall():
    new_game = server_lobby.rooms[request.form['room_name']].game
    game_player_id = int(request.form['game_player_id'])
    game_player = new_game.game_players[int(game_player_id)]

    file = int(request.form['file'])
    rank = int(request.form['rank'])

    game_player.install_firewall(file, rank)
    return jsonify(new_game.to_dict_for_player(game_player_id))


@app.route('/uninstall_firewall', methods=['POST'])
def uninstall_firewall():
    new_game = server_lobby.rooms[request.form['room_name']].game
    game_player_id = int(request.form['game_player_id'])
    game_player = new_game.game_players[int(game_player_id)]

    file = int(request.form['file'])
    rank = int(request.form['rank'])

    game_player.uninstall_firewall(file, rank)
    return jsonify(new_game.to_dict_for_player(game_player_id))


@app.route('/use_404_not_found', methods=['POST'])
def use_404_not_found():
    new_game = server_lobby.rooms[request.form['room_name']].game
    game_player_id = int(request.form['game_player_id'])
    game_player = new_game.game_players[int(game_player_id)]

    first_card_name = request.form['first_card_name']
    second_card_name = request.form['second_card_name']
    switch = True if request.form['switch'] == "true" else False

    game_player.use_404_not_found(first_card_name, second_card_name, switch)
    return jsonify(new_game.to_dict_for_player(game_player_id))


@app.route('/lobby')
def lobby():
    return jsonify(server_lobby.to_dict())


@app.route('/login', methods=['POST'])
def login():

    player_username = request.form['player_username']
    server_lobby.add_player(player_username)

    return jsonify(server_lobby.to_dict())


@app.route('/lobby/create_room', methods=['POST'])
def create_room():

    player = request.form['player_username']
    room_name = request.form['room_name']
    server_lobby.create_room(player, room_name)

    return jsonify(server_lobby.to_dict())


@app.route('/lobby/initialize_room', methods=['POST'])
def complete_room():

    username = request.form['player_username']
    room_name = request.form['room_name']
    server_lobby.add_player_in_room(username, room_name)
    server_lobby.create_room_game(room_name)

    return jsonify(server_lobby.to_dict())
