# 6GEI311 - Lab 2 - Partie 2
# Pieces jointes d'un ticket : texte, image ou video
# PieceJointe est abstraite, chaque sous-classe charge son fichier a sa facon

from abc import ABC, abstractmethod
import os


class PieceJointe(ABC):
    def __init__(self, chemin):
        self.chemin = chemin   # pour l'instant on garde juste le chemin du fichier

    # @abstractmethod oblige les sous-classes a ecrire ces methodes
    # (et on peut pas faire PieceJointe("...") directement)
    @abstractmethod
    def charger(self):
        pass

    @abstractmethod
    def exporterPDF(self):
        pass


class TextePieceJointe(PieceJointe):
    # pour un texte on lit vraiment le fichier
    def charger(self):
        try:
            with open(self.chemin, "r", encoding="utf-8") as f:
                contenu = f.read()
            print(f"[Texte] {contenu}")
            return contenu
        except FileNotFoundError:
            print(f"[Texte] Fichier introuvable : {self.chemin}")
            return ""

    def exporterPDF(self):
        contenu = self.charger()
        return f"--- Texte ({self.chemin}) ---\n{contenu}\n"


class ImagePieceJointe(PieceJointe):
    # pour une image on verifie qu'elle existe et on affiche sa taille
    def charger(self):
        if os.path.exists(self.chemin):
            taille = os.path.getsize(self.chemin)
            print(f"[Image] {self.chemin} chargée ({taille} octets)")
        else:
            print(f"[Image] Fichier introuvable : {self.chemin}")

    def exporterPDF(self):
        return f"--- Image : {self.chemin} ---\n"


class VideoPieceJointe(PieceJointe):
    # pour une video on verifie juste que le fichier est la
    def charger(self):
        if os.path.exists(self.chemin):
            print(f"[Vidéo] {self.chemin} prête à être lue")
        else:
            print(f"[Vidéo] Fichier introuvable : {self.chemin}")

    def exporterPDF(self):
        # on peut pas mettre une video dans un PDF, donc on met juste le chemin
        return f"--- Vidéo (chemin seulement) : {self.chemin} ---\n"
