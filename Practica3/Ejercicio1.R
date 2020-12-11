library(gplots)
library(RColorBrewer)
library(qgraph)

# Cargar Datos
data <- read.csv("http://cardsorting.net/tutorials/25.csv")

# Eliminar columnas innecesarias
data$Comment <- NULL
data$Uniqid <- NULL
data[2:5] <- NULL

# Histograma de todos los valores, vemos que son todo ceros y unos,
# Además vemos que aparecen muchos más ceros que unos (9:1)
hist(data.matrix(data[,-1]), main="Histograma de los valores de los datos")

# Trasponemos el dataframe
data <- as.data.frame(t(as.matrix(data)))
# Para poderlo usar con la función dist (que calcula la distancia entre 
# filas), quitamos la primera fila ya que es el nombre de la categoría
dst <- dist(data[-1,], diag=TRUE)

# Lo ponemos como matriz de datos numérica
dst <- data.matrix(dst)

# Obtenemos el número de categorías
dim <- ncol(dst)

# Dibujar una imagen donde el eje "z" es la distancia, de esta manera
# el color toma valores oscuros para distancias bajas
image(1:dim, 1:dim, -dst, axes = FALSE, xlab="", ylab="")

# Colocamos los nombres de las categorías en los ejes
axis(1, 1:dim, row.names(data)[-1], cex.axis = 0.5, las=3)
axis(2, 1:dim, row.names(data)[-1], cex.axis = 0.5, las=1)

# Colocamos los valores de las distancias en las posiciones correpsondientes
text(expand.grid(1:dim, 1:dim), sprintf("%0.1f", dst), cex=0.6)

# Hacemos el grafo de distancias. Utilizamos 1/dst porque cuanto menor 
# distancia mayor tamaño de arista.
dst <- 1/dst
qgraph(dst, layout='spring', labels = colnames(dst))

# Parece que las tarjetas más relacionadas son:
# Cake <-> Pie (Tartas)
# Pancakes <-> Waffles (Dulces de desayuno)
# Steak <-> Chicken (Carnes)
# Carrots <-> Onions <-> Brocoli <-> Lettuce (Verduras)
# Apple <-> Orange <-> Pineapple <-> Banana <-> Watermelon (Frutas)

# Dendrograma desde la matriz de distancias
plot(hclust(dist(data[-1,], diag=TRUE)), xlab="", ylab="", sub="")
