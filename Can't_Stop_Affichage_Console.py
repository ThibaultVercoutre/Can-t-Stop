import random

class Pion:
  def __init__(self, colonne : int, etage : int):
    self.colonne = colonne
    self.etage = etage
  def __repr__(self) -> str:
    return "Pion('" + str(self.colonne)+", "+str(self.etage) + "')"

class CombiDes:
  def __init__(self, separation : bool, combi1 : int, combi2 : int):
    self.separation = separation
    self.combi1 = combi1
    self.combi2 = combi2
  def __repr__(self) -> str:
    return "CombiDes('" + str(self.separation) + ", " + str(self.combi1) + ", " + str(self.combi2) + "')"

class Joueur:
  def __init__(self, nom : str, des : int, pions : list, grimpeurs : list):
    self.nom = nom
    self.des = des
    self.pions_restant = 0
    self.pions = pions
    self.grimpeurs_restant = 0
    self.grimpeurs = grimpeurs
    for i in range (len(grimpeurs)):
      if grimpeurs[i].colonne == 0:
        self.grimpeurs_restant += 1
    for i in range (len(pions)):
      if pions[i].colonne == 0:
        self.pions_restant += 1
  def __repr__(self) -> str:
    return ("Joueur('" + str(self.nom) + ", " + str(self.des) + ", "
            + str(self.pions_restant) + ", " + "[" + ', '.join(str(elem) for elem in self.pions) + "]" + ", "
            + str(self.grimpeurs_restant) + ", " + "[" + ', '.join(str(elem) for elem in self.grimpeurs) + "]" + "')")
    
######################################
############ Fonctions ###############
######################################

########## On lance 4 dés ############

def lancer_des() -> list:
    des = []
    for i in range (4):
        des.append(random.randint(1, 6))
    return des

############ On créé les combinaison de dés ###############

def addition(dés) -> list:
    possibilités = [CombiDes(False,dés[0]+dés[1],dés[2]+dés[3]),
                    CombiDes(False,dés[0]+dés[2],dés[1]+dés[3]),
                    CombiDes(False,dés[0]+dés[3],dés[1]+dés[2])]
    return(possibilités)
    
############ On définie la priorité des joueurs ###############

def prio(nb_j) -> int:
    prio = random.randint(1,nb_j)
    return prio

############ Test si peut placer ses pions ###########

def test_place_pion(possibilités,joueur,col):
    possibilités_finales = possibilités
    
    #Enlever les possibilités des lignes qui sont déjà finis
    
    for i in range (len(possibilités_finales)):
        
        for j in range (len(col)):
            for k in range(len(joueur.pions)):
                if possibilités_finales[i].combi1 == j+2 and joueur.pions[k].colonne == j+2 and joueur.pions[k].etage >= col[j]:
                    possibilités_finales[i].combi1 = 0
                if possibilités_finales[i].combi2 == j+2 and joueur.pions[k].colonne == j+2 and joueur.pions[k].etage >= col[j]:
                    possibilités_finales[i].combi2 = 0
                if possibilités_finales[i].combi1 == j+2 and possibilités_finales[i].combi2 == j+2 and joueur.pions[k].colonne == j+2 and joueur.pions[k].etage+2 > col[j]:
                    possibilités_finales[i].combi2 = 0
            for k in range(len(joueur.grimpeurs)):
                if possibilités_finales[i].combi1 == j+2 and joueur.grimpeurs[k].colonne == j+2 and joueur.grimpeurs[k].etage >= col[j]:
                    possibilités_finales[i].combi1 = 0
                if possibilités_finales[i].combi2 == j+2 and joueur.grimpeurs[k].colonne == j+2 and joueur.grimpeurs[k].etage >= col[j]:
                    possibilités_finales[i].combi2 = 0
                if possibilités_finales[i].combi1 == j+2 and possibilités_finales[i].combi2 == j+2 and joueur.grimpeurs[k].colonne == j+2 and joueur.grimpeurs[k].etage+2 > col[j]:
                    possibilités_finales[i].combi2 = 0
        
        #################################################### SI PIONS RESTANT >= 2 ########################################################
        
        if joueur.pions_restant >= 2:
            
            #if joueur.grimpeurs_restant >= 2:
                #On garde la poss qu'on test
                
            if joueur.grimpeurs_restant == 1:
                err = 0
                for k in range(len(joueur.grimpeurs)-joueur.grimpeurs_restant):
                    if possibilités_finales[i].combi1 != joueur.grimpeurs[k].colonne and possibilités_finales[i].combi2 != joueur.grimpeurs[k].colonne and joueur.grimpeurs[k].colonne != 0:
                        err += 1
                if err == len(joueur.grimpeurs)-joueur.grimpeurs_restant:
                    if possibilités_finales[i].combi1 != possibilités_finales[i].combi2:
                        #On sépare les poss
                        possibilités_finales[i].separation = True
                    #else:
                        #On garde la poss non separe si les deux poss sont =
                        
            if joueur.grimpeurs_restant == 0:
                poss_tempo = []
                for k in range(len(joueur.grimpeurs)):
                    if possibilités_finales[i].combi1 == joueur.grimpeurs[k].colonne and joueur.grimpeurs[k].colonne != 0:
                        poss_tempo.append(possibilités_finales[i].combi1)
                    if possibilités_finales[i].combi2 == joueur.grimpeurs[k].colonne and joueur.grimpeurs[k].colonne != 0:
                        poss_tempo.append(possibilités_finales[i].combi2)
                if len(poss_tempo) == 1:
                    possibilités_finales[i].combi1 = poss_tempo[0]
                    possibilités_finales[i].combi2 = 0
                if len(poss_tempo) == 0:
                    possibilités_finales[i].combi1 = 0
                    possibilités_finales[i].combi2 = 0
                    #else:
                        #On garde tout
                        
        #################################################### SI PIONS RESTANT == 1 ########################################################
        if joueur.pions_restant == 1:
            if joueur.grimpeurs_restant >= 2:
                err1 = 0
                corr = []
                for j in range (len(joueur.pions)):
                    #Si une des possibilité correspond à un pion
                    if (possibilités_finales[i].combi1 == joueur.pions[j].colonne or possibilités_finales[i].combi2 == joueur.pions[j].colonne) and joueur.pions[j].colonne != 0:
                        err2 = 0
                        for k in range (len(joueur.pions)):
                            #Si le premier grimpeur est déjà enregistré dans les pions, la dernière place est toujours libre
                            if joueur.grimpeurs[0].colonne == joueur.pions[k].colonne and joueur.pions[k].colonne != 0:
                                #Donc pas besoin de séparer les poss car la place est tjrs libre
                                possibilités_finales[i].separation = False
                            else:
                                err2 += 1
                        #Si le premier grimpeur prend la dernière place
                        if err2 == len(joueur.pions)-1:
                            if possibilités_finales[i].combi1 == joueur.pions[j].colonne:
                                corr.append(possibilités_finales[i].combi1)
                            if possibilités_finales[i].combi2 == joueur.pions[j].colonne:
                                corr.append(possibilités_finales[i].combi2)
                    #Sinon on ajoute une erreur
                    else:
                        err1 += 1
                #Si il a a corr (donc au moins une des deux poss corr à un pion enregistré, et que la place n'est pas libre)
                if corr != []:
                    if len(corr) == 1:
                        if corr[0] != possibilités_finales[i].combi1:
                            possibilités_finales[i].combi1 = 0
                        if corr[0] != possibilités_finales[i].combi2:
                            possibilités_finales[i].combi2 = 0
                    if len(corr) == 2:
                        if corr[0] != possibilités_finales[i].combi1 and corr[1] != possibilités_finales[i].combi1:
                            possibilités_finales[i].combi1 = 0
                        if corr[0] != possibilités_finales[i].combi2 and corr[1] != possibilités_finales[i].combi2:
                            possibilités_finales[i].combi2 = 0
                            
                #Si aucune poss correspond à aucun pion
                if err1 == len(joueur.pions):
                    err2 = 0
                    for k in range (len(joueur.pions)):
                        #Si le premier grimpeur est déjà enregistré dans les pions, la dernière place est toujours libre
                        if joueur.grimpeurs[0].colonne == joueur.pions[k].colonne and joueur.pions[k].colonne != 0:
                            #Donc on sépare les poss car il ne reste qu'une place
                            possibilités_finales[i].separation = True
                        else:
                            err2 += 1
                    #Si le premier grimpeurs sera enregistré dans la place libre, on ne peut pas placer les poss       
                    if err2 == len(joueur.pions):
                        possibilités_finales[i].combi1 = 0
                        possibilités_finales[i].combi2 = 0
            
            if joueur.grimpeurs_restant == 1:
                err1 = 0
                for j in range (len(joueur.pions)):
                    #Si une des deux possibilités corresponde
                    if (possibilités_finales[i].combi1 == joueur.pions[j].colonne or possibilités_finales[i].combi2 == joueur.pions[j].colonne) and joueur.pions[j].colonne != 0:
                        corr = 0
                        err2 = 0
                        #On veut savoir cb de ces grimpeurs sont déjà dans les pions
                        for k in range (len(joueur.pions)):
                            if (joueur.grimpeurs[1].colonne == joueur.pions[k].colonne or joueur.grimpeurs[2].colonne == joueur.pions[k].colonne) and joueur.pions[k].colonne != 0:
                                corr += 1
                            else:
                                err2 += 1
                        #Si les deux grimpeurs sont déjà enregistrés (il reste la place libre)
                        if corr == 2:
                            corr1 = 0
                            #On veut savoir si les poss peut correspondre aux grimpeurs
                            for k in range(len(joueur.grimpeurs)):
                                if possibilités_finales[i].combi1 == joueur.grimpeurs[k]:
                                    corr1 += 1
                                if possibilités_finales[i].combi2 == joueur.grimpeurs[k]:
                                    corr1 += 1
                            #Si aucune poss ne corr au grimpeurs
                            if corr1 == 0:
                                possibilités_finales[i].separation = True
                        #Si un des grimpeurs prend la place libre
                        if corr == 1:
                            corr1 = 0
                            #On veut savoir si les poss peut correspondre aux grimpeurs
                            for k in range(len(joueur.grimpeurs)):
                                if possibilités_finales[i].combi1 == joueur.grimpeurs[k]:
                                    corr1 += 1
                                if possibilités_finales[i].combi2 == joueur.grimpeurs[k]:
                                    corr1 += 1
                            #Si aucune poss ne corr au grimpeurs
                            if corr1 == 1 or corr1 == 0:
                                possibilités_finales[i].separation = True
                                #Supprimer les poss qui ne sont pas déjà enregistrées
                                lst_corr = []
                                for k in range(len(joueur.pions)):
                                    if possibilités_finales[i].combi1 == joueur.pions[k]:
                                        lst_corr.append(possibilités_finales[i].combi1)
                                    if possibilités_finales[i].combi2 == joueur.pions[k]:
                                        lst_corr.append(possibilités_finales[i].combi2)
                                #Si il y a correspondance
                                if lst_corr != []:
                                    if len(lst_corr) == 1:
                                        if possibilités_finales[i].combi1 != lst_corr[0]:
                                            possibilités_finales[i].combi1 = 0
                                        if possibilités_finales[i].combi2 != lst_corr[0]:
                                            possibilités_finales[i].combi2 = 0
                                    if len(lst_corr) == 2:
                                        possibilités_finales[i].separation = True
                            if corr1 == 2:
                                possibilités_finales[i].separation = False
                        
                    else:
                        err1 += 1
                #Si aucune des poss ne corresponde au pions
                if err1 == len(pions):
                    #On veut savoir cb de grimpeurs corresponde aux pions
                    for k in range (1,len(pions)):
                        #Si l'un des deux grimpeurs correspond
                        if (joueur.grimpeurs[1].colonne == joueur.pions[k].colonne or joueur.grimpeurs[2].colonne == joueur.pions[k].colonne) and joueur.pions[k].colonne != 0:
                            corr += 1
                        else:
                            err2 += 1
                    #Si les deux grimpeurs correspondent aux pions (il reste toujours une place)
                    if corr == 2:
                        #On veut savoir si les poss peuvent correspondre
                        corr3 = 0
                        for k in range(len(joueur.grimpeurs)):
                            if possibilités_finales[i].combi1 == joueur.grimpeur[k].colonne:
                                corr3 += 1
                            if possibilités_finales[i].combi2 == joueur.grimpeut[k].colonne:
                                corr3 += 1
                        if corr3 == 2 or corr3 == 1:
                            possibilités_finales[i].separation = False
                        else:
                            possibilités_finales[i].separation = True
        
            if  joueur.grimpeurs_restant == 0:
                poss_tempo = []
                for k in range(len(joueur.grimpeurs)):
                    #Si l'une des deux possibilité correspond
                    if possibilités_finales[i].combi1 == joueur.grimpeurs[k].colonne:
                        poss_tempo.append(possibilités_finales[i].combi1)
                    if possibilités_finales[i].combi1 == joueur.grimpeurs[k].colonne:
                        poss_teempo.append(possibilités_finales[i].combi2)
                        
                if len(poss_tempo) == 1:
                    if poss_tempo[0] != possibilités_finales[i].combi1:
                        possibilités_finales[i].combi1 = 0
                    if poss_tempo[0] != possibilités_finales[i].combi2:
                        possibilités_finales[i].combi2 = 0
                    
        #################################################### SI PIONS RESTANT == 0 ########################################################
        
        if joueur.pions_restant == 0:
            if joueur.grimpeurs_restant >= 2:
                poss_tempo = []
                for k in range (len(joueur.pions)):
                    if possibilités_finales[i].combi1 == joueur.pions[k].colonne:
                        poss_tempo.append(possibilités_finales[i].combi1)
                    if possibilités_finales[i].combi2 == joueur.pions[k].colonne:
                        poss_tempo.append(possibilités_finales[i].combi2)
                
                if len(poss_tempo) == 1:
                    if possibilités_finales[i].combi1 != poss_tempo[0]:
                        possibilités_finales[i].combi1 = 0
                    if possibilités_finales[i].combi2 != poss_tempo[0]:
                        possibilités_finales[i].combi2 = 0
                if len(poss_tempo) == 0:
                    possibilités_finales[i].combi1 = 0
                    possibilités_finales[i].combi2 = 0
                
            if joueur.grimpeurs_restant == 1:
                poss_tempo = []
                for k in range (len(joueur.pions)):
                    if possibilités_finales[i].combi1 == joueur.pions[k].colonne:
                        poss_tempo.append(possibilités_finales[i].combi1)
                    if possibilités_finales[i].combi2 == joueur.pions[k].colonne:
                        poss_tempo.append(possibilités_finales[i].combi2)
                
                if len(poss_tempo) == 1:
                    if possibilités_finales[i].combi1 != poss_tempo[0]:
                        possibilités_finales[i].combi1 = 0
                    if possibilités_finales[i].combi2 != poss_tempo[0]:
                        possibilités_finales[i].combi2 = 0
                if len(poss_tempo) == 0:
                    possibilités_finales[i].combi1 = 0
                    possibilités_finales[i].combi2 = 0
                
                poss_tempo = []
                for k in range(len(joueur.grimpeurs)):
                    if possibilités_finales[i].combi1 == joueur.grimpeurs[k].colonne:
                        poss_tempo.append(possibilités_finales[i].combi1)
                    if possibilités_finales[i].combi2 == joueur.grimpeurs[k].colonne:
                        poss_tempo.append(possibilités_finales[i].combi2)
                
                if len(poss_tempo) == 0:
                    possibilités_finales[i].separation = True
            
            if joueur.grimpeurs_restant == 0:
                poss_tempo = []
                for k in range (len(joueur.pions)):
                    if possibilités_finales[i].combi1 == joueur.pions[k].colonne:
                        poss_tempo.append(possibilités_finales[i].combi1)
                    if possibilités_finales[i].combi2 == joueur.pions[k].colonne:
                        poss_tempo.append(possibilités_finales[i].combi2)
                
                if len(poss_tempo) == 1:
                    if possibilités_finales[i].combi1 != poss_tempo[0]:
                        possibilités_finales[i].combi1 = 0
                    if possibilités_finales[i].combi2 != poss_tempo[0]:
                        possibilités_finales[i].combi2 = 0
                if len(poss_tempo) == 0:
                    possibilités_finales[i].combi1 = 0
                    possibilités_finales[i].combi2 = 0
                    
                poss_tempo = []
                for k in range(len(joueur.grimpeurs)):
                    if possibilités_finales[i].combi1 == joueur.grimpeurs[k].colonne:
                        poss_tempo.append(possibilités_finales[i].combi1)
                    if possibilités_finales[i].combi2 == joueur.grimpeurs[k].colonne:
                        poss_tempo.append(possibilités_finales[i].combi2)
                
                if len(poss_tempo) == 0 or len(poss_tempo) == 1:
                    possibilités_finales[i].combi1 = 0
                    possibilités_finales[i].combi2 = 0
            
        if possibilités_finales[i].combi1 == possibilités_finales[i].combi2:
            possibilités_finales[i].separation = False
    
    
    return possibilités_finales
    
############ boucle de jeu ##############

def trois_lignes_complete(joueur,colonne):
  res = 0
  for i in range(joueur.pions_restant):
    for j in range(len(colonne)):
      if j+2 == joueur.pions[i].colonne and colonne[j] == joueur.pions[i].etage:
        res += 1
  return res

def trois_grimpeurs_complete(joueur,colonne):
  res = 0
  for i in range(joueur.grimpeurs_restant):
    for j in range(len(colonne)):
      if j+2 == joueur.grimpeurs[i].colonne:
          if colonne[j] == joueur.grimpeurs[i].etage:
            res += 1
  return res

############ Choix d'une des possibilités #########

def choix_possibilité(possibilités):
    message = ""
    for i in range(len(possibilités)):
      if possibilités[i].separation == True:
        if possibilités[i].combi1 != 0:
          message += str(i + 1) + "a : " + str(possibilités[i].combi1) + ", "
        if possibilités[i].combi2 != 0:
          message += str(i + 1) + "b : " + str(possibilités[i].combi1) + ", "
      elif not(possibilités[i].combi1 == 0 and possibilités[i].combi2 == 0):
        message += str(i + 1) + " : " + str(possibilités[i].combi1) + " et " + str(possibilités[i].combi2) + ", "
    
    if message != "":
      choix = input(message)
    else:
      choix = ""
    col = []
    for i in range(len(possibilités)):
      if str(choix) == str(i + 1):
        if possibilités[i].combi1 != 0:
          col.append(possibilités[i].combi1)
        if possibilités[i].combi2 != 0:
          col.append(possibilités[i].combi2)
      if choix == str(i + 1) + "a":
        col.append(possibilités[i].combi1)
      if choix == str(i + 1) + "b":
        col.append(possibilités[i].combi2)

    return col
    #retourne une liste avec les possibilités choisit

############ avancer les pions ###############

def avancer_pions(col,joueur):
    for i in range(len(col)):
        etage = 0
        for j in range(len(joueur.pions) - joueur.pions_restant):
            if col[i] == joueur.pions[j].colonne:
                etage = joueur.pions[j].etage
        j = 0
        while j < len(joueur.grimpeurs):
            if col[i] == joueur.grimpeurs[j].colonne:
                joueur.grimpeurs[j].etage += 1
                j = len(joueur.grimpeurs)
            elif joueur.grimpeurs[j].colonne == 0:
                joueur.grimpeurs[j].colonne = col[i]
                joueur.grimpeurs[j].etage += etage + 1
                j = len(joueur.grimpeurs)
            j += 1
    
    joueur.grimpeurs_restant = 3
    for i in range (len(joueur.grimpeurs)):
      if joueur.grimpeurs[i].colonne != 0:
        joueur.grimpeurs_restant -= 1
        
    return joueur.grimpeurs, joueur.grimpeurs_restant, joueur.pions_restant

############ Enregistrer les pions ############

def enregistrer_pions(joueur):
    for i in range(len(joueur.grimpeurs)):
        j = 0
        while j < len(joueur.pions):
            if joueur.pions[j].colonne == joueur.grimpeurs[i].colonne or joueur.pions[j].colonne == 0:
                joueur.pions[j].colonne = joueur.grimpeurs[i].colonne
                joueur.pions[j].etage = joueur.grimpeurs[i].etage
                joueur.grimpeurs[i].colonne = 0
                joueur.grimpeurs[i].etage = 0
                j = len(joueur.pions)
            j += 1
    print(joueur.pions)
    print(joueur.grimpeurs)
    
    joueur.pions_restant = 9
    for i in range (len(joueur.pions)):
      if joueur.pions[i].colonne != 0:
        joueur.pions_restant -= 1
        
    return joueur.pions, joueur.grimpeurs, joueur.pions_restant
            

############ seul Ilyes le sait ###############

def continuer():
    continuer = input("Voulez-vous continuer ? ")
    if continuer == "oui":
        return True
    else:
        return False


### Def nombres de joueurs ###
    
def joueurs():
    joueurs = []
    nb_j = int(input("Combien de joueurs dans la partie ? "))
    for i in range(nb_j):
        joueurs.append(Joueur([], [Pion(0,0),Pion(0,0),Pion(0,0),Pion(0,0),Pion(0,0),Pion(0,0),Pion(0,0),Pion(0,0),Pion(0,0)], [Pion(0,0),Pion(0,0),Pion(0,0)]))
    return joueurs

#### Def nombre de joueurs ####

def n_joueurs(nb_j):
    jrs = []
    for i in range(nb_j):
        jrs.append(Joueur("", [], [Pion(0,0),Pion(0,0),Pion(0,0),Pion(0,0),Pion(0,0),Pion(0,0),Pion(0,0),Pion(0,0),Pion(0,0)], [Pion(0,0),Pion(0,0),Pion(0,0)]))
    return jrs

##### Test si il peut placer aucun pion ####

def test_0_pions(des):
    err = 0
    for i in range(len(des)):
        if des[i].combi1 == 0 and des[i].combi2 == 0:
            err += 1
    if err == 3:
        return False
    else:
        return True

############ On associe un joueur à ses dés, ses pions restants et ses grimpeurs placés ###############

def jeu():
    nb_j = 0
    while nb_j <= 1 or nb_j >= 5:
        nb_j = int(input("Combien de joueurs dans la partie ? "))
        if nb_j <= 1 or nb_j >= 5:
            print("Chosissez un nombre entre 2 et 4")
    
    joueurs = n_joueurs(nb_j)
    p = prio(nb_j)
    colonne= [2,4,6,8,10,12,10,8,6,4,2]

    win = False
    
    for i in range(len(joueurs)):
        msg = "Quel nom pour le joueur " + str(i+1) + " ? "
        name = input(msg)
        joueurs[i].nom = name
    
  
    while not win:
        cont = True
        while cont:
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            print("C'est à " + str(joueurs[p-1].nom + " de jouer !"))
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            #Définition des combinaisons de dés que le joueur peut jouer
            combis = addition(lancer_des())
            joueurs[p-1].des = test_place_pion(combis,joueurs[p-1],colonne)
        
            #Quel choix parmis ses combinaisons de dés veut-il faire
            print("Voici votre nombre de pions restant à placer : " + str(joueurs[p-1].pions_restant))
            print("Voici vos pions :")
            print(joueurs[p-1].pions)
            print("Voici votre nombre de grimpeurs restant à placer : " + str(joueurs[p-1].grimpeurs_restant))
            print("Voici vos grimpeurs :")
            print(joueurs[p-1].grimpeurs)
            
            if test_0_pions(joueurs[p-1].des):
                col = choix_possibilité(joueurs[p-1].des)
                #Avec ce choix, faire avancer le(s) grimpeur(s)
                joueurs[p-1].grimpeurs,joueurs[p-1].grimpeurs_restant,joueurs[p-1].pions_restant = avancer_pions(col,joueurs[p-1])
            
                #Ce joueur a-t-il gagné ?
                complete = trois_lignes_complete(joueurs[p-1],colonne) + trois_grimpeurs_complete(joueurs[p-1],colonne)
                if complete >= 3:
                    win = True
                    winner = p-1
                    cont = False
                    joueurs[p-1].pions, joueurs[p-1].grimpeurs, joueurs[p-1].pions_restant = enregistrer_pions(joueurs[p-1])
                    joueurs[p-1].grimpeurs_restant = len(joueurs[p-1].grimpeurs)
                    joueurs[p-1].des = []
                else:
                    print(joueurs[p-1].pions)
                    print(joueurs[p-1].grimpeurs)
                    #Continuer ?
                    cont = continuer()
                    joueurs[p-1].des = []
                    if not cont:
                        joueurs[p-1].pions, joueurs[p-1].grimpeurs, joueurs[p-1].pions_restant = enregistrer_pions(joueurs[p-1])
                        joueurs[p-1].grimpeurs_restant = len(joueurs[p-1].grimpeurs)
                        if p == len(joueurs):
                            p = 1
                        else:
                            p += 1
                   
            else:
                print("Pas de chance, vous ne pouvez placer aucun pion sur le place avec votre lancer")
                joueurs[p-1].grimpeurs_restant = len(joueurs[p-1].grimpeurs)
                joueurs[p-1].grimpeurs = [Pion(0,0),Pion(0,0),Pion(0,0)]
                if p == len(joueurs):
                    p = 1
                else:
                    p += 1
    
    print("Le joueur gagnant est le joueur " + str(winner) + " !")

    

jeu()
