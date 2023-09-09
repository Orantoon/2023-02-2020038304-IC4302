# **Base de Datos II (IC4302)** – Semestre 2, 2023
### **Tarea Corta #1** 
### Jesús Andrés Cortés Álvarez  – 2021579439
### Aaron Ortiz Jimenez  – 2022437529
### Naomi Ilama Gamboa – 2021114064
### Alexander Brenes Garita – 2018191805
### David Suárez Acosta – 2020038304

---

## **Guía de instalación y uso de la tarea**

<ins>**Helm Charts**</ins>

1. Desde una terminal, se entra a la carpeta *charts/bootstrap* y se corre el comando **helm dependency update** para descargar las dependencias para el helm.

2. Se corre el comando **cd ..** para volver a la carpeta *charts* y se corre el comando **helm install bootstrap bootstrap** para crear el Helm encargado de los namespaces llamado "bootstrap".

3. Se entra a la carpeta *charts/monitoring-stack* con el comando **cd monitoring-stack** y se corre el comando **helm dependency update** para descargar las dependencias para el helm.

4. Se corre el comando **cd ..** para volver a la carpeta *charts* y se corre el comando **helm install monitoring-stack monitoring-stack** para crear el Helm encargado de las herramientas Grafana y Prometheus llamado "monitoring-stack".

5. Se entra a la carpeta *charts/databases* con el comando **cd databases** y se corre el comando **helm dependency update** para descargar las dependencias para el helm.

6. Antes de continuar, tenemos que editar el archivo *databases/values.yaml* y deshabilitar todas las bases que no se van a utilizar (**enabled: false**) y solo habilitar las que se van a analizar (**enabled: true**). Por ejemplo:

![Databases Values](/imagenes/databases_values.jpg)

7. Se corre el comando **cd ..** para volver a la carpeta *charts* y se corre el comando **helm upgrade --install databases databases** para crear el Helm encargado de las bases de datos habilitadas llamado "databases".

8. Ahora hay que editar el archivo *grafana-config/values.yaml* y deshabilitar todos los dashboards que no se van a visualizar (**enabled: false**) y solo habilitar los que se quieren ver (**enabled: true**). Por ejemplo:

![Grafana Values](/imagenes/grafana_values.jpg)

9. En la carpeta *charts* se corre el comando **helm install grafana-config grafana-config** para crear el Helm encargado de la configuración de Grafana llamado "grafana-config".

10. Se edita el archivo *flask/stateless/values.yaml* afuera de la carpeta *charts* y deshabilitar uno del los dos valores *flaskes* y *flaskmg* (**enabled: false**) y habilitar el otro (**enabled: true**). Por ejemplo:

![Stateless Values](/imagenes/stateless_values.jpg)

11. En la carpeta *flask* se corre el comando **helm install stateless stateless** para crear el Helm encargado de descargar Flask llamado "stateless".

## **Configuración de las herramientas**

<ins>**Helm Charts**</ins>

Se utilizaron cinco Helm Charts para el desarrollo del proyecto:

- **Bootstrap**: crea los namespaces e instalación de los operadores.
- **Databases**: contiene las bases de datos que se van a analizar, estas son MariaDB, MongoDB, Elasticsearch, PostgreSQL, MariaDB Galera y PostgreSQL HA. Para esto se modificaron los archivos "Chart.yaml"

![Databases](/imagenes/databases_chart.jpg)

y "values.yaml" (es muy grande para adjuntar una imagen).

- **Grafana-config**: carga dinámicamente los Dashboards y Datasources.
- **Monitoring-stack**: contiene las herramientas Prometheus, Grafana y Thanos, de los cuales se utilizan Prometheus y Grafana.
- **Stateless**: se encuentra en la carpeta "flask" y permite el uso de Flask para el funcionamiento de la aplicación intermediaria.

<ins>**Aplicación Intermediaria (Flask y Prometheus)**</ins>

Para la aplicación intermediaria se creó la carpeta "flask" la cual contiene un Helm Chart llamado "stateless" el cual contiene la herramienta Flask que se utilizó para exponer métricas con Prometheus donde se utiliza un servicio tipo "ClusterIP".

---

<ins>**Grafana**</ins>

asdf

<ins>**Gatling**</ins>

**Instalación**

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

![imports](/imagenes/dependencias.jpg)

Estas importaciones son muy importantes para acceder a clases y métodos que posee Gatling, para poder realizar las pruebas de carga. Además el import http nos beneficia para poder realizar las pruebas mediante HTTP en Gatling, estas clases permiten realizar solicitudes  HTTP y además recibir las respuestas HTTP. 

<ins>**Configuración**</ins>

Para cumplir con la carga de datos, se utilizó la plantilla del video "GatlingCrashCourse" (se encuentra en la bibliografía) el cual explica como realizar Stress Tests sobre un API. En la capeta "plantilla gatling" se encuentra la plantilla, en la cual se creó el archivo principal **pruebas/pruebas.java** para realizar las pruebas que se necesitan para este trabajo y se crearon nuevos archivos JSON con datos de prueba del API de Pokemon (*data/gameJsonFile.json*) que usaremos para llenar las bases de datos, pero debido al tamaño de los datos se modificó, creandose el archivo **data/content.json** que se utiliza como los datos de prueba para las bases de datos y es una versión más simplificada de los datos del API Pokemon. Por último, se creó el archivo **bodies/newGameTemplate.json** que contiene la plantilla de los datos que van a insertarse en la base de datos, es decir una plantilla para un archivo de *content.json*.

En **pruebas/pruebas.java** se conecta primero con nuestra aplicación intermediaria con el método *httpProtocol*, se configuran los parametros de usuarios y tiempo para la realización de las pruebas y se extraen los datos de los JSON **data/content.json** y **bodies/newGameTemplate.json** para el funcionamiento de los diferentes tipos de pruebas.

Para los diferentes tipos de pruebas se realizaron diferentes métodos, que utilizan verbos, además Gatling nos brinda la clase *ChainBuilder* la cual ayuda a definir una serie de acciones. Los métodos son los siguientes:

* **crearRegistro:** Con este método invocamos el json mediante un feeder para alimentar con datos, luego definimos la solicitud HTTP con el nombre dinámico, para luego luego utilizar el verbo **“.post”**, que lo que realiza es una solicitud HTTP POST al url  “/crear”. Para finalizar mediante “.body”, se configura el cuerpo de la solicitud, utilizando el template diseñado para la carga de datos.

![Metodos](/imagenes/crear_registro.jpg)

* **borrarRegistro:** Este método utilizando el verbo **".delete"**, el cual coloca un nombre dinámico, para luego mediante  una solicitud HTTP realiza el delete a la URL “/borrar/”, seguidamente con el nombre del registro que se desea eliminar.

![Metodos](/imagenes/borrar_registro.jpg)

* **actualizarRegistro:** Este método tiene similitudes con el primer método mencionado, pero en este caso con el verbo **“.put”**, se realiza una nueva solicitud HTTP PUT al URL “/actualizar/”, también con el nombre del registro que se desea actualizar, para luego gracias al método “.body” se configura el cuerpo de la solicitud HHTP PUT, de igual forma con el template definido. para luego configurarlo de tipo JSON con el método “asJson”.

![Metodos](/imagenes/actualizar_registro.jpg)

* **busquedaRegistro:** Este método utiliza el verbo **“.get”**, con la finalidad de  realizar una solicitud HTTP GET al URL “/buscar/”, en este caso se utiliza el id para realizar la búsqueda del dato. Posteriormente se emplea el método “.check”, la cual hace una verificación de la solicitud, este método utiliza el lenguaje de consulta JSON JMESPath, esto para extraer el valor del campo que se definió en la función llamado “name”.

![Metodos](/imagenes/buscar_registro.jpg)

Luego de todos los métodos se utiliza una función la cual se llama *scenario*, esta función utiliza la clase **ScenarioBuilder**, la misma es muy importante para Gatling, ya que nos ayuda definir el escenario donde se ejecutarán los métodos ya definidos y realizar exitosamente las pruebas de carga. Finalmente hay un bloque de configuración para las pruebas donde se utilizan los parametros de usuario y tiempo de pruebas definidos anteriormente.

![Scenario](/imagenes/pruebas.jpg)


## **Pruebas de carga realizadas**

asdf


## **Conclusiones y recomendaciones**

asdf


## **Bibliografía**

- Video para la plantilla  y explicación de Gatling: https://www.youtube.com/watch?v=NzqO6AOKjeg&t=574s