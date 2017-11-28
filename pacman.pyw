# -*- coding: latin-1 -*-

# importation de la librairie graphique
import wxRUR



# Classe de l'application Pacman
class AppPacman(wxRUR.Application) :
    def __init__(self,) :
        # Initialise l'application graphique (appel au constructeur parent)
        wxRUR.Application.__init__(self,"PACMAN","pacman.wld")
        self.SetColours("black", "black", "red", "black")
        self.SetGridColours("black")
        self.vitesse = 0
        self.duree = 0
        self.fin_du_game = False;
        while self.vitesse<1 or self.vitesse>9 :
            try:
                self.vitesse = self.InputInt("Choisissez votre vitesse\n(entre 1 et 9)")
                if self.vitesse<1 or self.vitesse>9 :
                    self.ShowMessage("La vitesse doit etre un entier entre 1 et 9")
            except ValueError:
                self.ShowMessage("Oops!  That was no valid number.  Try again...")
            except TypeError:
                self.ShowMessage("What did you do !?\nYou just quit the application")
                self.Quit()

        while self.duree<30 or self.duree>240:
            try:
                self.duree = self.InputInt("Choisissez votre duree en sec\n(entre 30 et 240)")
                if self.duree<30 or self.duree>240 :
                    self.ShowMessage("La duree doit etre un entier entre 30 et 240")
            except ValueError:
                self.ShowMessage("Oops!  That was no valid number.  Try again...")
        #
        robot1 = wxRUR.Robot(self, col=1, row=1, orient = 'E', name='ROBOT1', colour='light blue')
        robot2 = wxRUR.Robot(self, col=10, row=1, orient = 'W', name='ROBOT2', colour='blue')
        robot3 = wxRUR.Robot(self, col=1, row=10, orient = 'E', name='ROBOT3', colour='purple')
        robot4 = wxRUR.Robot(self, col=10, row=10, orient = 'W', name='ROBOT4', colour='green')
        robot5 = wxRUR.Robot(self, col=1, row=6, orient = 'E', name='ROBOT5', colour='grey')
        self.les_robots =[robot1, robot2, robot3, robot4, robot5]
        #
        self.numero_robot=0
        #
        self.deplacement = {'N':(0,1) , 'W':(-1,0), 'E':(1,0), 'S':(0,-1)}
        # Crée un attribut pacman en position (6,6) tourné vers l'est
        self.pacman = wxRUR.Robot(self, col=6, row=6, orient = 'E', name= 'PACMAN', colour='pacman'  )
        #
        self.cases_parcourues = [self.pacman.getPos()]
        self.distance_au_pacman(self.les_robots[0], direction='E')
        self.distance_au_pacman(self.les_robots[0], direction='S')
        # Association de la méthode 'deplacer_pacman'
        # à l'évènement "KeyEvent" (appui sur une touche)
        self.KeyEventHandler(onKeyEvent=self.deplacer_pacman)
        #
        period = 1.0/self.vitesse
        self.TimerEventHandler(onTimerEvent=self.deplacer_un_robot, TimerPeriod=period)
        #
        #self.TimerEventHandler(onTimerEvent=self.fin_du_game, TimerPeriod=self.duree)
        #
        self.pacman.set_trace_style(-1, "brown")
        # Boucle de gestion des évènements de l'application
        self.MainLoop(self.duree)
        if not self.fin_du_game:
            self.ShowMessage("Defeat\nToo long Baby !")
        # Fermeture de l'application
        message = "nombres de cases parcourues : "+ str(len(self.cases_parcourues)) + "\ntemps de jeu : " + str(self.TimeLoop()) + " secondes" + "\nscore : " + str(3*self.vitesse*len(self.cases_parcourues) - self.TimeLoop())
        self.ShowMessage(message)
        self.Quit()

    # Méthode évènementielle de déplacement du pacman
    def deplacer_pacman(self, KeyEvent):
        self.score_en_direct()
        ordre = KeyEvent.GetKeyCode()
        if ordre == wxRUR.WXK_UP:
            self.pacman.turn('N')
        elif ordre == wxRUR.WXK_LEFT:
            self.pacman.turn('W')
        elif ordre == wxRUR.WXK_RIGHT:
            self.pacman.turn('E')
        elif ordre == wxRUR.WXK_DOWN:
            self.pacman.turn('S')
        if self.pacman.front_is_clear():
            self.pacman.move()
            if not self.cases_parcourues.__contains__(self.pacman.getPos()):
                self.cases_parcourues.append(self.pacman.getPos())
                if self.cases_parcourues.__len__()==100:
                    self.ShowMessage('Congrats')
                    self.fin_du_game=True
                    self.ExitMainLoop()
            for Robot in self.les_robots:
                if self.pacman.getPos()==Robot.getPos():
                    self.ShowMessage("C'est la piquette Jack !\nTu sais pas jouer Jack !\nT'es mauvais !")
                    self.fin_du_game=True
                    self.ExitMainLoop()

    # Méthode évènementielle de déplacement d'un robot
    def deplacer_un_robot(self, TimerEvent):
        direc = self.direction_poursuite(self.les_robots[self.numero_robot])
        self.les_robots[self.numero_robot].turn(direc)
        self.les_robots[self.numero_robot].move()
        if self.pacman.getPos()==self.les_robots[self.numero_robot].getPos():
            self.ShowMessage("C'est la piquette Jack !\nTu sais pas jouer Jack !\nT'es mauvais !")
            self.fin_du_game=True
            self.ExitMainLoop()
        if self.numero_robot==self.les_robots.__len__()-1:
            self.numero_robot=0
        else:
            self.numero_robot += 1

    def distance_au_pacman(self, robot, direction):
        posX= robot.getPos()[0] + self.deplacement.get(direction)[0]
        posY= robot.getPos()[1] + self.deplacement.get(direction)[1]
        x=(posX-self.pacman.getPos()[0])**2
        y=(posY-self.pacman.getPos()[1])**2
        dist=(x+y)**0.5
        return dist

    def direction_poursuite(self, robot):
        min = 100
        direction = 'Robot bloqué'
        for dir in ['N', 'E', 'W', 'S']:
            if robot.is_clear(dir):
                if min > self.distance_au_pacman(robot, dir):
                    min = self.distance_au_pacman(robot, dir)
                    direction = dir
        return direction

    def score_en_direct(self):
        self.SetStatusText("Temps restant : " + str(self.duree - self.TimeLoop()) + " | Nb cases parcourues : " + str(len(self.cases_parcourues)) + " | Score : " + str(3*self.vitesse*len(self.cases_parcourues) - self.TimeLoop()))

# Crée une instance de l'application Pacman
appPacman = AppPacman()