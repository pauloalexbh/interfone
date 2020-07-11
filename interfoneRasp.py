#! /usr/bin/python
# -*- coding: utf-8 -*-
 
 """
  Esse programa consiste no repositorio basico usado para acionar um interfone (porteiro eletronico) usando uma combinacao de impulsos do botao de campainha. 
 
  Guia de conexão:
  Nome ..................... Descricao .............................. Pino digital
  Campainha ................ Pino que recebe impulso da Campainha ... in: Pino a definir
  Relefech ................. Rele da fechadura eletrica.............. out: Pino a definir
  """
 
 
import Rpi.GPIO as gpio
from datetime import datetime, timedelta
import time

""" Global """
Campainha = 17
Relefech = 18

delayfinal = 100;       //Valor representa um tempo em milissegundos, esse tempo e aguardado pelo programa para que se inicie novamente o loop.  
duracaoPalma = 700;     //Valor representa um tempo em milissegundos, e o tempo que dura o som de uma palma, precisa ser calibrado entre 100 e 1000. 
intervaloPalmas = 500;  //Valor representa um tempo em milissegundos, e o intervalo maximo permitido entre uma sequencia de palmas.
tempototal = 3500;  //Valor representa um tempo em milissegundos, e o intervalo maximo permitido entre uma sequencia de palmas.
limiteoscilacao = 50;
oscilacao = 0;
iniciototal = 0;  //Marcador que indica o momento do inicio da primeira palma.
quantidadePalmas = 0;   //Quantidade de palmas registradas.
momentoPalma = 0;      //Marcador usado para a detecção das palmas, sera utilizado junto com a funcao millis. 
esperaPalmas = 0;      //Marcador usado para contagem dos intervalos de tempo, sera utilizado junto com a funcao millis.
debounceTime = 50;

""" Funcoes """
def action_event_campainha(gpio_pin):


""" Configuracoes de GPIO """
# Configurando o modo do GPIO como BCM
gpio.setmode(gpio.BCM)
 
# Configurando PIN's como INPUT/OUTPUT e modo pull-down interno
gpio.setup(Campainha, gpio.IN, pull_up_down = gpio.PUD_DOWN)
gpio.setup(Relefech, gpio.OUT)
gpio.output(Relefech, gpio.LOW)

# Adicionando interrupcoes
gpio.add_event_detect(Campainha, gpio.BOTH, callback=action_event_campainha)



"""Loop"""
while True:
    try:
        if gpio.event_detected(Porta):
            action_event_button(Porta)
            #gpio.remove_event_detect(PIN)
        
        else:
                    print("Botão Desligado")
        if gpio.event_detected(Tranca):
            action_event_button(Tranca)
            #gpio.remove_event_detect(PIN)
        
        else:
                    print("Botão Desligado")
 
        time.sleep(1)
    except (KeyboardInterrupt):
        print("Saindo...")
        gpio.cleanup()
        exit()
