import random
import pygame
import time



class Pion:
  def __init__(self, colonne : int, etage : int):
    self.colonne = colonne
    self.etage = etage
  def __repr__(self) -> str:
    return "Pion(" + str(self.colonne)+","+str(self.etage) + ")"

class CombiDes:
  def __init__(self, separation : bool, combi1 : int, combi2 : int):
    self.separation = separation
    self.combi1 = combi1
    self.combi2 = combi2
  def __repr__(self) -> str:
    return "CombiDes('" + str(self.separation) + ", " + str(self.combi1) + ", " + str(self.combi2) + "')"

class Joueur:
  def __init__(self,nom : str, des : int, pions : list, grimpeurs : list):
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
    return "Joueur(" + str(self.nom) + ':' + str(self.des) + ":" + str(self.pions_restant) + ":" + "[" + ':'.join(str(elem) for elem in self.pions) + "]" + ":" + str(self.grimpeurs_restant) + ":" + "[" + ':'.join(str(elem) for elem in self.grimpeurs) + "]" + ")"
    
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
    possibilités = [CombiDes(False,dés[0]+dés[1],dés[2]+dés[3]),CombiDes(False,dés[0]+dés[2],dés[1]+dés[3]),CombiDes(False,dés[0]+dés[3],dés[1]+dés[2])]
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
                if err1 == len(joueur.pions):
                    #On veut savoir cb de grimpeurs corresponde aux pions
                    err2 = 0
                    corr = 0
                    for k in range (1,len(joueur.pions)):
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
                        poss_tempo.append(possibilités_finales[i].combi2)
                        
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
  for i in range(len(joueur.pions)):
    for j in range(len(colonne)):
      if j+2 == joueur.pions[i].colonne and colonne[j] == joueur.pions[i].etage:
        res += 1
  return res

def trois_grimpeurs_complete(joueur,colonne):
  res = 0
  for i in range(len(joueur.grimpeurs)):
    for j in range(len(colonne)):
      if j+2 == joueur.grimpeurs[i].colonne and colonne[j] == joueur.grimpeurs[i].etage:
            res += 1
  return res

####################################################
################# Partie Graphique #################
####################################################

############ Choix d'une des possibilités #########

def choix_possibilité(possibilités,xy_rect_interactions,window_resolution,window_surface,joueur,des,p):
    black_color = (0,0,0)
    message = ""
    arial_font = pygame.font.SysFont("arial", 50)
    rect = []
    text_color = ('#e2bc74')
    font_color_title = ("#683243")
    font_color_choice = ("#00709a")
    if p == 1:
        name_color = (100, 200, 230)
    if p == 2:
        name_color = (240, 130, 190)
    if p == 3:
        name_color = (240, 180, 0)
    if p == 4:
        name_color = (150, 220, 120)
    
    nb = arial_font.render(str(joueur.nom),False,name_color)
    p_nb = nb.get_rect(center=(window_resolution[0]*2/3 + xy_rect_interactions[0]/2, xy_rect_interactions[1]/18))
    window_surface.blit(nb,p_nb)
    
    if possibilités[0].separation == True:
        rect_poss_1 = pygame.Rect(window_resolution[0]*2/3 + 10 ,(3*0+1)*window_resolution[1]/10+10 ,xy_rect_interactions[0]-20 ,xy_rect_interactions[1]/10-20)
        pygame.draw.rect(window_surface,font_color_title, rect_poss_1)
        pygame.draw.rect(window_surface,black_color, rect_poss_1,5)
        
        msg = ""
        if possibilités[0].combi1 != 0 and possibilités[0].combi1 == des[0] + des[1]:
            msg += str(des[0]) + " + " + str(des[1])
        elif possibilités[0].combi1 != 0 and possibilités[0].combi1 == des[2] + des[3]:
            msg += str(des[2]) + " + " + str(des[3])
        if possibilités[0].combi2 != 0 and possibilités[0].combi2 == des[2] + des[3]:
            if possibilités[0].combi1 != 0 and possibilités[0].combi1 == des[0] + des[1]:
                msg += " ou " + str(des[2]) + " + " + str(des[3])
            else:
                msg += str(des[2]) + " + " + str(des[3])
        elif possibilités[0].combi2 != 0 and possibilités[0].combi2 == des[0] + des[1]:
            if possibilités[0].combi1 != 0 and possibilités[0].combi1 == des[2] + des[3]:
                msg += " ou " + str(des[0]) + " + " + str(des[1])
            else:
                msg += str(des[0]) + " + " + str(des[1])
        
        nb = arial_font.render(msg ,False,text_color)
        p_nb = nb.get_rect(center=(rect_poss_1.x + rect_poss_1.width/2 , rect_poss_1.y + rect_poss_1.height/2))
        window_surface.blit(nb,p_nb)
        pygame.display.flip()
        
        if possibilités[0].combi1 != 0:
            rect_1a = pygame.Rect(window_resolution[0]*2/3 + 10 ,(3*0+2)*window_resolution[1]/10+10 ,xy_rect_interactions[0]-20 ,xy_rect_interactions[1]/10-20)
            rect.append(rect_1a)
            rect.append("1a")
            pygame.draw.rect(window_surface,font_color_choice, rect_1a)
            pygame.draw.rect(window_surface,black_color, rect_1a,5)
            nb = arial_font.render(str(possibilités[0].combi1),False,text_color)
            p_nb = nb.get_rect(center=(rect_1a.x + rect_1a.width/2 , rect_1a.y + rect_1a.height/2))
            window_surface.blit(nb,p_nb)
            pygame.display.flip()
            
            #message += str(i + 1) + "a, "
        if possibilités[0].combi2 != 0:
            rect_1b = pygame.Rect(window_resolution[0]*2/3 + 10 ,(3*0+3)*window_resolution[1]/10+10 ,xy_rect_interactions[0]-20 ,xy_rect_interactions[1]/10-20)
            rect.append(rect_1b)
            rect.append("1b")
            pygame.draw.rect(window_surface,font_color_choice, rect_1b)
            pygame.draw.rect(window_surface,black_color, rect_1b,5)
            nb = arial_font.render(str(possibilités[0].combi2),False,text_color)
            p_nb = nb.get_rect(center=(rect_1b.x + rect_1b.width/2 , rect_1b.y + rect_1b.height/2))
            window_surface.blit(nb,p_nb)
            pygame.display.flip()
                #message += str(i + 1) + "b, "
            
    elif not(possibilités[0].combi1 == 0 and possibilités[0].combi2 == 0):
        rect_poss_1 = pygame.Rect(window_resolution[0]*2/3 + 10 ,(1)*window_resolution[1]/10+10 ,xy_rect_interactions[0]-20 ,xy_rect_interactions[1]/10-20)
        pygame.draw.rect(window_surface,font_color_title, rect_poss_1)
        pygame.draw.rect(window_surface,black_color, rect_poss_1,5)
        
        msg = ""
        if possibilités[0].combi1 != 0 and possibilités[0].combi1 == des[0] + des[1]:
            msg += str(des[0]) + " + " + str(des[1])
        elif possibilités[0].combi1 != 0 and possibilités[0].combi1 == des[2] + des[3]:
            msg += str(des[2]) + " + " + str(des[3])
        if possibilités[0].combi2 != 0 and possibilités[0].combi2 == des[2] + des[3]:
            if possibilités[0].combi1 != 0 and possibilités[0].combi1 == des[0] + des[1]:
                msg += " ou " + str(des[2]) + " + " + str(des[3])
            else:
                msg += str(des[2]) + " + " + str(des[3])
        elif possibilités[0].combi2 != 0 and possibilités[0].combi2 == des[0] + des[1]:
            if possibilités[0].combi1 != 0 and possibilités[0].combi1 == des[2] + des[3]:
                msg += " ou " + str(des[0]) + " + " + str(des[1])
            else:
                msg += str(des[0]) + " + " + str(des[1])
                
        nb = arial_font.render(msg ,False,text_color)
        p_nb = nb.get_rect(center=(rect_poss_1.x + rect_poss_1.width/2 , rect_poss_1.y + rect_poss_1.height/2))
        window_surface.blit(nb,p_nb)
        pygame.display.flip()
        
        rect_1 = pygame.Rect(window_resolution[0]*2/3 + 10 ,(2)*window_resolution[1]/10+10 ,xy_rect_interactions[0]-20 ,xy_rect_interactions[1]/10-20)
        rect.append(rect_1)
        rect.append("1")        
        pygame.draw.rect(window_surface,font_color_choice, rect_1)
        pygame.draw.rect(window_surface,black_color, rect_1,5)
        
        msg = ""
        if possibilités[0].combi1 != 0:
            msg += str(possibilités[0].combi1)
        if possibilités[0].combi2 != 0:
            if possibilités[0].combi1 != 0:
                msg += " et " + str(possibilités[0].combi2)
            else:
                msg += str(possibilités[0].combi2)
        
        nb = arial_font.render(msg,False,text_color)
        p_nb = nb.get_rect(center=(rect_1.x + rect_1.width/2 , rect_1.y + rect_1.height/2))
        window_surface.blit(nb,p_nb)
        pygame.display.flip()
        
    if possibilités[1].separation == True:
        rect_poss_1 = pygame.Rect(window_resolution[0]*2/3 + 10 ,(4)*window_resolution[1]/10+10 ,xy_rect_interactions[0]-20 ,xy_rect_interactions[1]/10-20)
        pygame.draw.rect(window_surface,font_color_title, rect_poss_1)
        pygame.draw.rect(window_surface,black_color, rect_poss_1,5)
        
        msg = ""
        if possibilités[1].combi1 != 0 and possibilités[1].combi1 == des[0] + des[2]:
            msg += str(des[0]) + " + " + str(des[2])
        elif possibilités[1].combi1 != 0 and possibilités[1].combi1 == des[1] + des[3]:
            msg += str(des[1]) + " + " + str(des[3])
            
        if possibilités[1].combi2 != 0 and possibilités[1].combi2 == des[1] + des[3]:
            if possibilités[1].combi1 != 0 and possibilités[1].combi1 == des[0] + des[2]:
                msg += " ou " + str(des[1]) + " + " + str(des[3])
            else:
                msg += str(des[1]) + " + " + str(des[3])
        elif possibilités[1].combi2 != 0 and possibilités[1].combi2 == des[0] + des[2]:
            if possibilités[1].combi1 != 0 and possibilités[1].combi1 == des[1] + des[3]:
                msg += " ou " + str(des[0]) + " + " + str(des[2])
            else:
                msg += str(des[0]) + " + " + str(des[2])
                
        nb = arial_font.render(msg ,False,text_color)
        p_nb = nb.get_rect(center=(rect_poss_1.x + rect_poss_1.width/2 , rect_poss_1.y + rect_poss_1.height/2))
        window_surface.blit(nb,p_nb)
        pygame.display.flip()
        if possibilités[1].combi1 != 0:
            rect_2a = pygame.Rect(window_resolution[0]*2/3 + 10 ,(3*1+2)*window_resolution[1]/10+10 ,xy_rect_interactions[0]-20 ,xy_rect_interactions[1]/10-20)
            rect.append(rect_2a)
            rect.append("2a")
            pygame.draw.rect(window_surface,font_color_choice, rect_2a)
            pygame.draw.rect(window_surface,black_color, rect_2a,5)
            nb = arial_font.render(str(possibilités[1].combi1),False,text_color)
            p_nb = nb.get_rect(center=(rect_2a.x + rect_2a.width/2 , rect_2a.y + rect_2a.height/2))
            window_surface.blit(nb,p_nb)
            pygame.display.flip()
            
        if possibilités[1].combi2 != 0:
            rect_2b = pygame.Rect(window_resolution[0]*2/3 + 10 ,(3*1+3)*window_resolution[1]/10+10 ,xy_rect_interactions[0]-20 ,xy_rect_interactions[1]/10-20)
            rect.append(rect_2b)
            rect.append("2b")
            pygame.draw.rect(window_surface,font_color_choice, rect_2b)
            pygame.draw.rect(window_surface,black_color, rect_2b,5)
            nb = arial_font.render(str(possibilités[1].combi2),False,text_color)
            p_nb = nb.get_rect(center=(rect_2b.x + rect_2b.width/2 , rect_2b.y + rect_2b.height/2))
            window_surface.blit(nb,p_nb)
            pygame.display.flip()
            
    elif not(possibilités[1].combi1 == 0 and possibilités[1].combi2 == 0):
        rect_poss_1 = pygame.Rect(window_resolution[0]*2/3 + 10 ,(4)*window_resolution[1]/10+10 ,xy_rect_interactions[0]-20 ,xy_rect_interactions[1]/10-20)
        pygame.draw.rect(window_surface,font_color_title, rect_poss_1)
        pygame.draw.rect(window_surface,black_color, rect_poss_1,5)
        
        msg = ""
        if possibilités[1].combi1 != 0 and possibilités[1].combi1 == des[0] + des[2]:
            msg += str(des[0]) + " + " + str(des[2])
        elif possibilités[1].combi1 != 0 and possibilités[1].combi1 == des[1] + des[3]:
            msg += str(des[1]) + " + " + str(des[3])
            
        if possibilités[1].combi2 != 0 and possibilités[1].combi2 == des[1] + des[3]:
            if possibilités[1].combi1 != 0 and possibilités[1].combi1 == des[0] + des[2]:
                msg += " ou " + str(des[1]) + " + " + str(des[3])
            else:
                msg += str(des[1]) + " + " + str(des[3])
        elif possibilités[1].combi2 != 0 and possibilités[1].combi2 == des[0] + des[2]:
            if possibilités[1].combi1 != 0 and possibilités[1].combi1 == des[1] + des[3]:
                msg += " ou " + str(des[0]) + " + " + str(des[2])
            else:
                msg += str(des[0]) + " + " + str(des[2])
        
        nb = arial_font.render(msg ,False,text_color)
        p_nb = nb.get_rect(center=(rect_poss_1.x + rect_poss_1.width/2 , rect_poss_1.y + rect_poss_1.height/2))
        window_surface.blit(nb,p_nb)
        pygame.display.flip()
        
        rect_2 = pygame.Rect(window_resolution[0]*2/3 + 10 ,(3*1+2)*window_resolution[1]/10+10 ,xy_rect_interactions[0]-20 ,xy_rect_interactions[1]/10-20)
        rect.append(rect_2)
        rect.append("2")
        pygame.draw.rect(window_surface,font_color_choice, rect_2)
        pygame.draw.rect(window_surface,black_color, rect_2,5)
        
        msg = ""
        if possibilités[1].combi1 != 0:
            msg += str(possibilités[1].combi1)
        if possibilités[1].combi2 != 0:
            if possibilités[1].combi1 != 0:
                msg += " et " + str(possibilités[1].combi2)
            else:
                msg += str(possibilités[1].combi2)
        
        nb = arial_font.render(msg,False,text_color)
        p_nb = nb.get_rect(center=(rect_2.x + rect_2.width/2 , rect_2.y + rect_2.height/2))
        window_surface.blit(nb,p_nb)
        pygame.display.flip()
    
    if possibilités[2].separation == True:
        rect_poss_1 = pygame.Rect(window_resolution[0]*2/3 + 10 ,(7)*window_resolution[1]/10+10 ,xy_rect_interactions[0]-20 ,xy_rect_interactions[1]/10-20)
        pygame.draw.rect(window_surface,font_color_title, rect_poss_1)
        pygame.draw.rect(window_surface,black_color, rect_poss_1,5)
        
        msg = ""
        if possibilités[2].combi1 != 0 and possibilités[2].combi1 == des[0] + des[3]:
            msg += str(des[0]) + " + " + str(des[3])
        elif possibilités[2].combi1 != 0 and possibilités[2].combi1 == des[1] + des[2]:
            msg += str(des[1]) + " + " + str(des[2])
            
        if possibilités[2].combi2 != 0 and possibilités[2].combi2 == des[1] + des[2]:
            if possibilités[2].combi1 != 0 and possibilités[2].combi1 == des[0] + des[3]:
                msg += " ou " + str(des[1]) + " + " + str(des[2])
            else:
                msg += str(des[1]) + " + " + str(des[3])
        elif possibilités[2].combi2 != 0 and possibilités[2].combi2 == des[0] + des[3]:
            if possibilités[2].combi1 != 0 and possibilités[2].combi1 == des[1] + des[2]:
                msg += " ou " + str(des[0]) + " + " + str(des[3])
            else:
                msg += str(des[0]) + " + " + str(des[3])
                
        nb = arial_font.render(msg ,False,text_color)
        p_nb = nb.get_rect(center=(rect_poss_1.x + rect_poss_1.width/2 , rect_poss_1.y + rect_poss_1.height/2))
        window_surface.blit(nb,p_nb)
        pygame.display.flip()
        
        if possibilités[2].combi1 != 0:
            rect_3a = pygame.Rect(window_resolution[0]*2/3 + 10 ,(3*2+2)*window_resolution[1]/10+10 ,xy_rect_interactions[0]-20 ,xy_rect_interactions[1]/10-20)
            rect.append(rect_3a)
            rect.append("3a")
            pygame.draw.rect(window_surface,font_color_choice, rect_3a)
            pygame.draw.rect(window_surface,black_color, rect_3a,5)
            nb = arial_font.render(str(possibilités[2].combi1),False,text_color)
            p_nb = nb.get_rect(center=(rect_3a.x + rect_3a.width/2 , rect_3a.y + rect_3a.height/2))
            window_surface.blit(nb,p_nb)
            pygame.display.flip()
            
        if possibilités[2].combi2 != 0:
            rect_3b = pygame.Rect(window_resolution[0]*2/3 + 10 ,(3*2+3)*window_resolution[1]/10+10 ,xy_rect_interactions[0]-20 ,xy_rect_interactions[1]/10-20)
            rect.append(rect_3b)
            rect.append("3b")
            pygame.draw.rect(window_surface,font_color_choice, rect_3b)
            pygame.draw.rect(window_surface,black_color, rect_3b,5)
            nb = arial_font.render(str(possibilités[2].combi2),False,text_color)
            p_nb = nb.get_rect(center=(rect_3b.x + rect_3b.width/2 , rect_3b.y + rect_3b.height/2))
            window_surface.blit(nb,p_nb)
            pygame.display.flip()
            
    elif not(possibilités[2].combi1 == 0 and possibilités[2].combi2 == 0):
        rect_poss_1 = pygame.Rect(window_resolution[0]*2/3 + 10 ,(7)*window_resolution[1]/10+10 ,xy_rect_interactions[0]-20 ,xy_rect_interactions[1]/10-20)
        pygame.draw.rect(window_surface,font_color_title, rect_poss_1)
        pygame.draw.rect(window_surface,black_color, rect_poss_1,5)
        
        msg = ""
        if possibilités[2].combi1 != 0 and possibilités[2].combi1 == des[0] + des[3]:
            msg += str(des[0]) + " + " + str(des[3])
        elif possibilités[2].combi1 != 0 and possibilités[2].combi1 == des[1] + des[2]:
            msg += str(des[1]) + " + " + str(des[2])
            
        if possibilités[2].combi2 != 0 and possibilités[2].combi2 == des[1] + des[2]:
            if possibilités[2].combi1 != 0 and possibilités[2].combi1 == des[0] + des[3]:
                msg += " ou " + str(des[1]) + " + " + str(des[2])
            else:
                msg += str(des[1]) + " + " + str(des[3])
        elif possibilités[2].combi2 != 0 and possibilités[2].combi2 == des[0] + des[3]:
            if possibilités[2].combi1 != 0 and possibilités[2].combi1 == des[1] + des[2]:
                msg += " ou " + str(des[0]) + " + " + str(des[3])
            else:
                msg += str(des[0]) + " + " + str(des[3])
        
        nb = arial_font.render(msg ,False,text_color)
        p_nb = nb.get_rect(center=(rect_poss_1.x + rect_poss_1.width/2 , rect_poss_1.y + rect_poss_1.height/2))
        window_surface.blit(nb,p_nb)
        pygame.display.flip()
        
        rect_3 = pygame.Rect(window_resolution[0]*2/3 + 10 ,(3*2+2)*window_resolution[1]/10+10 ,xy_rect_interactions[0]-20 ,xy_rect_interactions[1]/10-20)
        rect.append(rect_3)
        rect.append("3")
        pygame.draw.rect(window_surface,font_color_choice, rect_3)
        pygame.draw.rect(window_surface,black_color, rect_3,5)
        
        msg = ""
        if possibilités[2].combi1 != 0:
            msg += str(possibilités[2].combi1)
        if possibilités[2].combi2 != 0:
            if possibilités[2].combi1 != 0:
                msg += " et " + str(possibilités[2].combi2)
            else:
                msg += str(possibilités[2].combi2)
        
        nb = arial_font.render(msg,False,text_color)
        p_nb = nb.get_rect(center=(rect_3.x + rect_3.width/2 , rect_3.y + rect_3.height/2))
        window_surface.blit(nb,p_nb)
        pygame.display.flip()
    
    return rect, window_surface
    

def prendre_possibilité(possibilités,xy_rect_interactions,window_resolution,window_surface,rect):
    no_click = True
    while no_click:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                no_click = False
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONUP:
                for i in range(int(len(rect)/2)):
                    if (rect[2*i].x < pygame.mouse.get_pos()[0] < rect[2*i].x + rect[2*i].width and
                        rect[2*i].y < int(pygame.mouse.get_pos()[1]) < rect[2*i].y + rect[2*i].height):
                        col = []
                        for k in range(len(possibilités)):
                            if rect[2*i+1] == str(k + 1):
                                if possibilités[k].combi1 != 0:
                                    col.append(possibilités[k].combi1)
                                if possibilités[k].combi2 != 0:
                                    col.append(possibilités[k].combi2)
                            no_click = False
                            nb_j = 1
                            if rect[2*i+1]  == str(k + 1) + "a":
                                col.append(possibilités[k].combi1)
                                no_click = False
                                nb_j = 1
                            if rect[2*i+1]  == str(k + 1) + "b":
                                col.append(possibilités[k].combi2)
                                no_click = False
                                nb_j = 1
    
    return col,window_surface
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

def continuer(rect):
    no_click = True
    while no_click:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                no_click = False
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONUP:
                for i in range(int(len(rect)/2)):
                    if (rect[2*i].x < pygame.mouse.get_pos()[0] < rect[2*i].x + rect[2*i].width and
                        rect[2*i].y < int(pygame.mouse.get_pos()[1]) < rect[2*i].y + rect[2*i].height):
                        r = rect[2*i+1]
                        no_click = False
    return r


### Def nombres de joueurs ###
    
def nb_joueurs(window_surface,window_resolution,black_color):
    joueurs = []
    couleur_font_bouton = (45, 36, 30)
    couleur_text = ("#80d0d0")
    
    can_t_stop_font = pygame.font.SysFont("gameplay", 100)
    p_nb = [window_resolution[0]/2,window_resolution[1]/10]
    nb = can_t_stop_font.render("Can't Stop",False,couleur_text)
    text_center = nb.get_rect(center=(window_resolution[0]/2, window_resolution[1]/8))
    window_surface.blit(nb,text_center)
    
    arial_font = pygame.font.SysFont("arial", 60)
    
    """
    Ce rectangle nous à servit de test, car plus simple de tester avec un seul joueur qu'avec plusieurs au départ
    rect_1_j = pygame.Rect(window_resolution[0]/2-window_resolution[0]/4 ,window_resolution[1]/2-window_resolution[1]/4 ,window_resolution[0]/4-10 ,window_resolution[1]/4-10 )
    nb1 = arial_font.render("1 joueur",False,couleur_text)
    text_center1 = nb1.get_rect(center=(rect_1_j.width/2+rect_1_j.x, rect_1_j.height/2 + rect_1_j.y))
    """
    
    rect_2_j = pygame.Rect(window_resolution[0]/2-window_resolution[0]/8,window_resolution[1]/2-window_resolution[1]/4,window_resolution[0]/4-10,window_resolution[1]/4-10)
    nb2 = arial_font.render("2 joueurs",False,couleur_text)
    text_center2 = nb2.get_rect(center=(rect_2_j.width/2+rect_2_j.x, rect_2_j.height/2 + rect_2_j.y))
    
    rect_3_j = pygame.Rect(window_resolution[0]/2-window_resolution[0]/4,window_resolution[1]/2+10,window_resolution[0]/4-10,window_resolution[1]/4-10)
    nb3 = arial_font.render("3 joueurs",False,couleur_text)
    text_center3 = nb3.get_rect(center=(rect_3_j.width/2+rect_3_j.x, rect_3_j.height/2 + rect_3_j.y))
    
    rect_4_j = pygame.Rect(window_resolution[0]/2+10,window_resolution[1]/2+10,window_resolution[0]/4-10,window_resolution[1]/4-10)
    nb4 = arial_font.render("4 joueurs",False,couleur_text)
    text_center4 = nb4.get_rect(center=(rect_4_j.width/2+rect_4_j.x, rect_4_j.height/2 + rect_4_j.y))
    
    #pygame.draw.rect(window_surface,couleur_font_bouton, rect_1_j)
    #pygame.draw.rect(window_surface,black_color, rect_1_j,5)
    pygame.draw.rect(window_surface,couleur_font_bouton, rect_2_j)
    pygame.draw.rect(window_surface,black_color, rect_2_j,5)
    pygame.draw.rect(window_surface,couleur_font_bouton, rect_3_j)
    pygame.draw.rect(window_surface,black_color, rect_3_j,5)
    pygame.draw.rect(window_surface,couleur_font_bouton, rect_4_j)
    pygame.draw.rect(window_surface,black_color, rect_4_j,5)
    
    #window_surface.blit(nb1,text_center1)
    window_surface.blit(nb2,text_center2)
    window_surface.blit(nb3,text_center3)
    window_surface.blit(nb4,text_center4)
    pygame.display.flip()
    
    no_click = True
    while no_click:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                no_click = False
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONUP:
                """
                if (rect_1_j.x < pygame.mouse.get_pos()[0] < rect_1_j.x + rect_1_j.width and
                    rect_1_j.y < int(pygame.mouse.get_pos()[1]) < rect_1_j.y + rect_1_j.height):
                    no_click = False
                    nb_j = 1
                """
                if (rect_2_j.x < pygame.mouse.get_pos()[0] < rect_2_j.x + rect_2_j.width and
                    rect_2_j.y < int(pygame.mouse.get_pos()[1]) < rect_2_j.y + rect_2_j.height):
                    no_click = False
                    nb_j = 2
                if (rect_3_j.x < pygame.mouse.get_pos()[0] < rect_3_j.x + rect_3_j.width and
                    rect_3_j.y < int(pygame.mouse.get_pos()[1]) < rect_3_j.y + rect_3_j.height):
                    no_click = False
                    nb_j = 3
                if (rect_4_j.x < pygame.mouse.get_pos()[0] < rect_4_j.x + rect_4_j.width and
                    rect_4_j.y < int(pygame.mouse.get_pos()[1]) < rect_4_j.y + rect_4_j.height):
                    no_click = False
                    nb_j = 4
                
        
    for i in range(nb_j):
        joueurs.append(Joueur("", [], [Pion(0,0),Pion(0,0),Pion(0,0),Pion(0,0),Pion(0,0),Pion(0,0),Pion(0,0),Pion(0,0),Pion(0,0)], [Pion(0,0),Pion(0,0),Pion(0,0)]))
    return joueurs

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

##############################################
###########    Partie graphique    ###########
##############################################

def rectangle_tableau(window_resolution,black_color,window_surface,font_color):
    rect_tableau = pygame.Rect(0,0,window_resolution[0]/1.5,window_resolution[1])
    pygame.draw.rect(window_surface,font_color, rect_tableau)
    rect_tableau = pygame.Rect(0,0,window_resolution[0]/1.5,window_resolution[1])
    pygame.draw.rect(window_surface,black_color, rect_tableau,5)
    
    return window_surface

def rectangle_interaction(window_resolution,black_color,window_surface,font_color):
    rect_interactions = pygame.Rect(window_resolution[0]/1.5,0,window_resolution[0],window_resolution[1])
    pygame.draw.rect(window_surface,font_color, rect_interactions)
    rect_interactions = pygame.Rect(window_resolution[0]/1.5,0,window_resolution[0],window_resolution[1])
    pygame.draw.rect(window_surface,black_color, rect_interactions,5)
    
    return window_surface
    
def fenêtre_de_base(window_resolution,black_color,window_surface,font_color):
    #Création des deux parties du plateau
    
    window_surface = rectangle_tableau(window_resolution,black_color,window_surface,font_color)
    window_surface = rectangle_interaction(window_resolution,black_color,window_surface,font_color)

    return window_surface

def tableau_de_base(col,xy_rect_tableau,window_surface):
    #Creation du tableau
    line_color = (45, 36, 30)
    place_color = (127, 127, 127)
    text_color = ('#f28a6d')
    for i in range(len(col)):
        if col[i] >= 12:
            p1 = [(i+1)*xy_rect_tableau[0]/(len(col)+1),1*xy_rect_tableau[1]/13]
            p2 = [(i+1)*xy_rect_tableau[0]/(len(col)+1),12*xy_rect_tableau[1]/13]
            pygame.draw.line(window_surface,line_color,p1,p2,5)
            pygame.draw.circle(window_surface,place_color, p1,10)
            pygame.draw.circle(window_surface,place_color, p2,10)
        if col[i] >= 10:
            p1 = [(i+1)*xy_rect_tableau[0]/(len(col)+1),2*xy_rect_tableau[1]/13]
            p2 = [(i+1)*xy_rect_tableau[0]/(len(col)+1),11*xy_rect_tableau[1]/13]
            pygame.draw.line(window_surface,line_color,p1,p2,5)
            pygame.draw.circle(window_surface,place_color, p1,10)
            pygame.draw.circle(window_surface,place_color, p2,10)
        if col[i] >= 8:
            p1 = [(i+1)*xy_rect_tableau[0]/(len(col)+1),3*xy_rect_tableau[1]/13]
            p2 = [(i+1)*xy_rect_tableau[0]/(len(col)+1),10*xy_rect_tableau[1]/13]
            pygame.draw.line(window_surface,line_color,p1,p2,5)
            pygame.draw.circle(window_surface,place_color, p1,10)
            pygame.draw.circle(window_surface,place_color, p2,10)
        if col[i] >= 6:
            p1 = [(i+1)*xy_rect_tableau[0]/(len(col)+1),4*xy_rect_tableau[1]/13]
            p2 = [(i+1)*xy_rect_tableau[0]/(len(col)+1),9*xy_rect_tableau[1]/13]
            pygame.draw.line(window_surface,line_color,p1,p2,5)
            pygame.draw.circle(window_surface,place_color, p1,10)
            pygame.draw.circle(window_surface,place_color, p2,10)
        if col[i] >= 4:
            p1 = [(i+1)*xy_rect_tableau[0]/(len(col)+1),5*xy_rect_tableau[1]/13]
            p2 = [(i+1)*xy_rect_tableau[0]/(len(col)+1),8*xy_rect_tableau[1]/13]
            pygame.draw.line(window_surface,line_color,p1,p2,5)
            pygame.draw.circle(window_surface,place_color, p1,10)
            pygame.draw.circle(window_surface,place_color, p2,10)
        if col[i] >= 2:
            p1 = [(i+1)*xy_rect_tableau[0]/(len(col)+1),6*xy_rect_tableau[1]/13]
            p2 = [(i+1)*xy_rect_tableau[0]/(len(col)+1),7*xy_rect_tableau[1]/13]
            pygame.draw.line(window_surface,line_color,p1,p2,5)
            pygame.draw.circle(window_surface,place_color, p1,10)
            pygame.draw.circle(window_surface,place_color, p2,10)
        
        arial_font = pygame.font.SysFont("arial", 30)
        
        nb = arial_font.render(str(i+2),False,text_color)
        y = ((13-col[i])/2)*xy_rect_tableau[1]/13
        if i + 2 - 10 < 0:
            x = (i+1)*xy_rect_tableau[0]/(len(col)+1)
        elif i + 2 - 10 >= 0:
            x = (i+1)*xy_rect_tableau[0]/(len(col)+1)
        p_nb = p_nb = nb.get_rect(center=(x, y))
        window_surface.blit(nb,p_nb)
        
    return window_surface
        

def afficher_avancer_grimpeurs(joueur,xy_rect_tableau,col,window_surface):
    color = (0,0,0)
    zero = 0
    for i in range(len(joueur.grimpeurs)):
        if joueur.grimpeurs[i].colonne != 0:
            for k in range(len(col)):
                if k+2 == joueur.grimpeurs[i].colonne:
                    x = (joueur.grimpeurs[i].colonne-1)*xy_rect_tableau[0]/(len(col)+1)
                    y = xy_rect_tableau[1] - ((joueur.grimpeurs[i].etage-1)*xy_rect_tableau[1]/13 + xy_rect_tableau[1]/13*(((13-col[k])+1)/2))
                    p1 = [x,y]
                    pygame.draw.circle(window_surface,color,p1,10)
        else:
            zero += 1
    for i in range(zero):
        p2 = [xy_rect_tableau[0]/(len(col)+1)+i*30,xy_rect_tableau[1]-(xy_rect_tableau[1]/13)]
        pygame.draw.circle(window_surface,color,p2,10)

    return window_surface

def afficher_avancer_pions(joueur,xy_rect_tableau,col,window_surface,p):
    if p == 1:
        color = (4, 139, 154)
        text_color = (100, 200, 230)
    if p == 2:
        color = (196, 105, 143)
        text_color = (240, 130, 190)
    if p == 3:
        color = (204, 153, 0)
        text_color = (240, 180, 0)
    if p == 4:
        color = (130, 196, 108)
        text_color = (150, 220, 120)
    zero = 0
    for i in range(len(joueur.pions)):
        if joueur.pions[i].colonne != 0:
            for k in range(len(col)):
                if k+2 == joueur.pions[i].colonne:
                    x = (joueur.pions[i].colonne-1)*xy_rect_tableau[0]/(len(col)+1)
                    y = xy_rect_tableau[1] - ((joueur.pions[i].etage-1)*xy_rect_tableau[1]/13 + xy_rect_tableau[1]/13*(((13-col[k])+1)/2))
                    if p == 1:
                        p1 = [x+10,y]
                    if p == 2:
                        p1 = [x-10,y]
                    if p == 3:
                        p1 = [x,y+10]
                    if p == 4:
                        p1 = [x,y-10]
                    pygame.draw.circle(window_surface,color,p1,10)
        else:
            zero += 1
    arial_font = pygame.font.SysFont("arial", 20)
    if p == 1:
        nb = arial_font.render(str(zero),False,text_color)
        p2 = [xy_rect_tableau[0]/(len(col)+1),xy_rect_tableau[1]/13]
        p_nb = nb.get_rect(center=(xy_rect_tableau[0]/(len(col)+1)-25 , xy_rect_tableau[1]/13))
        pygame.draw.circle(window_surface,color,p2,10)
        window_surface.blit(nb,p_nb)
        
        nb = arial_font.render(str(joueur.nom),False,text_color)
        p_nb = [xy_rect_tableau[0]/(len(col)+1)+15,xy_rect_tableau[1]/13-10]
        window_surface.blit(nb,p_nb)
    if p == 2:
        nb = arial_font.render(str(zero),False,text_color)
        p2 = [xy_rect_tableau[0]/(len(col)+1),xy_rect_tableau[1]/13+30]
        p_nb = nb.get_rect(center=(xy_rect_tableau[0]/(len(col)+1)-25 , xy_rect_tableau[1]/13+30))
        pygame.draw.circle(window_surface,color,p2,10)
        window_surface.blit(nb,p_nb)
        
        nb = arial_font.render(str(joueur.nom),False,text_color)
        p_nb = [xy_rect_tableau[0]/(len(col)+1)+15,xy_rect_tableau[1]/13+20]
        window_surface.blit(nb,p_nb)
    if p == 3:
        nb = arial_font.render(str(zero),False,text_color)
        p2 = [xy_rect_tableau[0]/(len(col)+1),xy_rect_tableau[1]/13+60]
        p_nb = nb.get_rect(center=(xy_rect_tableau[0]/(len(col)+1)-25 , xy_rect_tableau[1]/13+60))
        pygame.draw.circle(window_surface,color,p2,10)
        window_surface.blit(nb,p_nb)
        
        nb = arial_font.render(str(joueur.nom),False,text_color)
        p_nb = [xy_rect_tableau[0]/(len(col)+1)+15,xy_rect_tableau[1]/13+50]
        window_surface.blit(nb,p_nb)
    if p == 4:
        nb = arial_font.render(str(zero),False,text_color)
        p2 = [xy_rect_tableau[0]/(len(col)+1),xy_rect_tableau[1]/13+90]
        p_nb = nb.get_rect(center=(xy_rect_tableau[0]/(len(col)+1)-25 , xy_rect_tableau[1]/13+90))
        pygame.draw.circle(window_surface,color,p2,10)
        window_surface.blit(nb,p_nb)
        
        nb = arial_font.render(str(joueur.nom),False,text_color)
        p_nb = [xy_rect_tableau[0]/(len(col)+1)+15,xy_rect_tableau[1]/13+80]
        window_surface.blit(nb,p_nb)

    return window_surface

def afficher_continuer(xy_rect_interactions,window_resolution,window_surface):
    black_color = (0,0,0)
    arial_font = pygame.font.SysFont("arial", 30)
    rect_choix = []
    text_color = ('#687e40')
    font_color = ("#00709a")
    
    x = window_resolution[0]*2/3+10
    y = 1*window_resolution[1]/5+10
    dx = xy_rect_interactions[0]-20
    dy = xy_rect_interactions[1]/5-20
    nb = arial_font.render("Continuer ?",False,text_color)
    p_nb = nb.get_rect(center=(x + dx/2 , y + dy/2))
    window_surface.blit(nb,p_nb)
    
    x = window_resolution[0]*2/3+10
    y = 2*window_resolution[1]/5+10
    dx = xy_rect_interactions[0]-20
    dy = xy_rect_interactions[1]/5-20
    rect_oui = pygame.Rect(x,y,dx,dy)
    nb = arial_font.render("Oui",False,text_color)
    p_nb = nb.get_rect(center=(x + dx/2 ,y + dy/2))
    pygame.draw.rect(window_surface,font_color, rect_oui)
    pygame.draw.rect(window_surface,black_color, rect_oui,5)
    window_surface.blit(nb,p_nb)
    rect_choix.append(rect_oui)
    rect_choix.append(True)
    
    x = window_resolution[0]*2/3+10
    y = 3*window_resolution[1]/5+10
    dx = xy_rect_interactions[0]-20
    dy = xy_rect_interactions[1]/5-20
    rect_non = pygame.Rect(x,y,dx,dy)
    nb = arial_font.render("Non",False,text_color)
    p_nb = nb.get_rect(center=(x + dx/2 , y + dy/2))
    pygame.draw.rect(window_surface,font_color, rect_non)
    pygame.draw.rect(window_surface,black_color, rect_non,5)
    window_surface.blit(nb,p_nb)
    rect_choix.append(rect_non)
    rect_choix.append(False)
    
    return window_surface, rect_choix

############ Fenetre afficher nom en train de taper ##############

def afficher_nom(name, window_resolution, window_surface, i):
    arial_font = pygame.font.SysFont("arial", 100)
    if i == 0:
        color = (4, 139, 154)
    if i == 1:
        color = (196, 105, 143)
    if i == 2:
        color = (204, 153, 0)
    if i == 3:
        color = (130, 196, 108)
    
    nb = arial_font.render(name,False,color)
    p_nb = nb.get_rect(center=(window_resolution[0]/2 ,window_resolution[1]/2))
    window_surface.blit(nb,p_nb)
    
    return window_surface

def afficher_i_joueur_debut(window_resolution, window_surface, i):
    arial_font = pygame.font.SysFont("arial", 100)
    if i == 0:
        color = (4, 139, 154)
    if i == 1:
        color = (196, 105, 143)
    if i == 2:
        color = (204, 153, 0)
    if i == 3:
        color = (130, 196, 108)
    
    nb = arial_font.render("Joueur " + str(i+1),False,color)
    p_nb = nb.get_rect(center=(window_resolution[0]/2 ,window_resolution[1]/4))
    window_surface.blit(nb,p_nb)
    
    return window_surface

def afficher_ecrire(window_resolution, window_surface):
    arial_font = pygame.font.SysFont("arial", 20)
    color = (0,0,0)
    
    x = window_resolution[0]*1/3
    y = 5*window_resolution[1]/8+10
    dx = window_resolution[0]*1/3
    dy = 1*window_resolution[1]/8-20
    rect_clavier = pygame.Rect(x,y,dx,dy)
    
    nb = arial_font.render("Tapez au clavier votre nom",False,color)
    p_nb = nb.get_rect(center=(rect_clavier.x + rect_clavier.width/2,rect_clavier.y + rect_clavier.height/2 ))
    pygame.draw.rect(window_surface,color, rect_clavier,5)
    window_surface.blit(nb,p_nb)
    
    x = window_resolution[0]*1/3
    y = 6*window_resolution[1]/8+10
    dx = window_resolution[0]*1/3
    dy = 1*window_resolution[1]/8-20
    rect_entrer = pygame.Rect(x,y,dx,dy)
    
    nb = arial_font.render("Tapez entrer une fois finis",False,color)
    p_nb = nb.get_rect(center=(rect_entrer.x + rect_entrer.width/2,rect_entrer.y + rect_entrer.height/2 ))
    pygame.draw.rect(window_surface,color, rect_entrer,5)
    window_surface.blit(nb,p_nb)
    
    x = window_resolution[0]*1/3
    y = 7*window_resolution[1]/8+10
    dx = window_resolution[0]*1/3
    dy = 1*window_resolution[1]/8-20
    rect_entrer = pygame.Rect(x,y,dx,dy)
    
    nb = arial_font.render("Nom long à éviter, limite à 10",False,color)
    p_nb = nb.get_rect(center=(rect_entrer.x + rect_entrer.width/2,rect_entrer.y + rect_entrer.height/2 ))
    pygame.draw.rect(window_surface,color, rect_entrer,5)
    window_surface.blit(nb,p_nb)
    
    return window_surface

def ecran_perdu(window_resolution,black_color,window_surface,font_color):
    arial_font = pygame.font.SysFont("arial", 70)
    red_color = (255,0,0)
    text_color = (255,255,255)
    window_surface.fill(red_color)
    nb = arial_font.render("Perdu, aucun possibilité possible",False,text_color)
    p_nb = nb.get_rect(center=(window_resolution[0]/2,window_resolution[1]/2 ))
    window_surface.blit(nb,p_nb)
    
    return window_surface

def ecran_de_fin(window_resolution,black_color,window_surface,font_color,joueur):
    arial_font = pygame.font.SysFont("arial", 70)
    text_color = (255,255,255)
    font_rect_color = ("#746426")
    black_color = (0,0,0)
    
    window_surface.fill(font_color)
    
    
    x = 4*window_resolution[0]/10+10
    y = 6*window_resolution[1]/8+10
    dx = window_resolution[0]/10-10
    dy = window_resolution[1]/6
    rect_oui = pygame.Rect(x,y,dx,dy)
    
    x = 5*window_resolution[0]/10+10
    y = 6*window_resolution[1]/8+10
    dx = window_resolution[0]/10-10
    dy = window_resolution[1]/6
    rect_non = pygame.Rect(x,y,dx,dy)
    
    pygame.draw.rect(window_surface,font_rect_color, rect_oui)
    pygame.draw.rect(window_surface,black_color, rect_oui,5)
    nb = arial_font.render("Oui" ,False,text_color)
    p_nb = nb.get_rect(center=(rect_oui.x + rect_oui.width/2,rect_oui.y + rect_oui.height/2))
    window_surface.blit(nb,p_nb)
    
    pygame.draw.rect(window_surface,font_rect_color, rect_non)
    pygame.draw.rect(window_surface,black_color, rect_non,5)
    nb = arial_font.render("Non" ,False,text_color)
    p_nb = nb.get_rect(center=(rect_non.x + rect_non.width/2,rect_non.y + rect_non.height/2))
    window_surface.blit(nb,p_nb)
    
    nb = arial_font.render("Bravo " + str(joueur.nom) + " ! Vous avez gagné !" ,False,text_color)
    p_nb = nb.get_rect(center=(window_resolution[0]/2,2*window_resolution[1]/6 ))
    window_surface.blit(nb,p_nb)
    nb = arial_font.render("Voulez vous rejouer ?" ,False,text_color)
    p_nb = nb.get_rect(center=(window_resolution[0]/2,3*window_resolution[1]/6 ))
    window_surface.blit(nb,p_nb)
    
    
   
    
    pygame.display.flip()
    
    no_click = True
    while no_click:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                no_click = False
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONUP:
                if (rect_oui.x < pygame.mouse.get_pos()[0] < rect_oui.x + rect_oui.width and
                    rect_oui.y < int(pygame.mouse.get_pos()[1]) < rect_oui.y + rect_oui.height):
                    no_click = False
                    jeu_continue = True
                if (rect_non.x < pygame.mouse.get_pos()[0] < rect_non.x + rect_non.width and
                    rect_non.y < int(pygame.mouse.get_pos()[1]) < rect_non.y + rect_non.height):
                    no_click = False
                    jeu_continue = False
    
    return window_surface, jeu_continue

def menu(window_resolution,window_surface):
    arial_font = pygame.font.SysFont("arial", 70)
    text_color = (255,255,255)
    font_rect_color = ("#746426")
    black_color = (0,0,0)
    rects = []
    
    x = window_resolution[0]/2-window_resolution[0]/8
    y = 2*window_resolution[1]/6+10
    dx = 2*window_resolution[0]/8
    dy = window_resolution[1]/6-10
    rect_jeu = pygame.Rect(x,y,dx,dy)
    rects.append(rect_jeu)
    
    x = window_resolution[0]/2-window_resolution[0]/8
    y = 3*window_resolution[1]/6+10
    dx = 2*window_resolution[0]/8
    dy = window_resolution[1]/6-10
    rect_options = pygame.Rect(x,y,dx,dy)
    rects.append(rect_options)
    
    x = window_resolution[0]/2-window_resolution[0]/8
    y = 4*window_resolution[1]/6+10
    dx = 2*window_resolution[0]/8
    dy = window_resolution[1]/6-10
    rect_resultats = pygame.Rect(x,y,dx,dy)
    rects.append(rect_resultats)
    
    pygame.draw.rect(window_surface,font_rect_color, rect_jeu)
    pygame.draw.rect(window_surface,black_color, rect_jeu,5)
    pygame.draw.rect(window_surface,font_rect_color, rect_options)
    pygame.draw.rect(window_surface,black_color, rect_options,5)
    pygame.draw.rect(window_surface,font_rect_color, rect_resultats)
    pygame.draw.rect(window_surface,black_color, rect_resultats,5)
    
    nb = arial_font.render("Jeu" ,False,text_color)
    p_nb = nb.get_rect(center=(rect_jeu.x + rect_jeu.width/2,rect_jeu.y + rect_jeu.height/2))
    window_surface.blit(nb,p_nb)
    
    nb = arial_font.render("Options" ,False,text_color)
    p_nb = nb.get_rect(center=(rect_options.x + rect_options.width/2,rect_options.y + rect_options.height/2))
    window_surface.blit(nb,p_nb)
    
    nb = arial_font.render("Resultats" ,False,text_color)
    p_nb = nb.get_rect(center=(rect_resultats.x + rect_resultats.width/2,rect_resultats.y + rect_resultats.height/2))
    window_surface.blit(nb,p_nb)
    
    return window_surface, rects

def bouton_retour(window_surface, font_rect_color):
    
    x_rect = 10
    y_rect = 10
    dx_rect = 50
    dy_rect = 50
    rect_return = pygame.Rect(x_rect,y_rect,dx_rect,dy_rect)
    
    x0 = x_rect+dx_rect/6
    y0 = y_rect+dy_rect/3
    x1 = x0+8
    y1 = y0-6
    x2 = x1
    y2 = y1+12
    flèche_triangle = [(x0,y0),(x1,y1),(x2,y2)]
    
    x = x2
    y = (y1+y2)/2
    
    p1 = (x_rect+dx_rect/6+8,y)
    p2 = (x_rect+5*dx_rect/6,y)
    pygame.draw.line(window_surface, font_rect_color, p1, p2, 5)
    
    p1 = (x_rect+5*dx_rect/6,y)
    p2 = (x_rect+5*dx_rect/6,dy_rect/3+y)
    pygame.draw.line(window_surface, font_rect_color, p1, p2, 5)
    
    p1 = ((x_rect+5*dx_rect/6,dy_rect/3+y))
    p2 = (x,dy_rect/3+y)
    pygame.draw.line(window_surface, font_rect_color, p1, p2, 5)
    
    pygame.draw.rect(window_surface,font_rect_color, rect_return, 5)
    pygame.draw.polygon(window_surface,font_rect_color, flèche_triangle)
    
    return window_surface, rect_return

def aff_resultats(window_surface, window_resolution, font_color, resultats, debut, nb_res_aff):
    arial_font = pygame.font.SysFont("arial", 40)
    text_color = (255,255,255)
    font_rect_color = ("#746426")
    black_color = (0,0,0)
    line_color = ("#856d4d")
    nb_place = 20
    
    window_surface.fill(font_color)
    
    window_surface, rect_return = bouton_retour(window_surface, font_rect_color)
    
    x_rect = 70
    y_rect = 10
    dx_rect = 200
    dy_rect = 50
    rect_reset = pygame.Rect(x_rect,y_rect,dx_rect,dy_rect)
    pygame.draw.rect(window_surface,font_rect_color, rect_reset, 5)
    
    nb = arial_font.render("RESET", False, font_rect_color)
    p_nb = nb.get_rect(center=(rect_reset.x + rect_reset.width/2,rect_reset.y + rect_reset.height/2))
    window_surface.blit(nb,p_nb)
    
    rect_reset
    
    x_rect = window_resolution[0]/4
    y_rect = 0
    dx_rect = window_resolution[0]/4
    dy_rect = (nb_place+2)*window_resolution[1]/(nb_place+4)+10
    rect_winner = pygame.Rect(x_rect,y_rect,dx_rect,dy_rect)
    pygame.draw.rect(window_surface,font_rect_color, rect_winner, 5)
    
    x_rect = window_resolution[0]/2
    y_rect = 0
    dx_rect = window_resolution[0]/2
    dy_rect = (nb_place+2)*window_resolution[1]/(nb_place+4)+10
    rect_winner = pygame.Rect(x_rect,y_rect,dx_rect,dy_rect)
    pygame.draw.rect(window_surface,font_rect_color, rect_winner, 5)
    
    x_rect = window_resolution[0]/4+10
    y_rect = window_resolution[1]/(2*(nb_place+4))+10
    dx_rect = window_resolution[0]/4-10
    dy_rect = window_resolution[1]/(nb_place+4)-10
    rect_joueur = pygame.Rect(x_rect,y_rect,dx_rect,dy_rect)
    nb = arial_font.render("Gagnants", False, text_color)
    p_nb = nb.get_rect(center=(rect_joueur.x + rect_joueur.width/2,rect_joueur.y + rect_joueur.height/2))
    window_surface.blit(nb,p_nb)
    
    x_rect = window_resolution[0]/2+10
    y_rect = window_resolution[1]/(2*(nb_place+4))+10
    dx_rect = window_resolution[0]/6-10
    dy_rect = window_resolution[1]/(nb_place+4)-10
    rect_joueur = pygame.Rect(x_rect,y_rect,dx_rect,dy_rect)
    nb = arial_font.render("Perdants", False, text_color)
    p_nb = nb.get_rect(center=(rect_joueur.x + rect_joueur.width/2,rect_joueur.y + rect_joueur.height/2))
    window_surface.blit(nb,p_nb)
    
    pygame.display.flip()
    
    rect_parties = []
    for i in range(debut,nb_res_aff):
        for k in range(int(len(resultats[i])/2)):
            x_rect = 10
            y_rect = (i-debut+2)*window_resolution[1]/(nb_place+4)+10
            dx_rect = window_resolution[0]/4-10
            dy_rect = window_resolution[1]/(nb_place+4)-10
            rect_n_partie = pygame.Rect(x_rect,y_rect,dx_rect,dy_rect)
            nb = arial_font.render(str(i+1), False, text_color)
            p_nb = nb.get_rect(center=(rect_n_partie.x + rect_n_partie.width/2,rect_n_partie.y + rect_n_partie.height/2))
            window_surface.blit(nb,p_nb)
            
            rect_parties.append(rect_n_partie)
            
            if k == 0:
                x_rect = window_resolution[0]/4+10
                y_rect = (i-debut+2)*window_resolution[1]/(nb_place+4)+10
                dx_rect = window_resolution[0]/4-10
                dy_rect = window_resolution[1]/(nb_place+4)-10
                rect_joueur = pygame.Rect(x_rect,y_rect,dx_rect,dy_rect)
                print(resultats[i])
                nb = arial_font.render(str(resultats[i][2*k]), False, resultats[i][2*k+1])
                p_nb = nb.get_rect(center=(rect_joueur.x + rect_joueur.width/2,rect_joueur.y + rect_joueur.height/2))
                window_surface.blit(nb,p_nb)
                
            else:
                x_rect = (2+k)*window_resolution[0]/6+10
                y_rect = (i-debut+2)*window_resolution[1]/(nb_place+4)+10
                dx_rect = window_resolution[0]/6-10
                dy_rect = window_resolution[1]/(nb_place+4)-10
                rect_joueur = pygame.Rect(x_rect,y_rect,dx_rect,dy_rect)
                nb = arial_font.render(str(resultats[i][2*k]), False, resultats[i][2*k+1])
                p_nb = nb.get_rect(center=(rect_joueur.x + rect_joueur.width/2,rect_joueur.y + rect_joueur.height/2))
                window_surface.blit(nb,p_nb)
    
    x_rect = window_resolution[0]/4+10
    y_rect = (2*nb_place+5)*window_resolution[1]/(2*(nb_place+4))+10
    dx_rect = window_resolution[0]/4-10
    dy_rect = window_resolution[1]/(nb_place+4)-10
    rect_before = pygame.Rect(x_rect,y_rect,dx_rect,dy_rect)
    nb = arial_font.render("Page avant", False, text_color)
    p_nb = nb.get_rect(center=(rect_before.x + rect_before.width/2,rect_before.y + rect_before.height/2))
    window_surface.blit(nb,p_nb)
    
    x_rect = window_resolution[0]/2+10
    y_rect = (2*nb_place+5)*window_resolution[1]/(2*(nb_place+4))+10
    dx_rect = window_resolution[0]/4-10
    dy_rect = window_resolution[1]/(nb_place+4)-10
    rect_after = pygame.Rect(x_rect,y_rect,dx_rect,dy_rect)
    nb = arial_font.render("Page après", False, text_color)
    p_nb = nb.get_rect(center=(rect_after.x + rect_after.width/2,rect_after.y + rect_after.height/2))
    window_surface.blit(nb,p_nb)
    
    return window_surface, rect_return, rect_before, rect_after, rect_reset, rect_parties
    
def main():
    
    
    pygame.init()
    
    pygame.display.set_caption("Can't Stop")
    
    window_resolution = [1600,900]
    font_color = (220,228,203)
    black_color = (0, 0, 0)
    
    window_surface = pygame.display.set_mode(window_resolution, pygame.RESIZABLE)
    
    resultats = []
    resultats_joueurs = []
    fichier = open("resultats.txt","a+")
    fichier.close()
    fichier1 = open("joueurs.txt","a+")
    fichier1.close()
    with open("resultats.txt","r") as fichier:
        fic = fichier.read()
        elt = ""
        liste = []
        for i in range (len(fic)):
            if fic[i] != ";" and fic[i] != "|":
                elt += fic[i]
            elif fic[i] == "|":
                if elt[0] == "(" and elt[-1] == ")":
                    nb = ""
                    nbs = []
                    for k in range(len(elt)):
                        if elt[k] != "," and elt[k] != "(" and elt[k] != ")":
                            nb += elt[k]
                        elif elt[k] == "," or k == len(elt)-1:
                            nbs.append(int(nb))
                            nb = ""
                    elt = (nbs[0],nbs[1],nbs[2])
                liste.append(elt)
                elt = ""
            elif fic[i] == ";" :
                resultats.append(liste)
                liste = []
                elt = ""
    
    """
    with open("joueurs.txt","r") as fichier:
        fic = fichier.read()
        print(fic)
        elt = ""
        liste = []
        resultats_joueurs = []
        for i in range (len(fic)):
            joueurs = []
            if fic[i] != ";" and fic[i] != "|":
                elt += fic[i]
            elif fic[i] == "|":
                print(elt)
                if elt[0:6] == "Joueur":
                    inter_elt = ""
                    
                    nom = ""
                    nb_grimpeurs = 0
                    nb_pions = 0
                    pions = []
                    grimpeurs = []
                    des = []
                    for k in range(7,len(elt)-1):
                        if elt[k] != ":":
                            inter_elt += elt[k]
                        if elt[k] == ":":
                            print(inter_elt)
                            ### Nom ###
                            if "A" <= inter_elt[0] <= "Z" and "a" <= inter_elt[-1] <= "z":
                                nom = inter_elt
                            ### Pions/Grimpeurs ###
                            if inter_elt[0] == "[" and inter_elt[-1] == "]":
                                final_elt = ""
                                for j in range (len(inter_elt)):
                                    if ((inter_elt[j] and inter_elt[j+1]) != "," or (inter_elt[j] and inter_elt[j+1]) != " ") and j != len(inter_elt)-2:
                                        final_elt += inter_elt
                                    else:
                                        nb = [0,0]
                                        while i < 2:
                                            for i in range(5, len(final_elt)-1):
                                                if "0" <= final_elt[i] <= "12":
                                                    nb[i] += final_elt[i]
                                                else:
                                                    i + 1
                                        pion = Pion(nb[0],nb[1])
                                        if nb_grimpeurs != 0:
                                            grimpeurs.append(pion)
                                        else:
                                            pions.append(pion)
                            ### Nb_grimpeurs/Nb_pions ###                        
                            if inter_elt == "3" and nb_pions != None:
                                nb_grimpeurs = int(inter_elt[0])
                            elif "0" <= inter_elt <= "9":
                                nb_pions = int(inter_elt)
                            inter_elt = ""
                    joueur         
                    
                liste.append(elt)
                elt = ""
            elif fic[i] == ";" :
                resultats_joueurs.append(liste)
                liste = []
                elt = ""
        """
    launched =  True
    debut = 0
    nb_res_aff = 20
    #Rerhze|(196, 105, 143)|Ezfg|(4, 139, 154)|;
    while launched:
        window_surface.fill(font_color)
        window_surface, rects = menu(window_resolution,window_surface)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                launched = False
            elif event.type == pygame.MOUSEBUTTONUP:
                if (rects[0].x < pygame.mouse.get_pos()[0] < rects[0].x + rects[0].width and
                    rects[0].y < pygame.mouse.get_pos()[1] < rects[0].y + rects[0].height):
                    print("jeu lancé")
                    resultats_finaux, joueurs = jeu(window_surface, window_resolution, font_color)
                    resultats.append(resultats_finaux)
                    resultats_joueurs.append(joueurs)
                if (rects[1].x < pygame.mouse.get_pos()[0] < rects[1].x + rects[1].width and
                    rects[1].y < pygame.mouse.get_pos()[1] < rects[1].y + rects[1].height):
                    options(window_surface, window_resolution, font_color)
                if (rects[2].x < pygame.mouse.get_pos()[0] < rects[2].x + rects[2].width and
                    rects[2].y < pygame.mouse.get_pos()[1] < rects[2].y + rects[2].height):
                    if len(resultats) > 20+debut:
                        window_surface, rect_return, rect_before, rect_after, rect_reset, rect_parties = aff_resultats(window_surface, window_resolution, font_color, resultats, debut, nb_res_aff+debut)
                    else:
                        window_surface, rect_return, rect_before, rect_after, rect_reset, rect_parties = aff_resultats(window_surface, window_resolution, font_color, resultats, debut, len(resultats)-debut)
                    pygame.display.flip()
                    no_return = True
                    while no_return:
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                no_return = False
                                launched = False
                            elif event.type == pygame.MOUSEBUTTONUP:
                                if (rect_return.x < pygame.mouse.get_pos()[0] < rect_return.x + rect_return.width and
                                    rect_return.y < pygame.mouse.get_pos()[1] < rect_return.y + rect_return.height):
                                    no_return = False
                                    
                                if (rect_after.x < pygame.mouse.get_pos()[0] < rect_after.x + rect_after.width and
                                    rect_after.y < pygame.mouse.get_pos()[1] < rect_after.y + rect_after.height):
                                    if len(resultats)-debut > 20:
                                        debut += 20
                                    if len(resultats) > 20+debut:
                                        window_surface, rect_return, rect_before, rect_after, rect_reset, rect_parties = aff_resultats(window_surface, window_resolution, font_color, resultats, debut, nb_res_aff+debut)
                                    else:
                                        window_surface, rect_return, rect_before, rect_after, rect_reset, rect_parties = aff_resultats(window_surface, window_resolution, font_color, resultats, debut, len(resultats))
                                    pygame.display.flip()
                                if (rect_before.x < pygame.mouse.get_pos()[0] < rect_before.x + rect_before.width and
                                    rect_before.y < pygame.mouse.get_pos()[1] < rect_before.y + rect_before.height):
                                    if debut > 0:
                                        debut -= 20
                                    if len(resultats) > 20+debut:
                                        window_surface, rect_return, rect_before, rect_after, rect_reset, rect_parties = aff_resultats(window_surface, window_resolution, font_color, resultats, debut, nb_res_aff+debut)
                                    else:
                                        window_surface, rect_return, rect_before, rect_after, rect_reset, rect_parties = aff_resultats(window_surface, window_resolution, font_color, resultats, debut, len(resultats))
                                    pygame.display.flip()
                                    
                                if (rect_reset.x < pygame.mouse.get_pos()[0] < rect_reset.x + rect_reset.width and
                                    rect_reset.y < pygame.mouse.get_pos()[1] < rect_reset.y + rect_reset.height):
                                    resultats = []
                                    if len(resultats) > 20+debut:
                                        window_surface, rect_return, rect_before, rect_after, rect_reset, rect_parties = aff_resultats(window_surface, window_resolution, font_color, resultats, debut, nb_res_aff+debut)
                                    else:
                                        window_surface, rect_return, rect_before, rect_after, rect_reset, rect_parties = aff_resultats(window_surface, window_resolution, font_color, resultats, debut, len(resultats)-debut)
                                    pygame.display.flip()
                                
                                for i in range (len(rect_parties)):
                                    col = [2,4,6,8,10,12,10,8,6,4,2]
                                    xy_rect_tableau = [window_resolution[0]/1.5,window_resolution[1]]
                                    if (rect_parties[i].x < pygame.mouse.get_pos()[0] < rect_parties[i].x + rect_parties[i].width and
                                        rect_parties[i].y < pygame.mouse.get_pos()[1] < rect_parties[i].y + rect_parties[i].height):
                                        window_surface.fill(font_color)
                                        window_surface = fenêtre_de_base(window_resolution,black_color,window_surface,font_color)
                                        window_surface = tableau_de_base(col,xy_rect_tableau,window_surface)
                                        for j in range(len(resultats_joueurs[i])):
                                            window_surface = afficher_avancer_pions(resultats_joueurs[i][j],xy_rect_tableau,col,window_surface,j+1)
                                        
                                        
    with open("resultats.txt","w") as fic:
        ecrire = ""
        for i in range(len(resultats)):
            for k in range(len(resultats[i])):
                ecrire += str(resultats[i][k])
                ecrire += "|"
            ecrire += ";"
        fic.write(ecrire)
        
    with open("joueurs.txt","w") as fic:
        ecrire = ""
        for i in range(len(resultats_joueurs)):
            for k in range(len(resultats_joueurs[i])):
                ecrire += str(resultats_joueurs[i][k])
                ecrire += "|"
            ecrire += ";"
        fic.write(ecrire)
    pygame.quit()
        
############ On associe un joueur à ses dés, ses pions restants et ses grimpeurs placés ###############

def jeu(window_surface, window_resolution, font_color):
    #pygame.display.set_caption("Can't Stop")
    colonne = [2,4,6,8,10,12,10,8,6,4,2]
    black_color = (0, 0, 0)
    xy_rect_tableau = [window_resolution[0]/1.5,window_resolution[1]]
    xy_rect_interactions = [window_resolution[0]-window_resolution[0]/1.5,window_resolution[1]]
    resultats_finaux = []
    
    #window_surface = pygame.display.set_mode(window_resolution, pygame.RESIZABLE)
    
    jeu_continue = True
    while jeu_continue:
        
        window_surface.fill(font_color)
        joueurs = nb_joueurs(window_surface,window_resolution,black_color)
        
        window_surface.fill(font_color)
        pygame.display.flip()
        
        p = prio(len(joueurs))

        
        
        for i in range (len(joueurs)):
            name = ""
            x_name = True
            window_surface.fill(font_color)
            window_surface = afficher_i_joueur_debut(window_resolution, window_surface, i)
            window_surface = afficher_ecrire(window_resolution, window_surface)
            pygame.display.flip()
            while x_name:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        no_click = False
                        pygame.quit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN or len(name) >= 10:
                            x_name = False
                        elif event.key == pygame.K_BACKSPACE:
                            name = name[:-1]
                        else:
                            if len(name) == 0 and 97 <= event.key <= 122:
                                name = name + str(chr(event.key-32))
                            elif 97 <= event.key <= 122:
                                name = name + str(chr(event.key))
                            
                                
                        window_surface.fill(font_color)
                        window_surface = afficher_i_joueur_debut(window_resolution, window_surface, i)
                        window_surface = afficher_nom(name, window_resolution, window_surface, i)
                        window_surface = afficher_ecrire(window_resolution, window_surface)
                        pygame.display.flip()
            
            joueurs[i].nom = name
         
        window_surface.fill(font_color)
        window_surface = fenêtre_de_base(window_resolution,black_color,window_surface,font_color)
        window_surface = tableau_de_base(colonne,xy_rect_tableau,window_surface)
        pygame.display.flip()
                            
         
        
        win = False
        while not win:
            cont = True
            while cont:
                window_surface.fill(font_color)
                window_surface = fenêtre_de_base(window_resolution,black_color,window_surface,font_color)
                window_surface = tableau_de_base(colonne,xy_rect_tableau,window_surface)
                window_surface = afficher_avancer_grimpeurs(joueurs[p-1],xy_rect_tableau,colonne,window_surface)
                pygame.display.flip()
                #Définition des combinaisons de dés que le joueur peut jouer
                des = lancer_des()
                combis = addition(des)
                joueurs[p-1].des = test_place_pion(combis,joueurs[p-1],colonne)
                print(joueurs[p-1].des)
                
                #Quel choix parmis ses combinaisons de dés veut-il faire
                for i in range(len(joueurs)):
                    window_surface = afficher_avancer_pions(joueurs[i],xy_rect_tableau,colonne,window_surface,i+1)
                
                pygame.display.flip()
                
                if test_0_pions(joueurs[p-1].des):
                    rect,window_surface = choix_possibilité(joueurs[p-1].des,xy_rect_interactions,window_resolution,window_surface,joueurs[p-1],des,p)
                    
                    pygame.display.flip()
                    
                    col,window_surface = prendre_possibilité(joueurs[p-1].des,xy_rect_interactions,window_resolution,window_surface,rect)
                    pygame.display.flip()
                    
                    window_surface = rectangle_interaction(window_resolution,black_color,window_surface,font_color)
                    #Avec ce choix, faire avancer le(s) grimpeur(s)
                    joueurs[p-1].grimpeurs,joueurs[p-1].grimpeurs_restant,joueurs[p-1].pions_restant = avancer_pions(col,joueurs[p-1])
                    
                    window_surface = fenêtre_de_base(window_resolution,black_color,window_surface,font_color)
                    window_surface = tableau_de_base(colonne,xy_rect_tableau,window_surface)
                    for i in range(len(joueurs)):
                        window_surface = afficher_avancer_pions(joueurs[i],xy_rect_tableau,colonne,window_surface,i+1)
                    window_surface = afficher_avancer_grimpeurs(joueurs[p-1],xy_rect_tableau,colonne,window_surface)
                    
                    pygame.display.flip()
                    
                    #Ce joueur a-t-il gagné ?
                    complete = trois_lignes_complete(joueurs[p-1],colonne) + trois_grimpeurs_complete(joueurs[p-1],colonne)
                    if complete >= 3:
                        win = True
                        winner = joueurs[p-1]
                        cont = False
                        joueurs[p-1].pions, joueurs[p-1].grimpeurs, joueurs[p-1].pions_restant = enregistrer_pions(joueurs[p-1])
                        joueurs[p-1].grimpeurs_restant = len(joueurs[p-1].grimpeurs)
                        joueurs[p-1].des = []
                    else:
                        print(joueurs[p-1].pions)
                        print(joueurs[p-1].grimpeurs)
                        #Continuer ?
                        window_surface, rect_choix = afficher_continuer(xy_rect_interactions,window_resolution,window_surface)
                        pygame.display.flip()
                        cont = continuer(rect_choix)
                        joueurs[p-1].des = []
                        if not cont:
                            joueurs[p-1].pions, joueurs[p-1].grimpeurs, joueurs[p-1].pions_restant = enregistrer_pions(joueurs[p-1])
                            joueurs[p-1].grimpeurs_restant = len(joueurs[p-1].grimpeurs)
                            if p == len(joueurs):
                                p = 1
                            else:
                                p += 1
                        window_surface = rectangle_interaction(window_resolution,black_color,window_surface,font_color)
                        pygame.display.flip()
                       
                else:
                    window_surface = ecran_perdu(window_resolution,black_color,window_surface,font_color)
                    pygame.display.flip()
                    time.sleep(1)
                    joueurs[p-1].grimpeurs_restant = len(joueurs[p-1].grimpeurs)
                    joueurs[p-1].grimpeurs = [Pion(0,0),Pion(0,0),Pion(0,0)]
                    if p == len(joueurs):
                        p = 1
                    else:
                        p += 1
        
        resultats = []
        for i in range (len(joueurs)):
            if i == 0:
                color = (4, 139, 154)
            if i == 1:
                color = (196, 105, 143)
            if i == 2:
                color = (204, 153, 0)
            if i == 3:
                color = (130, 196, 108)
            if i != p-1:
                resultats.append(joueurs[i].nom)
                resultats.append(color)
            else:
                resultats.insert(0,joueurs[i].nom)
                resultats.insert(1,color)
        
        window_surface.fill(font_color)
        window_surface, jeu_continue = ecran_de_fin(window_resolution,black_color,window_surface,font_color,winner)
        pygame.display.flip()
        
        for i in range(len(resultats)):
            resultats_finaux.append(resultats[i])
    
    return resultats_finaux, joueurs

main()
