#####################################################
# Camada Física da Computação
#Carareto
#11/08/2020
#Aplicação
####################################################


#esta é a camada superior, de aplicação do seu software de comunicação serial UART.
#para acompanhar a execução e identificar erros, construa prints ao longo do código! 


from enlace import *
import numpy as np
import time
import random

# voce deverá descomentar e configurar a porta com através da qual ira fazer comunicaçao
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports
# se estiver usando windows, o gerenciador de dispositivos informa a porta

#use uma das 3 opcoes para atribuir à variável a porta usada
serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
#serialName = "/dev/tty.usbmodem1411" # Mac    (variacao de)
#serialName = "ACM0"                  # Windows(variacao de)

def comandos():
    n = random.randint(10,30)
    print(f"Essa lista tera {n}")
    c1 = [b'\x00' b'\xFF' b'\x00' b'\xFF']
    c2 = [b'\x00' b'\xFF' b'\xFF' b'\x00']
    c3 = [b'\xFF']
    c4 = [b'\x00']
    c5 = [b'\xFF' b'\x00']
    c6 = [b'\x00' b'\xFF']
    cs = [c1,c2,c3, c4, c5, c6]
    i = 0
    cl = []
    while i < n:
        x = random.choice(cs)
        cl.append(x)
        i += 1
    return cl

def main():
    try:
        #declaramos um objeto do tipo enlace com o nome "com". Essa é a camada inferior à aplicação. Observe que um parametro
        #para declarar esse objeto é o nome da porta.
        com1 = enlace(serialName)
        start_time = time.time()

        
    
        # Ativa comunicacao. Inicia os threads e a comunicação seiral 
        com1.enable()
        if com1.enable() == True:
            print("Comunicação Aberta")
        #Se chegamos até aqui, a comunicação foi aberta com sucesso. Faça um print para informar.
        
        #aqui você deverá gerar os dados a serem transmitidos. 
        #seus dados a serem transmitidos são uma lista de bytes a serem transmitidos. Gere esta lista com o 
        #nome de txBuffer. Esla sempre irá armazenar os dados a serem enviados.
        print("Carregando Lista de Comandos para transmissão")
        txBuffer = comandos()
        print(txBuffer)
        tamanhoLista=len(txBuffer)
        print("Enviando Tamanho da lista")
        print("A lista tem {0} bytes".format(tamanhoLista.to_bytes(2, 'big')))
        com1.sendData(tamanhoLista.to_bytes(2, 'big'))
        print("Tamanho da lista enviado")

        print("Esperadno Confirmação")
        tamComando, nRx = com1.getData(2)
        print("Tamanho do Comando", tamComando) 
        tamanhoRecebido = int.from_bytes(tamComando, byteorder="big")
        print("tamanhoRecebido: " , tamanhoRecebido)
        if tamanhoLista == tamanhoRecebido:
            time.sleep(0.1)
            print("Tamanho CorreanhoRecebido:to")
            print("Transmitindo Lista")
            for i in txBuffer:
                com1.sendData(np.asarray(i))
                print("Enviado")
        else:
            print('Tamanho Errado')
            print("Lista não enviada :(  ")

        timer = time.time()

        while timer <= 10:

            resposta,nRx = com1.getData(2)
            

            
            respostaInt = int.from_bytes(resposta, byteorder="big")
            
            if respostaInt != len(txBuffer):
                print("erro")

            else: 
                print("okk!")
            
            print("A resposta é: ", respostaInt)
        

        #faça aqui uma conferência do tamanho do seu txBuffer, ou seja, quantos bytes serão enviados.

            
        #finalmente vamos transmitir os tados. Para isso usamos a funçao sendData que é um método da camada enlace.
        #faça um print para avisar que a transmissão vai começar.
        #tente entender como o método send funciona!
        #Cuidado! Apenas trasmitimos arrays de bytes! Nao listas!


        # A camada enlace possui uma camada inferior, TX possui um método para conhecermos o status da transmissão
        # Tente entender como esse método funciona e o que ele retorna


        #Agora vamos iniciar a recepção dos dados. Se algo chegou ao RX, deve estar automaticamente guardado
        #Observe o que faz a rotina dentro do thread RX
        #print um aviso de que a recepção vai começar.
        
        #Será que todos os bytes enviados estão realmente guardadas? Será que conseguimos verificar?
        #Veja o que faz a funcao do enlaceRX  getBufferLen
      
        #acesso aos bytes recebidos

        # Encerra comunicação
            print("-------------------------")
            print("Comunicação encerrada")
            print("-------------------------")
            com1.disable()
            print("--- {:.4f} seconds ---".format(time.time() - start_time))

    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com1.disable()
        

    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()
