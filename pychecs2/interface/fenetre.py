from tkinter import Canvas,Tk, Label, NSEW, Menu, Button
from pychecs2.echecs.piece import Pion, Tour, Fou, Cavalier, Dame, Roi
from pychecs2.interface.menu import *
from pychecs2.echecs.partie import Partie

class Canvas_echiquier(Canvas):


    def __init__(self, parent, n_pixels_par_case, la_partie):

        self.n_ligne = 8
        self.n_colonne = 8
        self.n_pixels_par_case = n_pixels_par_case
        self.couleur_1 = 'white'
        self.couleur_2 = 'gray'
        self.partie = la_partie
        self.case_selection = False

        self.piece_blanc_perdu = ""
        self.piece_noir_perdu = ""

        self.liste_mouvement_effectuer = []
        self.dernier_mouvement_effectuer = []

        self.chiffres_rangees_inverse= ['8', '7', '6', '5', '4', '3', '2', '1']
        self.lettres_colonnes = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']


        super().__init__(parent, width = self.n_ligne*self.n_pixels_par_case,
                     height = self.n_colonne*self.n_pixels_par_case)
        self.bind('<Configure>', self.redimensionner)

    # Méthode qui dessine les cases pour l'échiquier
    def dessiner_case(self):
        self.delete("case")
        for i in range(self.n_ligne):
            for j in range(self.n_colonne):
                x_coin_superieur_gauche = j*self.n_pixels_par_case
                y_coin_superieur_gauche = i*self.n_pixels_par_case
                x_coin_inferieur_droit = j*self.n_pixels_par_case + self.n_pixels_par_case
                y_coin_inferieur_droit = i*self.n_pixels_par_case + self.n_pixels_par_case

                if (i+j) % 2 == 0:
                    couleur = self.couleur_1

                else:
                    couleur = self.couleur_2

                chiffre_rangee = self.chiffres_rangees_inverse[i]

                lettre_colonne= self.lettres_colonnes[j]

                nom_case = 'case{}{}'.format(lettre_colonne,chiffre_rangee)

                self.create_rectangle(x_coin_superieur_gauche, y_coin_superieur_gauche,
                                      x_coin_inferieur_droit, y_coin_inferieur_droit, fill = couleur, tag = (nom_case,'case'))

    # Méthode qui va permettre de changer la couleur de la case de la pièce que le joueur a sélectionné
    def changer_couleur_position(self, colonne, ligne):
        self.supprimer_selection()
        self.case_selection = True
        self.coordonner_colonne = colonne
        self.coordonner_ligne = ligne
        x_coin_superieur_gauche = colonne*self.n_pixels_par_case
        y_coin_superieur_gauche = ligne*self.n_pixels_par_case
        x_coin_inferieur_droit = colonne*self.n_pixels_par_case + self.n_pixels_par_case
        y_coin_inferieur_droit = ligne*self.n_pixels_par_case + self.n_pixels_par_case


        self.create_rectangle(x_coin_superieur_gauche, y_coin_superieur_gauche,
                            x_coin_inferieur_droit, y_coin_inferieur_droit, fill = 'yellow', tag = 'selection')

        self.dessiner_piece()

    # Méthode qui permet de supprimer la sélection de la case
    def supprimer_selection(self):
        self.case_selection = False
        self.delete('selection')

    # Méthode qui permet à l'utilisateur de changer la couleur des cases de l'échiquier
    def changer_couleur_theme(self, couleur_1, couleur_2):

        self.couleur_1 = couleur_1
        self.couleur_2 = couleur_2
        self.delete('case')
        self.dessiner_case()

        self.dessiner_piece()


    # Méthode qui dessine les pièce dans l'échiquier.
    def dessiner_piece(self):
        self.delete('piece')
        for position, type_piece in self.partie.echiquier.dictionnaire_pieces.items():

            coordonnee_y = (self.n_ligne - self.partie.echiquier.chiffres_rangees.index(position[1]) - 1) * self.n_pixels_par_case + self.n_pixels_par_case // 2

            coordonnee_x = self.partie.echiquier.lettres_colonnes.index(position[0]) * self.n_pixels_par_case + self.n_pixels_par_case // 2

            self.create_text(coordonnee_x, coordonnee_y, text=type_piece,
                             font=('Deja Vu', self.n_pixels_par_case//2), tags='piece')

    #Redimentionnement ne fonctionne pas....
    def redimensionner(self, event):
        # Nous recevons dans le "event" la nouvelle dimension dans les attributs width et height. On veut un damier
        # carré, alors on ne conserve que la plus petite de ces deux valeurs.
        nouvelle_taille = min(event.width, event.height)

        # Calcul de la nouvelle dimension des cases.
        self.n_pixels_par_case = nouvelle_taille // self.n_ligne

        # On supprime les anciennes cases et on ajoute les nouvelles.
        self.delete('case')
        self.dessiner_case()

        # On supprime les anciennes pièces et on ajoute les nouvelles.
        self.delete('piece')
        self.dessiner_piece()

        if self.case_selection:
            self.changer_couleur_position(self.coordonner_colonne,self.coordonner_ligne)


class Fenetre(Tk,menu_global):

    def __init__(self):
        super().__init__()

        self.partie = Partie()

        self.title("Jeu d'échec")
        self.piece_selectionner = None
        self.nombre_déplacement = 0

        self.grid_columnconfigure(1, weight = 1)
        self.grid_rowconfigure(0, weight = 1)

        self.Canvas_echiquier = Canvas_echiquier(self, 80, self.partie)

        self.Canvas_echiquier.grid(sticky=NSEW,column = 1 ,row=0)

        self.creation_frame_rangee()
        self.affiche_liste_rangee.grid(column= 0,row =0 )

        self.creation_frame_colonne()
        self.affiche_liste_colonne.grid(column= 1,row =2 )

        self.messages_joueur = Label(self, font=('Deja Vu', 12))
        self.messages_joueur['text'] = "C'est au tour du joueur {}".format(self.partie.joueur_actif)
        self.messages_joueur.grid(column = 1, row = 3)

        self.messages= Label(self,font=('Deja Vu', 13))
        self.messages.grid( column= 1, row=4, rowspan=2)

        self.messages_piece = Label(self,font=('Deja Vu', 11))
        self.messages_piece['text'] = "Pièces qui on été mangées:"
        self.messages_piece.grid(column= 1,row =6)

        self.messages_piece_blanc = Label(self,font=('Deja Vu', 10))
        self.messages_piece_blanc['text'] = "Pièces blanches:"
        self.messages_piece_blanc.grid(column= 1, row=7)
        self.messages_piece_noir = Label(self, font=('Deja Vu', 10))
        self.messages_piece_noir['text'] = "Pièces noirs:"
        self.messages_piece_noir.grid(column= 1,row =8)

        self.creation_frame_droite()
        self.frame.grid(column = 2, row=0, rowspan=8, sticky = NSEW)

        self.Canvas_echiquier.bind('<Button-1>', self.selectionner_piece)
        self.Canvas_echiquier.bind('<Button-3>', self.deselectionner_piece)

        self.menu_bar_principal()


    #Création d'un frame à droit de l'échiquier pour avoir le temps joué des joueurs et la liste des déplacements effectués
    def creation_frame_droite(self):

        self.frame = Frame(self)

        self.messages_mouvement = Label(self.frame,font=('Deja Vu', 12))
        self.messages_mouvement['text'] = "Mouvement joué:"
        self.messages_mouvement.grid(column= 0,row=0 , columnspan= 2,padx= 110, pady= 15, sticky= N)

        self.creation_frame_mouvement()
        self.frame_mouvement.grid(column= 0,row=1, columnspan= 2,sticky= NSEW)

        self.bouton_annuler_dernier_coup = Button(self.frame,font=('Deja Vu', 11), text="Voir le\ndernier coup", command = self.voir_dernier_mouvement,width = 15)
        self.bouton_annuler_dernier_coup.grid(column = 0, row = 3, pady= 15)

        self.bouton_annuler_dernier_coup = Button(self.frame,font=('Deja Vu', 11), text="Annuler le\ndernier coup", command = self.annuler_mouvement,width = 15)
        self.bouton_annuler_dernier_coup.grid(column = 1, row = 3, pady= 15)

    # Création d'un frame pour pouvoir afficher la liste des mouvements effectués
    def creation_frame_mouvement(self):
        self.frame_mouvement = Frame(self.frame,width = 200,height= 450,padx= 20)

        self.scrollbar = Scrollbar(self.frame_mouvement, orient=VERTICAL)
        self.listbox_mouvement = Listbox(self.frame_mouvement, yscrollcommand=self.scrollbar.set,activestyle = 'none', height = 30)
        self.scrollbar.config(command=self.listbox_mouvement.yview)
        self.scrollbar.pack(side=RIGHT, fill=Y)
        self.listbox_mouvement.pack(side=LEFT, fill=BOTH, expand=1)

    # Création d'un frame pour pouvoir afficher les range de l'échiquier
    def creation_frame_rangee(self):
        self.affiche_liste_rangee = Frame(self)


        for rangee in self.Canvas_echiquier.chiffres_rangees_inverse:
            self.chiffres_rangees= Label(self.affiche_liste_rangee,width = 2,height= self.Canvas_echiquier.n_pixels_par_case//20)
            self.chiffres_rangees['text'] = rangee

            self.chiffres_rangees.grid()


    # Création d'un frame pour pouvoir afficher les colonnes de l'échiquier
    def creation_frame_colonne(self):
        self.affiche_liste_colonne = Frame(self)
        place_colonne = 0
        for element in self.Canvas_echiquier.partie.echiquier.lettres_colonnes:
            self.lettre_colonne= Label(self.affiche_liste_colonne,width= self.Canvas_echiquier.n_pixels_par_case//8)
            self.lettre_colonne['text'] = element

            self.lettre_colonne.grid(row= 0, column=place_colonne,sticky= N)
            place_colonne +=1


    # Méthode qui va permettre d'afficher le gagnant de la partie lorsque le Roi adverse a été "mangé".
    def annoncer_partie_gagner(self):
        self.popup_gagner = Toplevel()
        self.popup_gagner.title("Partie Terminer")
        self.messages_gagner = Label(self.popup_gagner,font=('Deja Vu', 12))
        self.messages_gagner['text'] = "Félicitation! \nLe joueur {} à gagné la partie!\n\n Voulez-vous jouer une nouvelle partie?".format(self.partie.joueur_actif)
        self.messages_gagner.grid(columnspan = 2)

        self.bouton_nouvelle = Button(self.popup_gagner,text="Oui", command =lambda:self.nouvelle_partie(),width = 10)
        self.bouton_quitter = Button(self.popup_gagner, text="Non, quitter", command = self.quit,width = 10)
        self.bouton_nouvelle.grid(column = 0, row = 1, pady= 10)
        self.bouton_quitter.grid(column = 1, row = 1, pady= 10)

    # Méthode qui lance le déselectionner pièce, donc supprimer la sélection de la pièce.
    def deselectionner_piece(self, event):
        self.piece_selectionner = None
        self.Canvas_echiquier.supprimer_selection()
        self.messages['text'] = ' '
        self.Canvas_echiquier.dessiner_case()
        self.Canvas_echiquier.dessiner_piece()

    # Méthode qui affiche la pièce sélectionner de l'échiquier
    def selectionner_piece(self, event):
        ligne = event.y // self.Canvas_echiquier.n_pixels_par_case
        colonne = event.x // self.Canvas_echiquier.n_pixels_par_case
        position = "{}{}".format(self.Canvas_echiquier.partie.echiquier.lettres_colonnes[colonne], int(self.Canvas_echiquier.partie.echiquier.chiffres_rangees[self.Canvas_echiquier.n_ligne- ligne - 1]))
        if self.piece_selectionner is None: # si une pièce est sélectionner, affichez la pièce sélectionner et la position.
            try:
                piece = self.Canvas_echiquier.partie.echiquier.dictionnaire_pieces[position]
                self.position_depart_selectionnee = position

                self.messages['foreground'] = 'blue'
                self.messages['text'] = 'Pièce séléctionné : {} {} à la position {}\nDéplacement valide en bleu.'.format(piece.__class__.__name__,piece.couleur, self.position_depart_selectionnee)
                self.couleur_piece_selectionner = self.Canvas_echiquier.partie.echiquier.couleur_piece_a_position(position)
                if self.couleur_piece_selectionner != self.partie.joueur_actif: # Message qui affiche si le joueur actif sélectionne une pièce du joueur adverse.
                    self.messages['foreground'] = 'red'
                    self.messages['text'] = "Vous essayer de jouer une pièce de l'autre joueur TRICHEUR!"
                    return None
                self.piece_selectionner = piece

                self.verifier_coup_valide(position, colonne, ligne)
            except KeyError: #Message d'erreur qui se lance lorsqu'il a aucune pièce sur la case sélectionné
                self.messages['foreground'] = 'red'
                self.messages['text'] = 'erreur aucune piece ici'

        #S'il y a une pièce déjà selectionné onva vers la fonction qui selectionne l'arriver
        else:
            self.selectionner_arriver(ligne, colonne)
    # Méthode qui permet d'afficher au joueur actif, les coups valides pour la pièce sélectionné
    def verifier_coup_valide(self, position_depart, colonne, ligne):
        self.Canvas_echiquier.dessiner_case()
        self.Canvas_echiquier.changer_couleur_position(colonne, ligne)
        self.Canvas_echiquier.dessiner_piece()

        for ligne in self.Canvas_echiquier.partie.echiquier.chiffres_rangees:
            for colonne in self.Canvas_echiquier.partie.echiquier.lettres_colonnes:
                position_arriver = "{}{}".format(colonne,ligne)
                if self.Canvas_echiquier.partie.echiquier.deplacement_est_valide(position_depart,position_arriver):

                    nom_case = "case{}{}".format(colonne,ligne)
                    case = self.Canvas_echiquier.find_withtag(nom_case)
                    self.Canvas_echiquier.itemconfig(case, fill = "sky blue1")

    # Méthode qui sélectionne la case d'arriver
    def selectionner_arriver(self, ligne, colonne):
        position = "{}{}".format(self.Canvas_echiquier.partie.echiquier.lettres_colonnes[colonne], int(self.Canvas_echiquier.partie.echiquier.chiffres_rangees[self.Canvas_echiquier.n_ligne- ligne - 1]))
        #cas s'il y a une pièce sur la case d'arriver
        if self.Canvas_echiquier.partie.echiquier.recuperer_piece_a_position(position) is not None:
            #si le joueur sélectionne une pièce de sa couleur on change la pièce sélectionné
            if self.couleur_piece_selectionner == self.Canvas_echiquier.partie.echiquier.couleur_piece_a_position(position):
                piece = self.Canvas_echiquier.partie.echiquier.dictionnaire_pieces[position]
                self.position_depart_selectionnee = position
                self.piece_selectionner = piece
                self.messages['text'] = 'Pièce séléctionné : {} {} à la position {}\nDéplacement valide en bleu.'.format(piece.__class__.__name__,piece.couleur, self.position_depart_selectionnee)

                self.verifier_coup_valide(position, colonne, ligne)

        self.position_arriver_selectionnee = position
        # si le déplacement est valide, nous allons faire appel au méthode, piece mangé, afficher dernier coup effectué, afficher la liste des mouvements,
        if self.partie.echiquier.deplacement_est_valide(self.position_depart_selectionnee,self.position_arriver_selectionnee) is True:

            self.piece_mange = self.Canvas_echiquier.partie.echiquier.recuperer_piece_a_position(self.position_arriver_selectionnee)

            self.Canvas_echiquier.dernier_mouvement_effectuer = [self.Canvas_echiquier.partie.joueur_actif,self.piece_selectionner,self.position_depart_selectionnee,self.position_arriver_selectionnee, self.piece_mange]

            self.Canvas_echiquier.liste_mouvement_effectuer += [self.Canvas_echiquier.dernier_mouvement_effectuer]


            self.message_mouvement(self.Canvas_echiquier.dernier_mouvement_effectuer)


            self.listbox_mouvement.see(END)


            self.partie.echiquier.deplacer(self.position_depart_selectionnee,self.position_arriver_selectionnee)


            # si la partie est terminé, appel à la méthode annoncer le gagnant.
            if self.Canvas_echiquier.partie.partie_terminee() == True:
                self.annoncer_partie_gagner()
            #promotion du pion s'il arrive à l'extremité de l'échiquier
            elif isinstance(self.piece_selectionner, Pion):
                if self.piece_selectionner.couleur == "blanc":
                    if ligne == 0:
                        self.menu_promotion(self.position_arriver_selectionnee, "blanc")

                if self.piece_selectionner.couleur == "noir":
                    if ligne == 7:
                        self.menu_promotion(self.position_arriver_selectionnee,"noir")

            self.changer_de_tour()
        #si le déplacement n'est pas valide on sort de la fonction
        else:
            return None

    #fenetre de la promotion du pion
    def menu_promotion(self,position, couleur):
        self.popup_promotion = Toplevel()
        self.popup_promotion.title("Promotion du pion")
        self.messages_promotion = Label(self.popup_promotion)
        self.messages_promotion['text'] = "Choisisez la pièce qui remplacera le pion"
        self.messages_promotion.grid(row= 0,columnspan = 2,padx= 10, pady= 10)

        self.bouton_reine = Button(self.popup_promotion,text="Reine",width=10, command =lambda :self.promotion(position, Dame, couleur))
        self.bouton_reine.grid(row= 1,column= 0,pady= 10)
        self.bouton_fou = Button(self.popup_promotion,text="Fou",width=10, command =lambda :self.promotion(position, Fou, couleur))
        self.bouton_fou.grid(row= 1,column= 1,pady= 10)
        self.bouton_cavalier = Button(self.popup_promotion,text="Cavalier",width=10, command =lambda :self.promotion(position, Cavalier, couleur))
        self.bouton_cavalier.grid(row= 2,column= 0,pady= 10)
        self.bouton_tour = Button(self.popup_promotion,text="Tour",width=10, command =lambda :self.promotion(position, Tour, couleur))
        self.bouton_tour.grid(row= 2,column= 1,pady= 10)

    #fonction de promotion on remplace le pion par la pièce désirer dans le dictionaire
    def promotion(self, position,piece, couleur):
        self.popup_promotion.destroy()
        self.Canvas_echiquier.partie.echiquier.dictionnaire_pieces[position]=piece(couleur)
        self.Canvas_echiquier.dessiner_case()
        self.Canvas_echiquier.dessiner_piece()

    #fonction qui change le joueur actif et qui remet la fenetre et la selection par défaut.
    def changer_de_tour(self):
        self.Canvas_echiquier.dessiner_case()
        self.Canvas_echiquier.dessiner_piece()
        self.piece_selectionner = None
        self.messages['text'] = ' '
        self.Canvas_echiquier.supprimer_selection()
        self.joueur_actif = self.partie.joueur_suivant()
        self.messages_joueur['text'] = "C'est au tour du joueur {}".format(self.partie.joueur_actif)

    #Méthode qui permet au joueur actif d'annuler le dernier mouvement effectué
    def annuler_mouvement(self):
        try:
            mouvement = self.Canvas_echiquier.liste_mouvement_effectuer[-1]
            self.nombre_déplacement -=1
            #cas s'il y avait une pièce de mangé
            if mouvement[4] is not None:
                self.Canvas_echiquier.partie.echiquier.dictionnaire_pieces[mouvement[3]]= mouvement[4]
                self.Canvas_echiquier.partie.echiquier.dictionnaire_pieces[mouvement[2]]= mouvement[1]

                #on enleve la pièce perdu de la liste des pièce perdu
                if mouvement[4].couleur == "blanc":
                    self.Canvas_echiquier.piece_blanc_perdu  = self.Canvas_echiquier.piece_blanc_perdu [:-1]
                    self.messages_piece_blanc['text'] = "Pièces blanches:" +self.Canvas_echiquier.piece_blanc_perdu


                if mouvement[4].couleur == "noir":
                    self.Canvas_echiquier.piece_noir_perdu = self.Canvas_echiquier.piece_noir_perdu [:-1]
                    self.messages_piece_noir['text']= "Pièces noirs:"+self.Canvas_echiquier.piece_noir_perdu
                #on change de tour et on enleve le mouvement de la liste
                self.changer_de_tour()
                del self.Canvas_echiquier.liste_mouvement_effectuer[-1]
                self.Canvas_echiquier.dernier_mouvement_effectuer = self.Canvas_echiquier.liste_mouvement_effectuer[-1]
                self.listbox_mouvement.delete(END)
                self.listbox_mouvement.delete(END)
                self.listbox_mouvement.delete(END)
                self.listbox_mouvement.delete(END)
                self.Canvas_echiquier.dessiner_piece()
            #cas s'il n'y a pas de pièce mangé
            else:
                self.Canvas_echiquier.partie.echiquier.dictionnaire_pieces[mouvement[2]]= mouvement[1]
                del self.Canvas_echiquier.partie.echiquier.dictionnaire_pieces[mouvement[3]]
                self.changer_de_tour()
                del self.Canvas_echiquier.liste_mouvement_effectuer[-1]
                self.listbox_mouvement.delete(END)
                self.listbox_mouvement.delete(END)
                self.listbox_mouvement.delete(END)
                self.Canvas_echiquier.dessiner_piece()
                vide = []
                #cas s'il n'y a pas d'autre mouvement à annuler
                if self.Canvas_echiquier.liste_mouvement_effectuer == vide:
                    self.Canvas_echiquier.dernier_mouvement_effectuer = vide
                else:
                    self.Canvas_echiquier.dernier_mouvement_effectuer = self.Canvas_echiquier.liste_mouvement_effectuer[-1]

        except (IndexError):    # Message d'erreur  lorsqu'il a aucun coup effectué
            self.messages['foreground'] = 'red'
            self.messages['text'] = "Il n'y a aucun coup de joué pour le moment."

    #Fonction qui crée les messages des mouvement et qui l'ajoute à la liste de la fenetre
    def message_mouvement(self,mouvement):
        couleur_piece_depart = mouvement[1].couleur

        self.nombre_déplacement += 1
        #cas s'il y a une pièce de manger
        if mouvement[4] is not None:
            couleur_piece_arriver = mouvement[4].couleur
            numero_deplacement = "Déplacement {}: Joueur {}".format(self.nombre_déplacement, mouvement[0])
            text_mouvement= "Le {} {} se déplace de la case {} à {}".format(mouvement[1].__class__.__name__,couleur_piece_depart,mouvement[2],mouvement[3])
            text_manger ="Puis, mange le {} {}".format(mouvement[4].__class__.__name__, couleur_piece_arriver)
            self.ajouter_piece_manger(mouvement[4])
            self.listbox_mouvement.insert(END,numero_deplacement)
            self.listbox_mouvement.itemconfig(END,fg= "blue")
            self.listbox_mouvement.insert(END, text_mouvement)
            self.listbox_mouvement.insert(END, text_manger)
            self.listbox_mouvement.itemconfig(END,fg= "red")
            self.listbox_mouvement.insert(END,"")
            self.listbox_mouvement.selection_clear(0, END)
        #cas s'il n'y a pas de pièce de manger
        else:

            numero_deplacement = "Déplacement {}: Joueur {}".format(self.nombre_déplacement,mouvement[0])
            text_mouvement= "Le {} {} se déplace de la case {} à {}".format(mouvement[1].__class__.__name__,couleur_piece_depart,mouvement[2],mouvement[3])
            self.listbox_mouvement.insert(END,numero_deplacement)
            self.listbox_mouvement.itemconfig(END,fg= "blue")
            self.listbox_mouvement.insert(END, text_mouvement)
            self.listbox_mouvement.insert(END, "")
            self.listbox_mouvement.selection_clear(0, END)

    # Méthode qui affiche tous les pièces "mangées" de l'échiquier
    def ajouter_piece_manger(self, piece_mange):
        #affiche les pièces blanche
        if piece_mange.couleur == "blanc":
            self.Canvas_echiquier.piece_blanc_perdu  += str(piece_mange)
            self.messages_piece_blanc['text'] = "Pièces blanches:" +self.Canvas_echiquier.piece_blanc_perdu
        #affiche les pièce noir
        elif piece_mange.couleur == "noir":
            self.Canvas_echiquier.piece_noir_perdu += str(piece_mange)
            self.messages_piece_noir['text'] = "Pièces noirs:"+self.Canvas_echiquier.piece_noir_perdu

    # Méthode qui va permettre aux joueurs de pouvoir voir le dernier mouvement joué avec l'aide d'un bouton.
    def voir_dernier_mouvement(self):
        try:
            print(self.Canvas_echiquier.liste_mouvement_effectuer)
            print(self.Canvas_echiquier.dernier_mouvement_effectuer)
            mouvement= self.Canvas_echiquier.dernier_mouvement_effectuer

            nom_case = "case{}".format(mouvement[2])
            case = self.Canvas_echiquier.find_withtag(nom_case)
            self.Canvas_echiquier.itemconfig(case, fill = "green yellow")

            nom_case = "case{}".format(mouvement[3])
            case = self.Canvas_echiquier.find_withtag(nom_case)
            self.Canvas_echiquier.itemconfig(case, fill = "medium orchid1")

            self.messages['foreground'] = 'blue'
            self.messages['text'] = "Dernier mouvement effectué:\ndéplacement de la case verte à la case mauve"

        except (IndexError): # Message d'erreur si aucun coup joué
            self.messages['foreground'] = 'red'
            self.messages['text'] = "Il n'y a aucun coup de joué pour le moment."



if __name__ == '__main__':
    f = Fenetre()
    f.mainloop()