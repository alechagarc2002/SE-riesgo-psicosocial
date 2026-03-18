class SistemaExpertoPsicosocial:

    def __init__(self):
        # Base de hechos (axiomas): almacena respuestas del usuario
        self.hechos = {}

        # Base de conocimiento: lista de reglas
        self.reglas = []

        # Conclusiones generadas por el sistema
        self.conclusiones = {}

        # Traza: almacena el proceso de inferencia
        self.traza = []


    #  BASE DE CONOCIMIENTO 
    def definir_reglas(self):
        # Cada regla tiene:
        # - id: identificador
        # - premisas: condiciones (SI)
        # - conclusion: resultado (ENTONCES)
        # - certeza: nivel de confianza

        self.reglas = [

            # SI estrés alto Y poco sueño → Riesgo Alto
            {'id': 1,
             'premisas': [('estres_alto', True), ('poco_sueno', True)],
             'conclusion': 'Riesgo_Alto',
             'certeza': 0.9},

            # SI carga académica alta Y estrés alto → Riesgo Alto
            {'id': 2,
             'premisas': [('carga_alta', True), ('estres_alto', True)],
             'conclusion': 'Riesgo_Alto',
             'certeza': 0.85},

            # SI uso excesivo de redes Y poco sueño → Riesgo Medio
            {'id': 3,
             'premisas': [('uso_redes_excesivo', True), ('poco_sueno', True)],
             'conclusion': 'Riesgo_Medio',
             'certeza': 0.7},

            # SI poco apoyo familiar Y estrés alto → Riesgo Medio
            {'id': 4,
             'premisas': [('apoyo_familiar_bajo', True), ('estres_alto', True)],
             'conclusion': 'Riesgo_Medio',
             'certeza': 0.75},

            # SI bajo estrés Y buen sueño → Riesgo Bajo
            {'id': 5,
             'premisas': [('estres_bajo', True), ('buen_sueno', True)],
             'conclusion': 'Riesgo_Bajo',
             'certeza': 0.9}
        ]


    #  RECOLECCIÓN DE HECHOS 
    def obtener_sintomas(self):
        print("\nResponde con s/n\n")

        # Se pregunta al usuario y se guardan los hechos

        # Estrés
        self.hechos['estres_alto'] = input("¿Sientes estrés alto? ") == 's'
        self.hechos['estres_bajo'] = not self.hechos['estres_alto']

        # Sueño
        self.hechos['poco_sueno'] = input("¿Duermes menos de 6 horas? ") == 's'
        self.hechos['buen_sueno'] = not self.hechos['poco_sueno']

        # Carga académica
        self.hechos['carga_alta'] = input("¿Tu carga académica es alta? ") == 's'

        # Uso de redes
        self.hechos['uso_redes_excesivo'] = input("¿Usas redes más de 5 horas al día? ") == 's'

        # Apoyo familiar
        self.hechos['apoyo_familiar_bajo'] = input("¿Sientes poco apoyo familiar? ") == 's'


    def obtener_valor_hecho(self, nombre):
        # Verifica si el dato está en hechos
        if nombre in self.hechos:
            return self.hechos[nombre], 1.0  # certeza total

        # Verifica si es una conclusión previa
        if nombre in self.conclusiones:
            return True, self.conclusiones[nombre]

        # Si no existe, se considera falso
        return False, 0.0


    # MOTOR DE INFERENCIA 
    def motor_inferencia(self):

        # Variable para detectar cambios en conclusiones
        cambio = True

        # Mientras se generen nuevas conclusiones
        while cambio:
            cambio = False

            # Se evalúan todas las reglas
            for regla in self.reglas:

                # Evitar repetir conclusiones ya obtenidas
                if regla['conclusion'] in self.conclusiones:
                    continue

                cumple = True  # bandera para saber si se cumple la regla
                certeza_min = 1.0  # certeza mínima de las premisas
                detalles = []  # para guardar explicación

                # Evaluar cada premisa de la regla
                for nombre, esperado in regla['premisas']:
                    valor, certeza = self.obtener_valor_hecho(nombre)

                    # Si la condición se cumple
                    if valor == esperado:
                        detalles.append(f"{nombre}={valor}")

                        # Se toma la menor certeza (principio conservador)
                        certeza_min = min(certeza_min, certeza)
                    else:
                        cumple = False
                        break

                # Si todas las premisas se cumplen
                if cumple:
                    # Se calcula la certeza final
                    certeza_final = regla['certeza'] * certeza_min

                    # Se guarda la conclusión
                    self.conclusiones[regla['conclusion']] = certeza_final

                    # Se guarda la trazabilidad
                    self.traza.append({
                        'regla': regla['id'],
                        'conclusion': regla['conclusion'],
                        'certeza': certeza_final,
                        'premisas': detalles
                    })

                    cambio = True  # hubo cambios, se repite el ciclo


    #  SALIDA DEL SISTEMA 
    def mostrar_resultados(self):
        print("\n===== RESULTADOS =====")

        # Si no hay conclusiones
        if not self.conclusiones:
            print("No se detectó riesgo")
            return

        # Mostrar diagnósticos
        for c, certeza in self.conclusiones.items():
            print(f"{c.replace('_',' ')} ({round(certeza*100,2)}%)")

        # Recomendaciones según el nivel de riesgo
        print("\nRecomendación:")

        if 'Riesgo_Alto' in self.conclusiones:
            print("→ Apoyo psicológico")
        elif 'Riesgo_Medio' in self.conclusiones:
            print("→ Tutoría académica")
        else:
            print("→ Seguimiento")

        # Mostrar trazabilidad
        print("\nTrazabilidad del sistema:")

        for t in self.traza:
            print(f"\nRegla {t['regla']} activada")
            print(f"Conclusión: {t['conclusion']}")
            print(f"Premisas: {', '.join(t['premisas'])}")
            print(f"Certeza final: {t['certeza']:.2f}")


# PROGRAMA PRINCIPAL
if __name__ == "__main__":

    # Crear sistema experto
    se = SistemaExpertoPsicosocial()

    # Definir reglas
    se.definir_reglas()

    # Obtener datos del usuario
    se.obtener_sintomas()

    # Ejecutar inferencia
    se.motor_inferencia()

    # Mostrar resultados
    se.mostrar_resultados()