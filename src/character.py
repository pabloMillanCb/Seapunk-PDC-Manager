from telegram.ext import (
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)
from telegram import Update
from constants import *
import json

class Character:

    def __init__(self, nombre, iniciativa, ataque, impacto, max_salud, resistencia_f):

        self.nombre = nombre
        self.salud_f = max_salud
        self.max_salud_f = max_salud
        self.resistencia_f = resistencia_f
        self.iniciativa = iniciativa
        self.ataque = ataque
        self.impacto = impacto
        self.estado = 0
        self.modificadores = 0

    def set_salud(self, vida):
        self.salud_f = vida
        self.checkear_estado()
    
    def damage(self, dam):
        self.salud_f -= max(0, dam-self.resistencia_f)
    
    def checkear_estado(self):
        if (self.salud_f >= self.max_salud_f/2):
            self.estado = 0
        if (self.salud_f < self.max_salud_f/2):
            self.estado = -3
        if (self.salud_f <= 0):
            self.estado = -6

    def tirada_combate(self, tirada):
        tirada = tirada + self.modificadores + self.estado
        encontrado = False

        i = 0
        while ((not encontrado) and i < 9):
            if (self.impacto + tirada in rango_impacto[i][0]):
                dados = rango_impacto[i][1]
                encontrado = True
            i += 1

        if (encontrado):
            return ("⚡️ Iniciativa: " +  str(self.iniciativa + tirada) + "\n" 
                    "👊 Ataque: " + str(self.ataque + tirada) + "\n" + 
                    "💥 Impacto: " + str(self.impacto + tirada) + "(🎲 " + str(dados) + "d6" + ")")
        else:
            return "Has introducido un numero fuera del rango"

    def print(self):
        return (self.nombre + "\n" +
                "❤️ SALUD: " + str(self.salud_f) + "/" + str(self.max_salud_f) + "\n" +
                "↕️ MODIFICADORES: " + str(self.modificadores) + "\n" +
                "💪 RESISTENCIA: " + str(self.res_f) + "\n" +
                "⚡️ Iniciativa: " +  str(self.iniciativa ) + "\n" 
                "👊 Ataque: " + str(self.ataque) + "\n" + 
                "💥 Impacto: " + str(self.impacto))
    
    def print_estado(self):
        return ("❤️ SALUD: " + str(self.salud_f) + "/" + str(self.max_salud_f) + "\n" +
                "↕️ MODIFICADORES: " + str(self.modificadores))