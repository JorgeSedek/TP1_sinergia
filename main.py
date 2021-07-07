#--------GRUPO: SINERGIA------------------#

"""
    Integrantes:

    -Jorge Sedek
    -Zoilo Pazos
    -Joaquín Maguiña
    -Leonardo Ayuso
    -Ruy Mori
    -Agustín Sánchez Vergara

    Fecha: 1° Cuatrimestre del 2021

"""
#---------IMPORTES--------------------------#
from configuraciones import check, constantes
from cuerpo_funciones import *
from entrada_de_datos import *
from salida_de_datos import *
from diccionario import *
from turnos import *


def main():

    
    dicc_constantes = constantes()
    verificacion_configuraciones = check(dicc_constantes)
    #--------CONSTANTES-----------------
    MAX_USUARIOS = dicc_constantes['MAX_USUARIOS']
    LONG_PALABRA_MIN = dicc_constantes['LONG_PALABRA_MIN']
    MAX_DESACIERTOS=dicc_constantes['MAX_DESACIERTOS']
    PUNTOS_ADIVINA_PALABRA=dicc_constantes['PUNTOS_ADIVINA_PALABRA']
    PUNTOS_RESTA_GANA_PROGRAMA=dicc_constantes['PUNTOS_RESTA_GANA_PROGRAMA']

    intento = 1
    respuesta = "si"
    ganador=None
    

    #Diccionario
    diccionario = generar_diccionario()
    generar_palaras_csv(diccionario)
    diccionario_total = {}

    #-------------mostrar configuraciones-----------
    print(f"{'Configuraciones':*^80}")
    for configuraciones in dicc_constantes:
        print(f'{configuraciones}: {dicc_constantes[configuraciones]}')
    print(verificacion_configuraciones)

    while respuesta == "si":


        #instrucciones para el usuario
        if intento == 1: instrucciones()


        if intento == 1:
            nombres = validar_nombres(MAX_USUARIOS)
        nombres_ordenados = ordenar_nombres_aleatoriamente(nombres,ganador)
        mensaje = f"Ingrese la longitud de palabra (ente {LONG_PALABRA_MIN} y 16) con la que desea jugar, o presione enter para que sea aleatoria: \n"
        longitud_palabra_elegida = input(mensaje)
        if longitud_palabra_elegida != '':
            while int(longitud_palabra_elegida) < LONG_PALABRA_MIN or int(longitud_palabra_elegida) > 16:
                longitud_palabra_elegida=input("Ingreso invalido: ")

        #inicializar diccionarios
        dicc_palabra_adivinar_e_secreta = crear_diccionario_palabras(nombres_ordenados,longitud_palabra_elegida,diccionario)
        dicc_aciertos_desaciertos = crear_diccionario_aciertos_desaciertos(nombres_ordenados)
        dicc_repetidas_incorrectas = crear_diccionario_letras_repetidas_e_incorrectas(nombres_ordenados)
        dicc_puntaje = crear_diccionario_puntaje(nombres_ordenados)

        palabra_adivinada = False
        jugador = 0
        nombres = nombres_ordenados[:]
        terminar = False

        while not palabra_adivinada and len(nombres_ordenados) != 0 and not terminar:
                if jugador >= len(nombres_ordenados) :
                    jugador = 0
                nombre = nombres_ordenados[jugador]
                turno_de_un_jugador(nombre,dicc_repetidas_incorrectas,dicc_palabra_adivinar_e_secreta,dicc_aciertos_desaciertos,dicc_puntaje)
                if dicc_aciertos_desaciertos[nombre][1] >= MAX_DESACIERTOS:
                    nombres_ordenados.remove(nombre)
                    jugador = jugador - 1

                palabra_adivinada = descubrio_palabra(nombre,dicc_palabra_adivinar_e_secreta)
                if palabra_adivinada:
                    ganador = nombre
                    dicc_puntaje[nombre][0] += PUNTOS_ADIVINA_PALABRA

                if len(nombres_ordenados) == 0:
                    for nombre in nombres:
                        dicc_puntaje[nombre][0] -= PUNTOS_RESTA_GANA_PROGRAMA

                jugador += 1
                if "fin" in dicc_repetidas_incorrectas[nombre][1]:
                    terminar = True

        sumar_partidas(dicc_puntaje,dicc_aciertos_desaciertos,diccionario_total,nombres,intento,ganador)

        mostrar_diccionarios(nombres,dicc_palabra_adivinar_e_secreta,dicc_aciertos_desaciertos,dicc_puntaje,ganador)


        respuesta = input("Queres seguir jugando? si/no: ").lower()
        intento += 1
    print(f"{'Puntaje total':*^80}")
    diccionario_total=dict(sorted(diccionario_total.items(),key=lambda i: i[1][0],reverse=True))
    mostrar_ultimo_diccionario(diccionario_total)
    print(f'se jugaron: {intento-1} partidas')

main()