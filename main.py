class Enlace:
    def __init__(self, tra, dest):
        self.transicion = tra
        self.destino = dest

    def toString(self):
        out = ""
        out += "__"
        out += str(self.transicion)
        out += "__>("
        out += str(self.destino)
        out += ")\n"
        return out

class Nodo:
    enlaces = []
    inicial = False
    final = False

    def __init__(self, nomb):
        self.nombre = nomb

    def addEnlace(self, tra, dest):
        enl = Enlace(tra, dest)
        self.enlaces.append(enl)

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
class Grafo:
    nodos = []

    def addNodo(self, nomb):
        n = Nodo(nomb)
        if len(self.nodos) == 0:
            n.inicial = True
        self.nodos.append(n)
        return n
    def searchNodo(self, nomb):
        out = None
        for n in self.nodos:
            if n.nombre == nomb:
                out = n
        return out
    def getNodo(self, nomb):
        n = self.searchNodo(nomb)
        if(n == None):
            n = self.addNodo(nomb)
        return n

    def toString(self):
        #print (self.nodos)
        out = "\n"
        for n in self.nodos:
            out += n.toString()
            out += "\n"
        return out


    def parsear(self, entrada):
        entrada = entrada.split()
        print (entrada)

        while len(entrada) > 0:
            palabra = entrada.pop(0)
            if palabra.endswith("->"): #nodoOrigen
                nombre = palabra.replace("->", "")
                nodoOrigen = self.getNodo(nombre)
                print("ORIGEN: " + nodoOrigen.nombre)

            else:
                #print ("PALABRA: "+ palabra)
                trans = None
                nodoDestino = None

                enlace = palabra.split("|")
                for e in enlace:
                    #print ("ENLACE: " + e)
                    for caract in e:
                        if caract == "|":
                            trans = None
                            nodoDestino = None
                        if caract.islower():
                            print ("  tran: " + caract)
                            trans = caract
                        if caract.isupper():
                            print ("  dest: " + caract)
                            nodoDestino = caract
                if nodoDestino == None:
                    nodoDestino = self.getNodo("Final").nombre
                nodoOrigen.addEnlace(trans, nodoDestino)



if __name__ == "__main__":
    #print("Introducir cadena de caracteres:")
    #entrada = raw_input()
    entrada =   'A-> aB|bC\n'
    entrada +=  'C-> aC|bC|cB\n'
    entrada +=  'B-> bB|aD|a\n'
    entrada +=  'D-> aD|a|bB'
    print("Se ha introducido:\n" + entrada + "\n")
    g = Grafo()

    g.parsear(entrada)

    print("********************************************")
    print("*                 GRAFO                    *")
    print("********************************************")
    #print (g.toString())
