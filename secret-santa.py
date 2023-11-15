# This is a sample Python script.

from raffle import Contestant
from raffle import raffleAssignments
import logging
from gmail_api import GmailAPIAccess
import pathlib

LOGFILE = './assets/log/resultado.log'
TEMPLATE_FILE = "./assets/templates/modelo_email.html"
FILE_PATH = "assets/participants/"
PARTICIPANTS_FILE = "participants.txt"
EMAIL_FROM = "amigoinvisiblesoft@correo.com"
SUBJECT = "Amigo Invisible"

def loadParticipants(fileName) -> {Contestant}:
    participants = set()
    with open(fileName, "r") as participants_file:
        for line in participants_file:
            line = line.strip()
            tokens = line.split(':')
            participant = Contestant(tokens[0], tokens[1], tokens[2], tokens[3],
                                     set(int(token) for token in tokens[4].split(',')))
            participants.add(participant)
            logging.debug(f"Persona cargada: {participant}")

        for participant in participants:
            participant.addIncompatibilites(participants)

    return participants

def printAssertions(participants: {Contestant}) -> None:
    logging.info("Normas del Sorteo")
    for participant in participants:
        if len(participant.incompatibility_list) == 0:
            logging.info(f"{participant.name} {participant.surname} puede regalar a cualquiera")
        else:
            for friend in participant.incompatible_friends:
                logging.info(f"{participant.name} {participant.surname} no puede regalar a {friend.name} {friend.surname}")

def main (test_mode=True):
    # Establecemos nivel de login acorde a modo de ejecución
    if test_mode:
        logging.basicConfig(level=logging.DEBUG, format='%(asctime)s:%(levelname)s: %(message)s')
    else:
        logging.basicConfig(level=logging.INFO, format='%(asctime)s:%(levelname)s: %(message)s',
                            filename=LOGFILE, filemode="w")

    logging.info("Cargando participantes")
    participants = loadParticipants(FILE_PATH + PARTICIPANTS_FILE)
    #I mpresion de restricciones
    printAssertions(participants)

    logging.info("Realizando Sorteo")
    assignments = raffleAssignments(participants)

    logging.info("Comunicando resultados")
    # Preparando plantilla
    template_body = open(TEMPLATE_FILE, "r").read()
    for participant, friend in assignments.items():
        participant_name = f'{participant.name} {participant.surname}'
        friend_name = f'{friend.name} {friend.surname}'
        logging.info(f"A {participant_name} le ha tocado {friend_name}")
        # Prepara datos email
        email_to = participant.email
        email_body = template_body\
            .replace("[nombre]", participant_name)\
            .replace("[amigoInvisible]",friend_name)
        logging.debug(f"email_to:{email_to},email_from:{EMAIL_FROM},subject:{SUBJECT}")
        # Envía correo sólo si no es una prueba
        if not test_mode: GmailAPIAccess.gmail_send_message(email_to,EMAIL_FROM,SUBJECT,email_body)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print("Inicio del Sorteo")
    main()
    print("Sorteo finalizado")




# See PyCharm help at https://www.jetbrains.com/help/pycharm/
