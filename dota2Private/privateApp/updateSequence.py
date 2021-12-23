def update_latest_sequence(id):
    with open('dota2Private\privateApp\lastSequence.txt', "w") as myfile:
            myfile.write(id)