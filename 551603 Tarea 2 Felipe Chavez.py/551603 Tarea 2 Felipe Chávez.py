# Tarea 2 Python en Minería 
# Felipe Chávez Cuevas/2020427089

import math

# Parte 1 — Definición de clase del explosivo, con parametros de entrada dados.

class Explosive:
    def __init__(self, name, density, detonation_velocity, relative_weight_strength, water_resistance, tech_sheet_path):
        self.name = name  # Nombre comercial del explosivo
        self.density = density  # Densidad en g/cm³
        self.detonation_velocity = detonation_velocity  # Velocidad de detonación en m/s
        self.relative_weight_strength = relative_weight_strength  # Potencia relativa al ANFO (%)
        self.water_resistance = water_resistance  # Resistencia al agua
        self.tech_sheet_path = tech_sheet_path  # Ruta a la ficha técnica

    def calculate_detonation_pressure(self):
        # 1.a) Presión de detonación en kPa (ρ * V² * 0.25)
        pressure = self.density * 1000 * self.detonation_velocity**2 * 0.25 / 1000
        return pressure

    def calculate_linear_density(self, diameter_mm):
        # 1.b) Densidad lineal (kg/m)
        radius_m = (diameter_mm / 1000) / 2
        area_m2 = math.pi * radius_m**2
        linear_density = self.density * 1000 * area_m2
        return linear_density

    def calculate_anfo_equivalent(self, explosiveweight_kg):
        # 1.c) Equivalente de explosivo a ANFO (kg)
        anfo_equivalent = explosiveweight_kg * (self.relative_weight_strength / 100) #Se realiza conversión a kg dividiendo por 100
        return anfo_equivalent

    def is_water_resistant(self):
        # 1.d) Devolución 'True' si es resistente al agua
        if isinstance(self.water_resistance, str):
            return self.water_resistance.lower() == "excelente"
        else:
            return bool(self.water_resistance)

# Parte 1 — Instanciación de explosivos 
detonita_5000 = Explosive("Detonita 5000", 1.15, 5200, 98.0, "Excelente", tech_sheet_path="fichas_tecnicas/Detonita famesa.png")
emultex_cn = Explosive("Emultex CN", 1.15, 5000, 101, "Excelente", tech_sheet_path="fichas_tecnicas/Emultex Enaex.png")

# Parte 1 — punto a: Presión de detonación
print("Parte 1 — punto a: Presión de detonación")
print(f"- {detonita_5000.name}: {detonita_5000.calculate_detonation_pressure():.2f} kPa")
print(f"- {emultex_cn.name}: {emultex_cn.calculate_detonation_pressure():.2f} kPa")

# Parte 1 — punto b: Densidad lineal para 140 mm
print("\nParte 1 — punto b: Densidad lineal para diámetro 140 mm")
print(f"- {detonita_5000.name}: {detonita_5000.calculate_linear_density(140):.2f} kg/m")
print(f"- {emultex_cn.name}: {emultex_cn.calculate_linear_density(140):.2f} kg/m")

# Parte 1 — punto c: Equivalente en ANFO para 500 kg
print("\nParte 1 — punto c: Equivalente en ANFO para 500 kg")
print(f"- {detonita_5000.name}: {detonita_5000.calculate_anfo_equivalent(500):.2f} kg")
print(f"- {emultex_cn.name}: {emultex_cn.calculate_anfo_equivalent(500):.2f} kg")

# Parte 1 — punto d: Resistencia al agua
print("\nParte 1 — punto d: Resistencia al agua")
print(f"- {detonita_5000.name}: {'Resistente' if detonita_5000.is_water_resistant() else 'No resistente'} al agua")
print(f"- {emultex_cn.name}: {'Resistente' if emultex_cn.is_water_resistant() else 'No resistente'} al agua")
# Parte 1 — Fichas técnicas
print("Parte 1: Fichas técnicas")
print(f"- {detonita_5000.name}: {detonita_5000.tech_sheet_path}")
print(f"- {emultex_cn.name}: {emultex_cn.tech_sheet_path}")


# Parte 2 — Herencia
# Definimos la clase BankBlasting que hereda de Explosive.
# Modelación de tronadura de banco con parametros geometricos y costos.
class BankBlasting(Explosive):
    def __init__(self, name, density, detonation_velocity, relative_weight_strength, water_resistance,
                 tech_sheet_path,
                 drill_diameter_mm, burden_m, spacing_m, bench_height_m, subdrilling_m, stemming_m,
                 explosive_cost_per_kg, drilling_cost_per_m):
        super().__init__(name, density, detonation_velocity, relative_weight_strength, water_resistance, tech_sheet_path)
        self.drill_diameter_mm = drill_diameter_mm # Diámetro de perforación en mm
        self.burden_m = burden_m # Burden (distancia entre filas) en metros
        self.spacing_m = spacing_m # Espaciamiento entre pozos en metros
        self.bench_height_m = bench_height_m  # Altura del banco en metros
        self.subdrilling_m = subdrilling_m # Pasadura o sobreperforación en metros
        self.stemming_m = stemming_m # Taco en collar
        self.explosive_cost_per_kg = explosive_cost_per_kg # Costo del explosivo por kg ($)
        self.drilling_cost_per_m = drilling_cost_per_m # Costo de perforación por metro ($)


    def calculate_charge_length(self):
        # Largo de carga útil = altura de banco + pasadura - taco
        return self.bench_height_m + self.subdrilling_m - self.stemming_m

    def calculate_linear_density(self):
        # Densidad lineal del explosivo en el pozo (kg/m)
        # Se usó diametro de perforación y dens explosivo.
        radius_m = (self.drill_diameter_mm / 1000) / 2
        area_m2 = math.pi * radius_m**2
        return self.density * 1000 * area_m2  # kg/m

    def calculate_charge_per_hole(self):
        # Carga explosivo por pozo(Kg).
        return self.calculate_linear_density() * self.calculate_charge_length()

    def calculate_volume_per_hole(self):
        # Volumen de roca tronada por pozo (m3)
        # Producto del Burden, espaciamiento y altura banco.
        return self.burden_m * self.spacing_m * self.bench_height_m

    def calculate_specific_consumption(self):
        # Consumo especifico del explosivo (kg/m3)
        # Carga por pozo/ vol tronado por pozo. 
        # 2.a)
        return self.calculate_charge_per_hole() / self.calculate_volume_per_hole()

    def calculate_anfo_equivalent_factor(self):
        # 2.b) Factor de carga equivalente en ANFO
        # Producto del consumo especifico por poterncia relativa (%)
        return self.calculate_specific_consumption() * (self.relative_weight_strength / 100)

    def calculate_cost_per_m3(self):
        # 2.c) Costo tronadura por m3
        # Suman del costo del explosivo por pozo y el costo de perforación,
        # Dividiendo por el volumen tronado por pozo.
        charge_per_hole = self.calculate_charge_per_hole()
        explosive_cost = charge_per_hole * self.explosive_cost_per_kg
        drilling_cost = (self.bench_height_m + self.subdrilling_m) * self.drilling_cost_per_m
        total_cost = explosive_cost + drilling_cost
        return total_cost / self.calculate_volume_per_hole()


# Parte 2 — Tronadura con Emultex CN
blast_emultex = BankBlasting(
    name="Emultex CN",
    density=1.15,
    detonation_velocity=5000,
    relative_weight_strength=101,
    water_resistance="Excelente",
    tech_sheet_path="fichas_tecnicas/Emultex Enaex.png",  # <- aquí se agrega
    drill_diameter_mm=140,
    burden_m=3.5,
    spacing_m=4.0,
    bench_height_m=12,
    subdrilling_m=1,
    stemming_m=3,
    explosive_cost_per_kg=2500,
    drilling_cost_per_m=13000
)

# Parte 2 — Resultados
print("\nParte 2 — Resultados")
a = blast_emultex.calculate_specific_consumption()
print(f"a) Factor de carga: {a:.2f} kg/m³")

b = blast_emultex.calculate_anfo_equivalent_factor()
print(f"b) Factor de carga equivalente en ANFO: {b:.2f} kg/m³")

c = blast_emultex.calculate_cost_per_m3()
print(f"c) Costo de la tronadura por m³: ${c:,.2f}")

