# Calculate Videogames Grade

**Calculate Videogames Grade** es un predictor del éxito de un videojuego.  
Su misión es predecir la nota que va a obtener un videojuego en función de determinadas características proporcionadas por el usuario.

![Flujo Generico](/img/FlujoGenerico.PNG)

La aplicacion se alimenta con datos históricos de ventas y calificación de dos medios especializados, estos datos son procesados para adaptarlos a un formato común. Mediante un análisis estadístico, cruzando con el valor de las variables proporcionadas por el usuario, se genera una calificación que se devuelve al usuario.  

## Datos

Los datos empleados en la obtención de estádisticas han sido extraídos de los siguientes archivos CSV: [IGN](https://www.kaggle.com/egrinstein/20-years-of-games/data) y [Metacrític](https://www.kaggle.com/leonardf/releases-and-sales/data) 

El fichero de **IGN** contiene los siguientes datos de 18.625 videojuegos:
  - ID.
  - Nota en palabra.
  - Título.
  - URL en IGN.
  - Plataforma.
  - Nota según IGN.
  - Género.
  - Si se recomienda el juego o no.
  - Año de publicación.
  - Mes de publicación.
  - Día de publicación.  

Los datos que nos importan de este fichero son: la plataforma, la nota, el género y el año y mes de publicación. Nos hemos quedado con sólo estas columnas en un nuevo CSV.

El fichero de **Metacrític** contiene los siguientes datos de 16.719 videojuegos:
  - Nombre.
  - Plataforma.
  - Año de lanzamiento.
  - Género.
  - Compañía.
  - Ventas en América.
  - Ventas en Europa.
  - Ventas en Japón.
  - Ventas en otros sitios.
  - Ventas totales.
  - Nota de los críticos.
  - Nota de los usuarios.
  - Número de usuarios que ha puntuado.
  - Estudio de desarrollo.
  - Rating.  
  
Al igual que con el fichero de IGN, hemos creado uno nuevo para guardar los datos que nos interesan: plataforma, año de lanzamiento, género, compañía, ventas totales y nota tanto de críticos como de usuarios.

Los dos ficheros fueron parseados para poder ser tratados de forma más sencilla en Spark, no hay cambios sustanciales en los datos.


## Diseño
Todo el proyecto está desarrollado en Python, ya que nos parece un lenguaje sencillo a la vez que potente y que permite una buena integración de Spark. 

La parte más importante del código es el fichero **patrons.py** que contiene las funcionalidades Spark: leer CSVs y convertirlos en RDDs en los que buscará los juegos que encajen en las categorías especificadas, agruparlos y calcular su media.

## Uso de la aplicación
Cómo se usa

## Rendimiento
Velocidad, eficiencia... Cómo se han conseguido.

## Qué hemos aprendido
Cosas interesantes que hemos aprendido del proyecto.

## Qué podemos mejorar
Proponer mejoras.

## Conclusiones
Qué es lo que más nos ha gustado, lo que más nos ha costado, lo más frustrante y qué haríamos diferente.

## Nosotros
Proyecto realizado por:
 - Irene González Velasco.
 - Elena Kaloyanova Popova.
 - Víctor del Pino Castilla.
