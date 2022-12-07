import logging
import random


class Contestant:

    id: int

    def __init__(self, id: int, name: str, surname: str, email:str, incompatibility_list: {int}):
        self.id = id
        self.name = name
        self.surname = surname
        self.email = email
        self.incompatibility_list = incompatibility_list
        self.incompatible_friends = set()

    def __str__(self) -> str:
        tostr = "{}:{} {}:{}:{}"
        return tostr.format(self.id,self.name,self.surname,self.email,self.incompatibility_list)

    def __hash__(self) -> int:
        return int(self.id)

    def __eq__(self, other) -> bool:
        return self.id == other.id

    def addIncompatibilites(self, contestants) -> None:
        '''
        Rellena la lista de incompatibilidades de Objetos
        :param contestants:
        :return: Nada
        '''
        for id in self.incompatibility_list:
            added = False
            for contestant in contestants:
                if int(contestant.id) == id:
                    self.incompatible_friends.add(contestant)
                    added = True
            if not added:
                raise Exception("No se encontró el amigo con id {} ".format(id))

class NoCandidatesLeft(Exception):
    '''
    No more candidates left in the raffle
    :param Exception:
    :return:
    '''
    pass

class RaffleExhausted(Exception):
    '''
    The Raffle has been executed many times without success
    :param Exception:
    :return:
    '''
    pass


def raffleAssignments(participants: {Contestant}) -> {Contestant, Contestant}:
    '''
    Realiza el sorteo asignando un amigo a cada participante
    :param participants:
    :return: Diccionario de parejas de amigos invisibles
    '''
    #creamos una variable resultado inicialmente vacía
    resultado = {Contestant: Contestant}

    ended = False
    raffle_round=0
    while raffle_round <50 and not ended:
        try:
            backlog = participants.copy()

            for participant in participants:
                logging.debug("Buscando amigo para {} {}".format(participant.name, participant.surname))
                candidates = backlog.copy()
                candidates.discard(participant)
                assigned_friend = chooseFriend(candidates, participant.incompatible_friends)
                resultado[participant] = assigned_friend
                backlog.remove(assigned_friend)
                logging.debug("\t\t{}".format(assigned_friend))
            logging.debug("Asignación finalizada correctamente")
            ended = True
        except NoCandidatesLeft:
            logging.debug("No quedan candidatos, sorteo agotado")
            raffle_round += 1
            resultado.clear()

    if raffle_round == 50:
        raise RaffleExhausted("No se pudo resolver el sorteo, quizás las condiciones" +
                              " de incompatibilidad no se puedan resolver")

    return resultado

def chooseFriend(candidates: {Contestant}, incompatible_friends: {Contestant}):
    candidates = candidates - incompatible_friends

    numero_candidatos = len(candidates)
    if numero_candidatos == 0:
        raise NoCandidatesLeft("No quedan candidatos")

    selected_index = random.randint(1, numero_candidatos)
    for i in range(selected_index):
        assigned_friend = candidates.pop()

    return assigned_friend
def cleanCandidates(candidates, incompatibility_list):
    for candidate in candidates:
        if candidate.id in incompatibility_list:
            candidates.remove(candidate)
