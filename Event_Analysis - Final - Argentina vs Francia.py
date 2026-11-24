# ==================================================
# IMPORT LIBRARIES
# ==================================================

import json
import pandas as pd
import matplotlib.pyplot as plt

# ==================================================
# LOAD DATA
# ==================================================

MATCH_ID = 3869685
ruta = rf"C:\data\events\{MATCH_ID}.json"

def cargar_datos (ruta):

    with open( ruta, encoding="utf-8") as f:
        return json.load(f)

eventos = cargar_datos (ruta)

# ==================================================
# VARIABLES
# ==================================================

xg_equipo = {}
xg_jugador = {}
goles_jugador = {}
tipos_evento = {}
tiros_equipo = {}
goles_equipo = {}
tiros = []

# ==================================================
# DATA ANALYSIS USING PYTHON
# ==================================================

for evento in eventos:

    tipo = evento["type"]["name"]

    tipos_evento.setdefault(tipo, 0)

    tipos_evento[tipo] += 1


df_eventos = pd.DataFrame(
    sorted(
        tipos_evento.items(),
        key=lambda x: x[1],
        reverse=True
    ),
    columns=["Event", "Count"]
)

for evento in eventos:

    if evento["type"]["name"] == "Shot":

        tiros.append(evento)

for evento in eventos:

    if evento["type"]["name"] == "Shot":

        equipo = evento["team"]["name"]

        tiros_equipo.setdefault(equipo, 0)

        tiros_equipo[equipo] += 1

print("\nShots by Team\n")
print(tiros_equipo)

for evento in eventos:

    if evento["type"]["name"] == "Shot":

        if evento["shot"]["outcome"]["name"] == "Goal":

            equipo = evento["team"]["name"]

            goles_equipo.setdefault(equipo, 0)

            goles_equipo[equipo] += 1

print("\nGoals by Team\n")
print(goles_equipo)

for evento in eventos:

      
    if evento["type"]["name"] == "Shot":

        equipo = evento["team"]["name"]

        xg = evento["shot"]["statsbomb_xg"]

        xg_equipo.setdefault(equipo, 0)

        xg_equipo[equipo] += xg

        jugador = evento["player"]["name"]
        
        xg = evento["shot"]["statsbomb_xg"]
        
        xg_jugador.setdefault(jugador, 0)
        
        xg_jugador[jugador] += xg

        if evento["shot"]["outcome"]["name"] == "Goal":

            jugador = evento["player"]["name"]

            goles_jugador.setdefault(jugador, 0)

            goles_jugador[jugador] += 1

print("\nxG por equipo\n")
for equipo, total_xg in xg_equipo.items():

    print(
        equipo,
        round(total_xg, 2)
    )

# Calculate Expected Goals (xG)
# accumulated by each player

print("\nRanking xG por jugador\n")
for jugador, xg in sorted(
    xg_jugador.items(),
    key=lambda x: x[1],
    reverse=True
):

        print(
        jugador,
        round(xg, 2)
        )


ranking_xg = pd.DataFrame(
    sorted(
        xg_jugador.items(),
        key=lambda x: x[1],
        reverse=True
    ),
    columns=["Jugador", "xG"]
)

ranking_xg["xG"] = ranking_xg["xG"].round(2)

ranking_xg.to_csv(
    "ranking_xg_jugadores.csv",
    index=False,
    encoding="utf-8-sig"
)

ranking_goles = pd.DataFrame(
    sorted(
        goles_jugador.items(),
        key=lambda x: x[1],
        reverse=True
    ),
    columns=["Jugador", "Goles"]
)

ranking_goles.to_csv(
    "ranking_goles_jugadores.csv",
    index=False,
    encoding="utf-8-sig"
)

df_xg_equipos = pd.DataFrame(
    xg_equipo.items(),
    columns=["Equipo", "xG"]
)

df_xg_equipos["xG"] = df_xg_equipos["xG"].round(2)

df_xg_equipos.to_csv(
    "xg_equipos.csv",
    index=False,
    encoding="utf-8-sig"
)

df_eventos.to_csv(
    "event_types.csv",
    index=False,
    encoding="utf-8-sig"
)



# ==================================================
# Generated Graph - Top xG by Player
# ==================================================

top10_xg = (
    ranking_xg.head(10)
    .sort_values(by="xG")

)

plt.figure(figsize=(10,6))

plt.barh(
    top10_xg["Jugador"],
    top10_xg["xG"]
)

plt.title(
    "Top Players by xG - Argentina vs France"
)

plt.tight_layout()

plt.savefig("top10_xg_jugadores.png")

plt.close()


# ==================================================
# Generated Files
# ==================================================

print("\nGenerated Files:\n")

print("- xg_equipos.csv")

print("- ranking_xg_jugadores.csv")

print("- ranking_goles_jugadores.csv")

print("- top10_xg_jugadores.png")
