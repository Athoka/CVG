# Calculate Videogames Grade  
  
**CVG** es un predictor del éxito de un videojuego.  
Su misión es predecir la nota que va a obtener un videojuego en función de determinadas características proporcionadas por el usuario.  
  
La aplicación se alimenta con datos históricos de ventas y calificaciones de dos medios especializados. Estos datos son procesados para adaptarlos a un formato común, y mediante un análisis estadístico, cruzando con el valor de las variables proporcionadas por el usuario, se genera una calificación que se devuelve al usuario.  
  
## Diseño
Todo el proyecto está desarrollado en Python, ya que nos parece un lenguaje sencillo a la vez que potente y que permite una buena integración de Spark. 
  
La parte más importante del código es el fichero **patrons.py** que contiene las funcionalidades Spark: leer CSVs y convertirlos en RDDs en los que buscará los juegos que encajen en las categorías especificadas, agruparlos y calcular su media.
  
![Flujo Datos 1](/img/FlujoAplicacion1.PNG)  
  
El flujo de uso de la aplicación empieza con un menú **menu.py** en el que se le pide al usuario que introduzca los datos sobre los que se van a realizar los cálculos.  
  
***[menu.py](/Proyect/menu.py)***
```python
def get_data(op):
	platforms = ["PS4","XOne","WiiU","PSV", "3DS", "PC", "Android"] # the ones used on this moment
	correct = False
	while correct is False:
		platform = raw_input("Platform:")
		if platform in platforms:
			correct = True
			genre = raw_input("Genre:")
			dev = raw_input("Developer:")
			month = int(raw_input("Month of release (1-12):"))
			if month < 1 or month > 12:
				correct = False
				print("Wrong month!")
			else:
				correct = True
		else:
			print("Wrong platform, correct ones are: " + str(platforms))
	# Write down the data on a file which is going to be read later by the main program.
	file = open("data.txt", "w")
	file.write(str(op) + "," + platform + "," + genre + "," + dev + "," + str(month) + "\n")
	file.close()
```
  
Estos datos se le pasan a **patrons.py** que utilizando los datos históricos disponibles realiza el análisis estadístico de la entrada. El resultado final se guarda en un fichero ***result.txt***  
  
***[average example - patrons.py](/Proyect/patrons.py)***
```python
def developer_avg(metacriticData,sc,developer):
	#Do the statisticts related to the given developer

	# Search in Metacritic CSV
	developerMetacritic = metacriticData.filter(lambda line: developer in line).map(lambda line: (line[3],line[5],line[6]))

	if developerMetacritic.isEmpty() is False:
		developerMCritics = developerMetacritic.map(lambda line: (line[1])).reduce(lambda x,y: x+y)
		developerMUsers = developerMetacritic.map(lambda line: (line[2])).reduce(lambda x,y: x+y)
		developerMCount = developerMetacritic.count()
	else:
		developerMCritics = 0
		developerMUsers = 0
		developerMCount = 0

	#Calculate averega grade
	avgs_list,avg = average(developerMCritics,developerMUsers,0,developerMCount,0)

	result = sc.parallelize(avgs_list,1)
	result.saveAsTextFile("developers.txt")
	return avg
```
  
Por último el fichero **avgs.py** muestra la calificación final de los datos proporcionados  
  
***[avgs.py](/Proyect/avgs.py)***
```python
categories = ["Platform: ", "Genre: ", "Developer: ", "Month of release: ", "Expected grade: "]
categories2 = ["Platform: ", "Genre: ", "Developer: ", "Expected sales: "]

file_name = sys.argv[1]
file = open(file_name)
option = file.readline()
if  int(option) == 3:
	result = file.readline()
	print("The average is: " + result)
elif int(option) == 1:
	for i in range(5):
		avg = file.readline()
		avg = avg.rstrip("\n")
		print(categories[i] + avg)
	avg = int(avg)
	if avg <= 100 and avg >= 90:
		print("EXCELLENT!")
	elif avg < 90 and avg >= 70:
		print("GREAT")
	elif avg < 70 and avg >= 50:
		print("GOOD")
	else:
		print("SORRY :(")
elif int(option) == 2:
	 for i in range(4):
		avg = file.readline()
		avg = avg.rstrip("\n")
		print(categories2[i] + avg)

file.close()
```
  
## Infraestructura
  
Actualmente la aplicación esta diseñada para ser desplegada en un único nodo de hadoop con posibilidad de realizar paralelismo de tareas tal como se muestra a continuación.  
  
![Flujo Generico](/img/FlujoGenerico.PNG)  
  
Este despliegue nos permite una escalabilidad horizontal utilizando más nodos con hadoop de forma que sea posible servir las peticiones entrantes y adaptarse a la demanda  
 
## Uso de la aplicación
La interacción del usuario con el programa se produce gracias al un script en Bash que permite integrar todos los ficheros comentados en el apartado de diseño. Lo primero que ocurre es que se le muestra al usuario un menú mostrándole las posibles opciones que le ofrece nuestra aplicación. 

![Avgs](/img/avgs.jpg)

La primera opción es la predicción de notas. Tras seleccionar esta opción se le pedirá al usuario que introduzca por consola los datos sobre su videojuego: plataforma, género, desarrolladora y mes de lanzamiento. Estos datos se pasarán al programa principal para hayar las medias correspondientes a cada categoría y con ellas la media general. El resultado que se muestra al usuario es el siguiente:

![Avgs_Resultados](/img/res_avgs.jpg)

La segunda opción es casi idéntica solo que, en vez de predecir la nota, predice las ventas que se van a obtener. La petición de datos al usuario y el procesamiento de estos es igual que en el caso anterior pero cambiando la columna utilizada para calcular la media. El resultado que se muestra al usuario es muy similar al anterior:

![Ventas_Resultados](/img/res_sales.jpg)

La tercera es un mecanismo de consulta que permite al usuario buscar la media tanto de notas como de ventas de cualquiera de las categorías disponibles. Se le pedirá al usuario primero que indique si quiere conocer la media de las notas o de las ventas y segundo qué categoría quiere consultar. Por último se le pedirá que inserte un valor y, si ese valor se encuentra entre nuestros datos, se le mostrará la media pedida. Lo que se le muestra al usuario es lo siguiente:

![Menu_Stats](/img/menu_stats.jpg)

