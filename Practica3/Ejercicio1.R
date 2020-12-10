# Cargar Datos
data <- read.csv("http://cardsorting.net/tutorials/25.csv")

# Eliminar columnas innecesarias
data$Comment <- NULL
data$Uniqid <- NULL
data[2:5] <- NULL

# Pasar categoría a minúscula (hay iguales)
data$Category <- tolower(data$Category)

# Agregar las filas con la misma categoría sumando apariciones
data <- aggregate(. ~ Category, data, sum)

