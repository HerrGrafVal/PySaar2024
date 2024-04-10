from better_symbol import Sym

"""
Creates `better_symbol.Sym()` instances for material parameters in seperate namespace
"""

n_i = Sym("n_i", "Eigenleitungsdichte")
eps_r = Sym("epsilon_r", "Relative Permitivität")
W_g = Sym("W_g", "Bandlücke")

N_c = Sym("N_C", "Effektive Ladungsträgerdichte im Leitungsband") 
N_v = Sym("N_V", "Effektive Ladungsträgerdichte im Valenzband")

m_ed = Sym("m_ed^*", "Effektive Zustandsdichte-Massen für Elektronen")
m_hd = Sym("m_hd^*", "Effektive Zustandsdichte-Massen für Löcher")

m_ed = Sym("m_ec^*" ,"Effektive Leitfähigkeits-Massen für Elektronen")
m_hd = Sym("m_hc^*", "Effektive Leitfähigkeits-Massen für Löcher")