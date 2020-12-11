#
#  Esse programa consiste no repositorio basico usado para acionar um interfone (porteiro eletronico) usando uma combinacao de impulsos do botao de campainha. 
# 
#  Guia de conexão:
#  Nome ..................... Descricao .............................. Pino digital
#  Campainha ................ Pino que recebe impulso da Campainha ... in: Pino a definir
#  Relefech ................. Rele da fechadura eletrica.............. out: Pino a definir
# 
 
import RPi.GPIO as gpio
from datetime import datetime, timedelta
import time
import PinagemZero

# Global
Campainha = PinagemZero.Campainha
Relefech = PinagemZero.Portao

duracaoPalma = 700;     #Valor representa um tempo em milissegundos, e o tempo que dura o som de uma palma, precisa ser calibrado entre 100 e 1000. 
tempototal = 3500;  #Valor representa um tempo em milissegundos, e o intervalo maximo permitido entre uma sequencia de palmas.
quantidadePalmas = 0; #Quantidade de palmas registradas.
debounceTime = 100;

#Funcoes
def action_event_campainha(gpio_pin):
    print ("Interrupcao iniciada")
    
    global quantidadePalmas
    quantidadePalmas = 0
    iniciototatal = datetime.now()
    momentoPalma = iniciototatal
    looping=1
    mudou=0
    ultimoestado = gpio.input(gpio_pin)
    while looping:
        if quantidadePalmas==0:
            quantidadePalmas = 1
            iniciototatal = datetime.now()
            momentoPalma = iniciototatal
            ultimoestado = gpio.input(gpio_pin)
        
        if gpio.input(gpio_pin) != ultimoestado:
            ultimoestado = gpio.input(gpio_pin)
            mudou=1
            #print("Estado alterado")
            #print(ultimoestado)
            momentoPalma =datetime.now()
            #time.sleep(0.01)
            
        if ((datetime.now()>(momentoPalma+timedelta(milliseconds=debounceTime)))and mudou):
            ultimoestado = gpio.input(gpio_pin)
            momentoPalma =datetime.now()
            quantidadePalmas = quantidadePalmas+1
            mudou=0
            #print(quantidadePalmas)
            #time.sleep(0.01)
            
        if datetime.now()>(iniciototatal+timedelta(milliseconds=tempototal)):
            looping=0
            
        if datetime.now()>(momentoPalma+timedelta(milliseconds=duracaoPalma)):
            looping=0
            
    if quantidadePalmas ==6:
        print("O código foi corretamente realizado. Abrindo portão.")
        print(quantidadePalmas)
        gpio.output(Relefech, gpio.HIGH)
        time.sleep(0.5)
        gpio.output(Relefech, gpio.LOW)
        quantidadePalmas = 0
    else:
        print("O código foi incorretamente realizado. Fazer nada.")
        print(quantidadePalmas)
        quantidadePalmas = 0


#Configuracoes de GPIO
# Configurando o modo do GPIO como BCM
gpio.setmode(gpio.board)
 
# Configurando PIN's como INPUT/OUTPUT e modo pull-down interno
gpio.setup(Campainha, gpio.IN, pull_up_down = gpio.PUD_DOWN)
gpio.setup(Relefech, gpio.OUT)
gpio.output(Relefech, gpio.LOW)

# Adicionando interrupcoes
gpio.add_event_detect(Campainha, gpio.RISING, callback=action_event_campainha, bouncetime=10)

#Loop
while True:
 try:
     
     if gpio.event_detected(Campainha):
         print ("Evento concluído.")
     else:
         print ("Aguardando")
         time.sleep(1)
 except (KeyboardInterrupt):
  print("Saindo")
  gpio.cleanup()
  exit()
