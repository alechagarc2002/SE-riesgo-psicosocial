# =========================
# REGRESIÓN LINEAL SIMPLE
# Ejemplo propio:
# Minutos de ejercicio vs calorías quemadas
#Queremos predecir cuántas calorías se queman según los minutos de ejercicio.
#X = minutos de ejercicio
#y = calorías quemadas
# =========================
# =========================
# REGRESIÓN LINEAL SIMPLE
# Ejemplo propio:
# Minutos de ejercicio vs calorías quemadas
# =========================

# Importamos NumPy para manejar datos numéricos
import numpy as np

# Importamos matplotlib para hacer gráficas
import matplotlib.pyplot as plt

# Importamos el modelo de regresión lineal
from sklearn.linear_model import LinearRegression

# Importamos función para dividir datos
from sklearn.model_selection import train_test_split

# Importamos métricas para evaluar el modelo
from sklearn.metrics import mean_squared_error, r2_score


# =========================
# PASO 1: CREAR DATOS
# =========================

# Fijamos semilla para que siempre salgan los mismos números aleatorios
np.random.seed(42)

# Generamos 50 valores de minutos de ejercicio (entre 10 y 60)
# Cada valor representa una persona
X = np.random.randint(10, 60, size=(50, 1))

# Generamos calorías quemadas
# Fórmula:
# calorías = 8 * minutos + 30 + ruido
#
# - 8 = calorías por minuto (aproximado)
# - 30 = base
# - ruido = variación real (personas diferentes queman distinto)
y = (8 * X).squeeze() + 30 + np.random.randn(50) * 20

# Mostramos algunos datos
print("Primeras 5 muestras:")
print(f"Minutos: {X[:5].flatten()}")
print(f"Calorías: {y[:5]}")


# =========================
# PASO 2: DIVIDIR DATOS
# =========================

# 80% entrenamiento, 20% prueba
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print(f"\nDatos de entrenamiento: {len(X_train)}")
print(f"Datos de prueba: {len(X_test)}")


# =========================
# PASO 3: ENTRENAR MODELO
# =========================

# Creamos el modelo
modelo = LinearRegression()

# Entrenamos el modelo
modelo.fit(X_train, y_train)

print("\nModelo entrenado")
print(f"Pendiente (calorías por minuto): {modelo.coef_[0]:.2f}")
print(f"Intercepto (base): {modelo.intercept_:.2f}")


# =========================
# PASO 4: PREDICCIONES
# =========================

# Predecimos con datos de prueba
y_pred = modelo.predict(X_test)

print("\nComparación:")
for i in range(5):
    print(f"Real={y_test[i]:.2f} | Predicho={y_pred[i]:.2f}")


# =========================
# PASO 5: EVALUACIÓN
# =========================

# Error promedio
mse = mean_squared_error(y_test, y_pred)

# Qué tan bueno es el modelo (1 = perfecto)
r2 = r2_score(y_test, y_pred)

print("\nEvaluación del modelo:")
print(f"MSE: {mse:.2f}")
print(f"R^2: {r2:.2f}")


# =========================
# PASO 6: GRÁFICA
# =========================

plt.figure(figsize=(10, 6))

# Datos de entrenamiento (gris)
plt.scatter(X_train, y_train, color='gray', alpha=0.5, label='Entrenamiento')

# Datos de prueba (azul)
plt.scatter(X_test, y_test, color='blue', edgecolors='black', label='Prueba')

# Línea del modelo
X_linea = np.linspace(X.min(), X.max(), 100).reshape(-1, 1)
y_linea = modelo.predict(X_linea)

plt.plot(X_linea, y_linea, color='red', linewidth=2, label='Modelo')

# Etiquetas
plt.title('Calorías quemadas según minutos de ejercicio')
plt.xlabel('Minutos de ejercicio')
plt.ylabel('Calorías')
plt.legend()
plt.grid(True, alpha=0.3)

plt.show()


# =========================
# PASO 7: PRUEBA FINAL
# =========================

# Queremos saber cuántas calorías se queman en 45 minutos
nuevo = np.array([[45]])

resultado = modelo.predict(nuevo)

print(f"\nSi haces 45 minutos de ejercicio...")
print(f"Quemas aproximadamente: {resultado[0]:.2f} calorías")