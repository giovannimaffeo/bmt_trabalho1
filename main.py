from SRC.PC.PC import main as PC
from SRC.GLI.GLI import main as GLI
from SRC.INDEX.INDEX import main as INDEX
from SRC.BUSCADOR.BUSCADOR import main as BUSCADOR


PC()
GLI()
vetorial_model, idf_df = INDEX()
BUSCADOR(vetorial_model, idf_df)


