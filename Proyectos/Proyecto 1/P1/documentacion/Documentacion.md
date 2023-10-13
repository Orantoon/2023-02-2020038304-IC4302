# **Base de Datos II (IC4302)** – Semestre 2, 2023
### **Proyecto 1** 
### **WikiSearch** 
### Jesús Andrés Cortés Álvarez  – 2021579439
### Aaron Ortiz Jimenez  – 2022437529
### David Suárez Acosta – 2020038304

---

## **Ejecución del proyecto**

El siguiente sistema implementa un buscador para el sitio web de Wikipedia, utilizando dos motores de bases de datos como lo son Mongo Atlas y Autonomous databse de Oracle, para obtener el contenido del sitio ya mencionado se utilizará los XML dumps.

Como primer paso desde MobaXterm desde la carpeta P1 donde se encuentra el proyecto, se ejecuta el siguiente código, se presenta una imagen de ejemplo de la ejecución.

```
terraform init

terraform apply --var-file=config/group.tfvars

```
![inicio](/imagenes/inicio.png) 

Para visualizar el funcionamiento del sistema desarrollado, se debe ingresar a la aplicación "Postman".

![postman1](/imagenes/postman1.png) 

Al ingresar se presenta un espacio para ingresar la ruta del método que desea implementar, para obtener los datos deseados para este proyecto, se utilizará el método "buscaGene" para la base datos de Mongo para obtener los datos generales según un texto para realizar la búsqueda, también se tiene el método "buscarFiltros", realiza la búsqueda en la base de datos de Mongo tomando en cuenta el filtro deseado. A continuación, se presentan ejemplos de la explicación anterior.

La siguiente imagen presenta la estructura que debe tener la ruta para realizar la busqueda correctamente.

![filtro1](/imagenes/filtro1.png)

**Resultados**

![prueba11](/imagenes/prueba11.png) 

![prueba22](/imagenes/prueba22.png) 

![prueba33](/imagenes/prueba33.png) 

Seguidamente se presenta un ejemplo del método que se debe utilizar para realizar la búsqueda en la base de datos de Autonomous, en este caso el método a utilizar seria "getData" para visualizar los datos requeridos.

La siguiente imagen presenta la estructura que debe tener la ruta para realizar la búsqueda correctamente.

![pruebaA](/imagenes/pruebaA.png)

**Resultados**

![pruebaB](/imagenes/pruebaB.png) 

![pruebaC](/imagenes/pruebaC.png)


---
## Explicación de proceso de Facets 
**Facets Mongo**

![facet1](/imagenes/facet1.png)

Las siguientes rutas con utilizadas para realizar filtros: 

**Filtros**

En la siguiente ruta se aplican dos filtros, donde primero se realiza un filtro con la fecha para luego aplicar otro filtro, utilizando "&", que serían los bytes igual a 100000.

![filtros1](/imagenes/filtros1.png)

En la siguiente ruta se aplica un único filtro, luego de digitar el valor de búsqueda se coloca un signo de interrogación(?), para indicar que lo que sigue son parámetros, en el ejemplo se observa que es únicamente uno y es de lenguaje(leng) cuando es "English"

![filtro1](/imagenes/filtro1.png)

**Valores de filtro**

En este apartado se logra observar los valores utilizados para realizar los filtros, los valores que se encuentran de color morado entre paréntesis, son los que se colocan en el request para indicar el valor que será filtrado. Los filtros son los siguientes:

* **leng:** Filtro de tipo lenguaje(SiteLanguaje).
* **fecha:** Filtro segun la fecha(PageLastModified).
* **bytes:** Filtro segun cantidad de bytes(PageBytes).
* **nLink:** Filtro segun cantidad de links(PageNumberLinks).
* **nameSpace:** Filtro de namespaces(PageNamespaces).
* **restriction:** Filtro segun la restriccion(PageRestriction).
* **infoName:** Filtro segun infoName(SiteInfoName).
* **infodbName:** Filtro segun infodbName(SiteInfoDBName).
* **pageredirect:** Filtro segun redirect(PageRedirect).

![valoresfiltro](/imagenes/valoresfiltro.png)

**Mapping**

En el siguiente apartado se explica el proceso de índice de Mongo, para este proyecto se realizó de la siguiente forma, en cada espacios se definen dos tipos, primero de tipo facet, por ejemplo de tipo numérico, como page bytes y page links, también se tiene los tipo string, como page last modified user, name sapce, page redirect, page restriction y page lenguaje, para fianlizar estan los tipo date, que el único seria last modified, por último los tipo "number" y "date", que funcionan para realizar filtrado. Para los tipos de texto se utilizó "lucene.simple" para realizar comparaciones en casos de minúsculas y mayúsculas.


![mapping1](/imagenes/mapping1.png)

![mapping2](/imagenes/mapping2.png)

## **Pruebas realizadas**

Las siguientes pruebas fueron realizadas para mostrar el funcionamiento del Loader y el funcionamiento de las bases de datos propuestas para el presente proyecto.

A continuación, se presentan los archivos que se encuentran en el Object Storage, serian dos XML largos, un XML normal y un TXT largo.

![loader10](/imagenes/loader10.png)

Ejecución del código con la sección de Autonomous comentada para mostrar el funcionamiento de la base de datos de Mongo.

![loader11](/imagenes/loader11.png)

Pruebas de Mongo recibiendo datos.

![loader12](/imagenes/loader12.png)

![loader13](/imagenes/loader13.png)

Ejecución del código con la sección de Mongo comentada para mostrar el funcionamiento en la base de datos de Autonomous.

![loader14](/imagenes/loader14.png)

Demostración de los datos en funcionamiento en la base de datos de Autonomous.

Para iniciar se muestra que las tablas se encuentran sin datos.

![loader15](/imagenes/loader15.png)

En la siguiente imagen se presenta la base de datos de Autonomous con los datos de prueba.

![loader16](/imagenes/loader16.png)

## **Pruebas unitarias**

En la siguiente imagen se presenta el código realizado en el archivo **"test.py"**, donde se realizan las pruebas unitarias de las APIs, en la primera prueba con la API de Mongo, se verifica que el código de envió sea el 200, además cuando se realiza el request, se verifica el contenido del documento y que el n sea diferente de 0. Con la prueba unitaria con la API de Autonomous Database, se realiza de igual forma una verificación en el contenido, de igual manera que n sea diferente de 0.

![prueba1](/imagenes/prueba1.png)

A continuación se presenta como se realizó la subida de la base de datos, se coloca terraform init, para luego ubicarse en la carpeta de templates y modificar el archivo el archivo llamado "vm01.sh" para modificar las imágenes, en este caso se coloca la imagen del repositorio de la API, para exportar del puerto 5000 al 80 que sería el puerto con el que se comunica con la máquina virtual.

![prueba2](/imagenes/prueba2.png)

![prueba3](/imagenes/prueba3.png)

## **Endpoints de Mongo Atlas**

<ins>**Funcionamiento de API Mongo**</ins>

Para comenzar se menciona que toda la API posee el mismo endpoint, iniciando con **"http"** y  la **"IP"**, luego se coloca el nombre de la función, que en este caso se le llamó **"BuscaGene"**, seguidamente el nombre del valor de búsqueda, que para este caso de prueba se utilizó "anarchism". Al procesar lo mencionado, se retorna todos los valores que coincidan con el valor de búsqueda, los valores que se obtienen son los siguientes, los documentos que coinciden, iniciando con el "page_id", "page_title" y por último los highlight, que lo que realizan es mostrar una lista con partes del texto, y donde aparezca hit es donde el valor enviando el inicio que en este caso es "anarchism" aparece. Ahora se presentan los facets, que muestra todas las categorías, los cuales fueron incluidos en el mapping.


![foto1](/imagenes/foto1.png)

## **Recomendaciones y conclusiones**

* En el área de Mongo, una de las principales características es que posee un esquema mas muy flexible, permitiendo que, en el caso de la existencia de datos no existentes, no genera problemas en la búsqueda o generar lógica adicional para evitar esos inconvenientes.
* La dificultad de inserción se ve disminuida por el modelo de documentos utilizados en Mongo, que se podría decir que es muy intuitivo.
* La agregación definida por Mongo, como las operaciones, highlights, facets, consultas y el funcionamiento de algunas aplicaciones que utilizan APIs, para la comunicación con la base de datos. 
* En el apartado de Autonomous database, con el tema de modelaje e implementación en comparación con Mongo, se vuelve un sistema un poco tosco de manejar, para realizar las pruebas ya sean de inserción o consulta, en consulta si se hace énfasis debido a la gran cantidad de métodos que se debían realizar, de igual forma apreciando el funcionamiento de los facets en Mongo en comparación a los de Autonomous si es un poco sencillo al utilizar métodos como "Group by" o "Count", pero a nuestro punto de vista si es un poco desactualizado, viendo la forma que se realizan en otros sistemas.  
* Como recomendación para Mongo seria realizar búsquedas de  operaciones que se pueden realizar, como la agregación o la consulta, ya que hay otros metodos que permiten filtrar de una mejor manera la información, no se pudo abarcar todos y pudieron haber sido de gran utilidad en el futuro.
* Otra recomendación seria que se podrían implementar otros métodos para realizar métricas con la aplicación, como lo fueron "count" o "history", que no fueron implementadas y pudieron permitir obtener otro tipo de métricas.
* Para el filtrado realizado desde las APIs, se debería identificar otro método para definir los valores de filtrado más eficientes y de una manera más dinámica.
* Como conclusion para el apartado de Autonomous en comparacion con Mongo se presentaron mas diferencias, tomando en cuenta la complejidad del codigo, al implementar en Python el lenguaje SQL, ya sea para creación de tablas e insersiones de datos.
* Al trabajar con una base de datos SQL como Autonomous, al momento de implementar inserciones se deben de tomar muchos temas en cuenta, por ejemplo relaciones y orden de insercion, en comparacion con Mongo que es unicamente la creacion de un diccionario, se presenta mas flexibilidad por parte de Mongo, tomando en cuenta que no posee un schema como lo tiene las bases de datos relacionales. 
* Con respecto de la base de datos Autonomous, una de las dificultades que presenta y que genera un poco de incomodidades es al momento de correr "terraform apply", habia qe ingresar constantemente a Oracle para realizar modificaciones en la seccion de Network en la base creada.

## Anexos

A continuación se presentan los modelos realizados para el entendimiento de las tablas diseñadas para la base de datos de Autonomous.

**Modelo Conceptual**

![modeloConceptual](/imagenes/modeloConceptual.drawio.png)

**Modelo Logico**

![modeloConceptual](/imagenes/modeloLogico.drawio.png)

## **Referencias**

Material consultada:

* https://python-oracledb.readthedocs.io/en/latest/api_manual/module.html

* https://www.youtube.com/watch?v=5WfolTP_QRA&ab_channel=OracleMania
