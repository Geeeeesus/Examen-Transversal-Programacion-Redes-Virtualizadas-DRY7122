vlan = int(input("Número de VLAN: "))
print("Rango normal" if 1 <= vlan <= 1005 else
      "Rango extendido" if 1006 <= vlan <= 4094 else
      "Fuera de rango")
