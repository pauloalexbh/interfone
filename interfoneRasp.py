 """
  Esse programa consiste no repositorio basico usado para acionar um interfone (porteiro eletronico) usando uma combinacao de impulsos do botao de campainha. 
 
  Guia de conexão:
  Nome ..................... Descricao .............................. Pino digital
  Campainha ................ Pino que recebe impulso da Campainha ... in: Pino a definir
  Relefech ................. Rele da fechadura eletrica.............. out: Pino a definir
  """
 
 
import RPi.GPIO as gpio
from datetime import datetime, timedelta
import time

""" Global """
Campainha = 17
Relefech = 18

duracaoPalma = 700;     #Valor representa um tempo em milissegundos, e o tempo que dura o som de uma palma, precisa ser calibrado entre 100 e 1000. 
tempototal = 3500;  #Valor representa um tempo em milissegundos, e o intervalo maximo permitido entre uma sequencia de palmas.
quantidadePalmas = 0; #Quantidade de palmas registradas.
debounceTime = 50;

""" Funcoes """
def action_event_campainha(gpio_pin):
 global quantidadePalmas
 iniciototatal = datetime.now()
 looping=1
 while datetime.now()<(iniciototatal+timedelta(milliseconds=tempototal)):
  
  if quantidadePalmas==0:
   quantidadePalmas = quantidadePalmas+1
   iniciototatal = datetime.now()
   momentoPalma = iniciototatal
   ultimoestado = gpio.input(gpio_pin)
   time.sleep(0.01)
 
  if gpio.input(gpio_pin) != ultimoestado:
   ultimoestado = gpio.input(gpio_pin)
   momentoPalma =datetime.now()
   time.sleep(0.01)
  
  if datetime.now()>(momentoPalma+timedelta(milliseconds=debounceTime)):
   ultimoestado = gpio.input(gpio_pin)
   momentoPalma =datetime.now()
   quantidadePalmas = quantidadePalmas+1
   time.sleep(0.01)
  
  if datetime.now()>(iniciototatal+timedelta(milliseconds=tempototal)):
   looping=0
  
  if datetime.now()>(momentoPalma+timedelta(milliseconds=duracaoPalma)):
   looping=0
 
 if quantidadePalmas ==6:
  print("O código foi corretamente realizado. Abrindo portão.")
  gpio.output(Relefech, gpio.HIGH)
  time.sleep(0.5)
  gpio.output(Relefech, gpio.LOW)
 else:
  print("O código foi incorretamente realizado. Fazer nada.")
  
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
  print ("Aguardando")
  time.sleep(1)
 except (KeyboardInterrupt):
  print("Saindo")
  gpio.cleanup()
  exit()
