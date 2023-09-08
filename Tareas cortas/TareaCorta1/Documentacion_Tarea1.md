# **Base de Datos II (IC4302)** – Semestre 2, 2023
### **Tarea Corta #1** 
### Jesús Andrés Cortés Álvarez  – 2021579439
### Aaron Ortiz Jimenez  – 2022437529
### Naomi Ilama Gamboa – 2021114064
### Alexander Brenes Garita – 2018191805
### David Suárez Acosta – 2020038304

---

## **Guía de instalación y uso de la tarea**

asdf


## **Configuración de las herramientas**

*Helm Charts*

asdf

*Aplicación Intermediaria (Flask y Prometheus)*

asdf

*Grafana*

asdf

## Gatling

En este apartado se explicará la instalación de Gatling y otros aspectos importantes para su utilización.
Para comenzar visitaremos el sitio oficial de gatling(https://gatling.io/open-source/) para instalar lo necesario; Se debe instalar la versión open source y dar click el siguiente botón para comenzar la descarga.

![gatling](/imagenes/gatling.jpg)

Luego de haberse descargado, en su apartado de descargas aparecerá este archivo .zip, el cual en su disco local, debe crear una carpeta llamada gatling y ahí deberá descomprimir todos los archivos.

![descarga](/imagenes/descarga.jpg)
![carpeta](/imagenes/carpeta.jpg)

Para Gatling es necesario tener instalado el JDK de Java, para esto es necesario tener la versión 17 instalada, en el siguiente link podrá descargar el JDK(https://www.oracle.com/uk/java/technologies/downloads/), a continuación se presenta una imagen del sitio web de oracle donde debe descargar la versión correspondiente para su computadora.

![java](/imagenes/java.jpg)

Para finalizar es necesario tener instalado en su computadora la herramienta de compilación maven, la cual la puede descargar en el siguiente link(https://maven.apache.org/download.cgi).

![maven](/imagenes/maven.jpg)

Luego de tener lo necesario instalado, se presenta la estructura que toma Gatling para poder ejecutar las pruebas. Se mostrará la estructura utilizada para ejecutar las pruebas en Gatling.
En este trabajo se utilizó un archivo Java para desarrollar el código necesario para ejecutar las pruebas en Gatling.
Para comenzar se importan las dependencias necesarias para Gatling, que son las siguientes:

![maven](/imagenes/dependencias.jpg)

Estas importaciones son muy importantes para acceder a clases y métodos que posee Gatling, para poder realizar las pruebas de carga. Además el import http nos beneficia para poder realizar las pruebas mediante HTTP en Gatling, estas clases permiten realizar solicitudes  HTTP y además recibir las respuestas HTTP. 

Para cumplir con la carga de datos, se realizaron diferentes métodos, que utilizan verbos los cuales nos facilitan las pruebas, además Gatling nos brinda la clase **ChainBuilder** la cual ayuda a definir una serie de acciones, los métodos son los siguientes:

* **crearRegistro:** Con este método invocamos el json mediante un feeder para alimentar con datos, luego definimos la solicitud HTTP con el nombre dinámico, para luego luego utilizar el verbo **“.post”**, que lo que realiza es una solicitud HTTP POST al url  “/crear”. Para finalizar mediante “.body”, se configura el cuerpo de la solicitud, utilizando el template diseñado para la carga de datos.



* **borrarRegistro:** Este método utilizando el verbo **".delete"**, el cual coloca un nombre dinámico, para luego mediante  una solicitud HTTP realiza el delete a la URL “/borrar/”, seguidamente con el nombre del registro que se desea eliminar.

* **actualizarRegistro:** Este método tiene similitudes con el primer método mencionado, pero en este caso con el verbo **“.put”**, se realiza una nueva solicitud HTTP PUT al URL “/actualizar/”, también con el nombre del registro que se desea actualizar, para luego gracias al método “.body” se configura el cuerpo de la solicitud HHTP PUT, de igual forma con el template definido. para luego configurarlo de tipo JSON con el método “asJson”.

* **busquedaRegistro:** Este método utiliza el verbo **“.get”**, con la finalidad de  realizar una solicitud HTTP GET al URL “/buscar/”, en este caso se utiliza el id para realizar la búsqueda del dato. Posteriormente se emplea el método “.check”, la cual hace una verificación de la solicitud, este método utiliza el lenguaje de consulta JSON JMESPath, esto para extraer el valor del campo que se definió en la función llamado “name”.

Luego de todos los métodos se utiliza una función la cual se llama scenario, esta función utiliza la clase **ScenarioBuilder**, la misma es muy importante para Gatling, ya que nos ayuda definir el escenario donde se ejecutarán los métodos ya definidos y realizar exitosamente las pruebas de carga.


## **Pruebas de carga realizadas**

asdf


## **Conclusiones y recomendaciones**

asdf


