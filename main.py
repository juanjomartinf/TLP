class Enlace: #clase ENLACE
    def __init__(self, tra, dest):
        #variable que guarda la transicion entre nodos
        self.transicion = tra
        #variable que guarda el nodo destino del enlace
        self.destino = dest

    #metodo para sacar por pantalla el enlace
    def toString(self):
        out = "\t"
        out += "--"
        out += str(self.transicion)
        out += "-->("
        out += str(self.destino)
        out += ")\n"
        return out

class Nodo: #clase NODO
    def __init__(self, nomb):
        #variable que guarda el NOMBRE o id del nodo
        self.nombre = nomb
        #lista de objetos ENLACE que tiene un nodo
        self.enlaces = []
        #variable que guarda si el nodo es INICIAL "-->"
        self.inicial = False
        #variable que guarda si el nodo es FINAL "((  ))"
        self.final = False

    #método para añadir un objeto ENLACE a la lista de enlaces
    def addEnlace(self, tra, dest):
        enl = Enlace(tra, dest)
        self.enlaces.append(enl)

    #metodo para sacar por pantalla el nodo
    def toString(self):
        out = ""
        if self.inicial:
            out += "->"
        if self.final:
            out += "(("+self.nombre+")):\n"
        else:
            out += "("+self.nombre+"):\n"

        for e in self.enlaces:
            out += e.toString()
        return out
class Grafo: #clase GRAFO
    def __init__(self, entr):
        self.entrada = entr
        #lista de objetos NODO que tiene el grafo
        self.nodos = []
        #varibale que guarda el número de nodos intermedios
        self.numNodoInter = 0

    #método para añadir un objeto NODO a la lista de nodos, comprueba si
    #el nodo es el primero en añadirse y lo asigna como INICIAL
    def addNodo(self, nombN):
        n = Nodo(nombN)
        if len(self.nodos) == 0:
            n.inicial = True
        self.nodos.append(n)
        return n

    #método que añade un nodo INTERMEDIO llamados "Ik" | k >= 0
    def addNodoInt(self):
        n = Nodo("I" + str(self.numNodoInter))
        self.numNodoInter += 1
        self.nodos.append(n)
        return n

    #método que busca un nodo por su NOMBRE y lo devuelve. Si no lo encuentra
    #devuelve None
    def searchNodo(self, nomb):
        out = None
        for n in self.nodos:
            if n.nombre == nomb:
                out = n
        return out
    #método que devuelve un nodo por su nombre. Primero lo busca, si lo
    #encuentra lo devuelve. Si no lo encuentra, lo crea y lo devuelve.
    def getNodo(self, nomb):
        n = self.searchNodo(nomb)
        if(n == None):
            n = self.addNodo(nomb)
            if nomb == "FINAL":
                n.final = True
        return n

    #método que lee una entrada de datos y crea nodos y enlaces en el grafo
    def parsear(self):
        entrada = self.entrada.split()

        while len(entrada) > 0:
            palabra = entrada.pop(0)
            if palabra.endswith("->"): #nodoOrigen
                nombre = palabra.replace("->", "")
                nodoOrigen = self.getNodo(nombre)
            else:
                trans = None
                nodoDestino = None

                enlace = palabra.split("|")

                for e in enlace:
                    minusculas = []
                    mayusculas = []
                    #dividir los caracteres entre minusculas y MAYUSCULAS
                    for caract in e:
                        if caract == "€":
                            minusculas = []
                            mayusculas = []
                        elif caract.islower():
                            minusculas.append(caract)
                        elif caract.isupper():
                            mayusculas.append(caract)

                    if len(mayusculas) == 0:
                        nodoDestino = self.getNodo("FINAL")
                    elif len(mayusculas) == 1:
                        nodoDestino = self.getNodo(mayusculas.pop(0))

                    if len(minusculas) == 0:
                        nodoOrigen.addEnlace("€", nodoDestino.nombre)
                    elif len(minusculas) == 1:
                        trans = minusculas.pop(0)
                        nodoOrigen.addEnlace(trans, nodoDestino.nombre)
                    elif len(minusculas) > 1:
                        noOr = nodoOrigen
                        noDe = None

                        for m in range(len(minusculas)-1):
                            trans = minusculas.pop(0)
                            noDe = self.addNodoInt()
                            noOr.addEnlace(trans, noDe.nombre)
                            noOr = noDe
                        trans = minusculas.pop(0)
                        noOr.addEnlace(trans, nodoDestino.nombre)
    #metodo para sacar por pantalla el grafo
    def toString(self):
        out = "ENTRADA:\n\n"
        out += self.entrada + "\n"
        out += "\n"
        out += "GRAFO:\n\n"
        for n in self.nodos:
            out += n.toString() + "\n"
        out += "................................................"
        return out

if __name__ == "__main__":
    #print("Introducir cadena de caracteres:")
    #entrada = raw_input()
    entrada1 =   'A-> aB|bC\n'
    entrada1 +=  'C-> aC|bC|cB\n'
    entrada1 +=  'B-> bB|aD|a\n'
    entrada1 +=  'D-> aD|a|bB'

    entrada2 =   'S-> abA|B|baB|€\n'
    entrada2 +=  'A-> bA|b\n'
    entrada2 +=  'B-> aS|cb'

    g1 = Grafo(entrada1)
    g1.parsear()
    print (g1.toString())

    g2 = Grafo(entrada2)
    g2.parsear()
    print (g2.toString())
