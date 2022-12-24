from telegram.ext import (
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from constants import *
from character import *

main_menu_buttons = [["Crear Personaje"], ["Realizar Tirada"]]

################################################
# Conversation handler para crear el personaje #
################################################


async def new_char(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.user_data:
        context.user_data["personajes"] = []
    await update.message.reply_text(
        "Introduce el nombre de tu personaje:",
        reply_markup=ReplyKeyboardRemove(),
    )
    return 1

async def nombre(update: Update, context: ContextTypes.DEFAULT_TYPE):

    context.user_data["nombre"] = update.message.text
    await update.message.reply_text(
        "Introduce la ⚡️ INICIATIVA"
    )
    return 2

async def iniciativa(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if (update.message.text.isnumeric()):
        context.user_data["iniciativa"] = int(update.message.text)
        await update.message.reply_text(
            "Introduce el 👊 ATAQUE"
        )
        return 3
    else:
        await update.message.reply_text(
            "Tienes que introducir un número, por ejemplo 5"
        )
        return 2

async def ataque(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if (update.message.text.isnumeric()):
        context.user_data["ataque"] = int(update.message.text)
        await update.message.reply_text(
            "Introduce el 💥 IMPACTO"
        )
        return 4
    else:
        await update.message.reply_text(
            "Tienes que introducir un número, por ejemplo 9"
        )
        return 3

async def impacto(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if (update.message.text.isnumeric()):
        context.user_data["impacto"] = int(update.message.text)
        await update.message.reply_text(
            "Introduce la ❤️ SALUD FISICA MAXIMA"
        )
        return 5
    else:
        await update.message.reply_text(
            "Tienes que introducir un número, por ejemplo 11"
        )
        return 4

async def salud(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if (update.message.text.isnumeric()):
        context.user_data["salud"] = int(update.message.text)
        await update.message.reply_text(
            "Introduce la 💪 RESISTENCIA FISICA"
        )
        return 6
    else:
        await update.message.reply_text(
            "Tienes que introducir un número, por ejemplo 23"
        )
        return 5

async def resistencia(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if (update.message.text.isnumeric()):
        context.user_data["resf"] = int(update.message.text)
        context.user_data["personajes"].append( Character(context.user_data["nombre"], context.user_data["iniciativa"],
                                                        context.user_data["ataque"], context.user_data["impacto"],
                                                        context.user_data["salud"], context.user_data["resf"]) )
        await update.message.reply_text(
            "✅ Personaje creado con éxito ✅",
            reply_markup=ReplyKeyboardMarkup(
                main_menu_buttons, one_time_keyboard=False
            ),
        )
        return 7
    else:
        await update.message.reply_text(
            "Tienes que introducir un número, por ejemplo 4"
        )
        return 6

async def cancel_char(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(
        #"Se ha cancelado la creacion del personaje",
        reply_markup=ReplyKeyboardRemove(),
    )

#########################################################
# Conversation handler para realizar Tiradas de Combate #
#########################################################

async def pedir_tirada(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(
        "Escribe tu Tirada de Combate",
        reply_markup=ReplyKeyboardMarkup(
            [["Volver"]], one_time_keyboard=False
        ),
    )
    return 1

async def muestra_tirada(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if (update.message.text.isnumeric()):
        if (context.user_data.get("personajes")):
            await update.message.reply_text(
                context.user_data["personajes"][0].tirada_combate(int(update.message.text))
            )
        else:
            await update.message.reply_text(
                "No has creado ningún personaje. Por favor crea uno."
            )
        return 1
    else:
        await update.message.reply_text(
            "Introduce solo un número (por ejemplo: 11)"
        )
        return 1

async def cancelar_tirada(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(
        "Volviendo al menu principal",
        reply_markup=ReplyKeyboardMarkup(
            main_menu_buttons, one_time_keyboard=False
        ),
    )
    return 2

##################
# Menu Principal #
##################

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Comenzamos",
        reply_markup=ReplyKeyboardMarkup(
            main_menu_buttons, one_time_keyboard=False
        ),
    )
    return 1

######################################################################################

create_character = ConversationHandler(
        entry_points=[MessageHandler(filters.Regex("^(Crear Personaje)$"), new_char)],
        states={
            1: [MessageHandler(filters.TEXT & ~filters.COMMAND, nombre)],
            2: [MessageHandler(filters.TEXT & ~filters.COMMAND, iniciativa)],
            3: [MessageHandler(filters.TEXT & ~filters.COMMAND, ataque)],
            4: [MessageHandler(filters.TEXT & ~filters.COMMAND, impacto)],
            5: [MessageHandler(filters.TEXT & ~filters.COMMAND, salud)],
            6: [MessageHandler(filters.TEXT & ~filters.COMMAND, resistencia)],
        },
        fallbacks=[CommandHandler("cancelar", cancel_char)],
        map_to_parent={
            7: 1
        }
    )

do_tc = ConversationHandler(
        entry_points=[MessageHandler(filters.Regex("^(Realizar Tirada)$"), pedir_tirada)],
        states={
            1: [MessageHandler(filters.TEXT & ~filters.COMMAND & ~filters.Regex("^(Volver)$"), muestra_tirada),
                MessageHandler(filters.Regex("^(Volver)$"), cancelar_tirada)],
        },
        fallbacks=[CommandHandler("cancelar", cancel_char)],
        map_to_parent={
            2: 1
        },
    )

main_menu = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            1: [create_character, do_tc],
        },
        fallbacks=[CommandHandler("cancelar", cancel_char)],
    )