# This is a sample Python script.
from Raffle.raffle import Contestant
from Raffle.raffle import raffleAssignments
import logging

# Press Mayús+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

FILE_PATH = "assets/participants/"
PARTICIPANTS_FILE = ".participants.txt"


def loadParticipants(fileName) -> {Contestant}:
    participants = set()
    with open(fileName, "r") as participants_file:
        for line in participants_file:
            line = line.strip()
            tokens = line.split(':')
            participant = Contestant(tokens[0], tokens[1], tokens[2], tokens[3],
                                     set(int(token) for token in tokens[4].split(',')))
            participants.add(participant)
            logging.debug("Persona cargada: {}".format(participant))

        for participant in participants:
            participant.addIncompatibilites(participants)

    return participants

def printAssertions(participants: {Contestant}) -> None:
    logging.info("Normas del Sorteo")
    for participant in participants:
        if len(participant.incompatibility_list) == 0:
            logging.info("{} {} puede regalar a cualquiera".format(participant.name, participant.surname))
        else:
            for friend in participant.incompatible_friends:
                logging.info("{} {} no puede regalar a {} {}"
                             .format(participant.name, participant.surname, friend.name, friend.surname))


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    logging.info("Cargando participantes")
    participants = loadParticipants(FILE_PATH + PARTICIPANTS_FILE)
    printAssertions(participants)
    logging.info("Realizando Sorteo")
    assignments = raffleAssignments(participants)
    logging.info("Comunicando resultados")



# See PyCharm help at https://www.jetbrains.com/help/pycharm/
