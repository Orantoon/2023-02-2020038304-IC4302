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

<ins>**IMPORTANTE**</ins>

Es necesario instalar unas dependencias para que funcione las imagenes de flask para las bases de datos, todas tienen que estar instalado en cmd powershell

```sh
pip install psycopg2-binary Flask-SQLAlchemy
```
```sh
pip install flask
```
```sh
pip install elasticsearch
```
```sh
pip install prometheus_client
```
```sh
pip install werkzeug
```
```sh
pip install mysql-connector-python
```
```sh
pip install flask_sqlalchemy
```
```sh
pip install sqlalchemy
```

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

* **Pruebas en Mongo DB**
  
En esta primera prueba se usaron 1000 usuarios en 15 segundos de interacción, en el siguiente grafico se puede visualizar el CPU Process, que llega como hasta 3, se logran ver los picos de procesamientos, en el último se visualizan los 1000 usuarios, luego en el segundo grafico se logra ver los query operations y se pueden observar las pruebas de delete, insert, update y search. En el tercer grafico se logra observar el tiempo de ejecución, las conexiones disponibles y las conexiones abiertas que fueron 7.74. En la parte inferior se logra ver la memoria y básicamente se visualiza como se utiliza más la memoria virtual que usa 2.5GB.

![Mongo](/imagenes/mongo 1.jpg)

En esta segunda prueba se trabaja con 2000 usuarios y 15 segundos de respuesta, en el primer grafico se visualiza el CPU Process que llega a niveles de 2, en el apartado de query operations se hacen 60 operaciones por segundo, como lo son los delete, insert, update y search.

En el apartado de operaciones se lleva una hora y cuarenta y tres minutos, se repiten las conexiones disponibles y las operaciones abiertas son de 9 y la memoria virtual 2.57GB.

![Mongo1](/imagenes/mongo2.jpg)

![Mongo2](/imagenes/mongo3.jpg)


En las siguientes pruebas se trabaja con 3000 usuarios, se sigue el mismo rango del CPU que es de 2, en el apartado de operaciones llega a 80 operaciones por segundo con las pruebas de delete, insert, update y search. En el apartado de conexiones sigue en una hora cincuenta tres minutos, hay 838851 conexiones disponibles y 9 operaciones abiertas. Y la memoria no tuvo mucho cambio se mantiene en 2.57GB.

![Mongo1](/imagenes/mongo4.jpg)

![Mongo2](/imagenes/mongo5.jpg)


Las pruebas siguientes se trabaja con 5000 usuarios en 15 segundos, no se presenta problemas, con las métricas del CPU con una medida de 5, en el apartado de query operations, ya se llega a las 125 operaciones por segundo, se logra ver como en este caso todas las operaciones se mantienen y se ve como baja con la velocidad de las operaciones.

Con las conexiones se lleva una hora 60 minutos de las métricas, se tiene 838849 conexiones disponibles y 10.9 conexiones abiertas, ahora se puede observar como en la memoria virtual hubo un aumento a 20MB.

![Mongo1](/imagenes/mongo6.jpg)

![Mongo2](/imagenes/mongo7.jpg)


Ahora las pruebas se realizan con 10 000 usuarios en 15 segundos, en el primer grafico se trabajó con Gatling, con Gatling se logran visualizar algunos problemas de conexiones, casi después de un minuto empiezan a haber problemas, y se observa cómo va bajando la velocidad de respuesta de los request y se ve muy lento, en la curva amarilla se logran ver los request que se están pidiendo y en la parte inferior la zona verde son lo que si se han logrado responder.

![Mongo1](/imagenes/mongo8.jpg)

Ahora se logra ver en el CPU hay un nivel de 9 de procesamiento, nos enfocamos en la parte de query operations se visualiza que algunas operaciones ya les cuesta, los inserts no tuvieorn problemas, como también los de búsqueda, los inserta tuvieron un mejor rendimiento, pero los demás si comenzaron a decaer tomando en cuenta que ya había búsqueda de por medio. En las métricas se tuvo 1,77 horas de trabajos, tiene 838836 conexiones disponibles y 24.3 conexiones abiertas. La memoria ya pasó de 2.57GB a 2.67GB, ahora se nota más el incremento.

![Mongo2](/imagenes/mongo9.jpg)

Luego de trabajar con 10 000 usuarios no se podía seguir, por lo tanto, se realizó un reinicio.
Los inserts siguieron teniendo buen rendimiento, pero siguen un poco lentas en comparación con las pruebas anteriores, completar los querys si lleva mucho tiempo.

![Mongo2](/imagenes/mongo10.jpg)

En la siguiente imagen, el grafico de query operations, hubo altos picos de inserción, la parte de actualización, de borrado y búsqueda si se genera un poco más de dificultad para realizarlas. La memoria virtual lleva ya 2.61GB.

![Mongo2](/imagenes/mongo11.jpg)

![Mongo2](/imagenes/mongo12.jpg)

---
* **Pruebas en Elasticsearch**

Para comenzar se están trabajando con 1000 usuario en 15 segundos, ahora se puede visualizar el CPU percent, el primer pico seria cuando se inicializa en elasticsearch. Ahora podemos visualizar los nodos que sería solo 1, los data nodos también son 1, se tienen 656 File Descriptors, el cluster health está en 23.

![Mongo2](/imagenes/elastic1.jpg)

En la siguiente imagen se tiene el CPU memory, donde la memoria usada se ven unos pequeños picos.

![Mongo2](/imagenes/elastic2.jpg)

En esta imagen se presentan los documentos y se logra visualizar como aumentan la cantidad de nodos con documentos, y en los documentos indexados hay un pico muy grande, similar al de borrado.

![Mongo2](/imagenes/elastic3.jpg)

Par las siguientes pruebas se tienen 2000 usuarios en 15 segundos, el CPU percent está llegando a 20%, el cluster healt está en 23, los open file descriptors se tienen 652, también se tienen 12 active primary shards, de igual forma 12 active shards.

![Mongo2](/imagenes/elastic4.jpg)

En los documentos eliminados se pudo ver muy poco incremento y documentos unidos se logra ver más altos que los anteriores.  

![Mongo2](/imagenes/elastic5.jpg)

En la siguiente imagen se logra observar un pico muy grande

![Mongo2](/imagenes/elastic6.jpg)


En las siguientes pruebas se trabajó con 3000 usuarios en 15 segundos. Se puede destacar que ahora se presentaron algunos problemas para procesar los request, el porcentaje del CPU se encuentra en 20%, el cluster healt se mantiene comparándolo con el anterior, los file descriptors ya se encuentran en 660, la memoria se encuentra en un 76.2%.

![Mongo2](/imagenes/elastic7.jpg)

En la siguiente imagen se logra observar el porcentaje de carga que se mantiene. 

![Mongo2](/imagenes/elastic8.jpg)

En la siguiente imagen que sería el apartado de documentos, el contador de documentos en nodos aumentó a 4000, en los indexados se llegó a 600.

![Mongo2](/imagenes/elastic9.jpg)

![Mongo2](/imagenes/elastic10.jpg)

En el siguiente grafico de Gatling presentó problemas, debido a que al principio funcionaba todo bien, pero a cierta cantidad de usuarios, comenzó a disminuir la velocidad de respuesta del servidor, y llega a niveles muy bajos, adicionando que la respuesta es demasiado lenta, cuando se trabaja con 3000 usuarios.

![Mongo2](/imagenes/elastic11.jpg)

En la siguiente prueba se realizó un cambio muy grande con las métricas, tomando en cuenta que se trabajó de nuevo con 3000 usuarios, pero se agregó más el tiempo de respuesta a un minuto, para lograr visualizar algún aumento, el margen de error se mantuvo, las respuestas seguían un poco lentas, pero en ciertos momentos si hay un pico positivo y puede responder a algunas, dos minutos después se pudo ver una respuesta más rápida. A pesar de que se tuvo que reiniciar trabó de buena forma tomando en cuenta que se le agregó más tiempo.

![Mongo2](/imagenes/elastic12.jpg)

![Mongo2](/imagenes/elastic13.jpg)


Para estas últimas pruebas se trabajó con 4000 usuarios y de igual forma con un minuto de tiempo, estas pruebas se realizaron debido a que con 3000 usuarios hubieron fallas, se queria ver el comportamiento con 4000 usuarios.

Como se logra ver en la primera imagen, el porcentaje del CPU es 20, el cluster healt se mantiene en 23, el uso de memoria es de un 65.3%, hay 641 file descriptors.

![Mongo2](/imagenes/elastic14.jpg)

El uso de memoria como se visualiza en esta imagen es muy importante, no tuvo mucho incremento.

![Mongo2](/imagenes/elastic15.jpg)

![Mongo2](/imagenes/elastic16.jpg)

En este apartado en comparación a los anteriores, como se tuvo que realizar un reincido se logra ver varias diferencias, el contador de documentos por nodo va por 3000, y documentos indexados se llevan 60, y documentos eliminados 92.

![Mongo2](/imagenes/elastic17.jpg)

En este grafico de Gatling, se deseaba observar como respondía con 4000 usuarios, y no es tan constante, hay más picos en comparación con los 3000 usuarios. La cantidad de los request no se mantenía.

![Mongo2](/imagenes/elastic18.jpg)


* **Pruebas en MariaDB**
Las pruebas de MariaDB no pudieron ejecutadas por problemas de conexion, el codigo de MariaDB funciona al igual que la implementacion con flask, tambien esta configurado el template y la conexion con values estan. Al igual las pruebas internas con postman funcionan pero dieron error las pruebas externas con gaitlin no se pudo hacer la conexion aunque el puerto de la base de datos estaba activado no se pudo conectar. Fue el unico error que se tuvo.



* **Pruebas en MariaDB Galera**
Las pruebas en MariaDB Galera no se pudieron llevar a cabo debido a dificultades de conectividad. El código de MariaDB Galera se encuentra en perfecto estado y se comporta de manera similar a la implementación con Flask. La plantilla está configurada adecuadamente, al igual que la conexión con los valores necesarios. Las pruebas internas con Postman se ejecutaron con éxito; sin embargo, nos encontramos con un desafío al intentar realizar pruebas externas con Gatling, ya que no logramos establecer la conexión, a pesar de tener el puerto de la base de datos activado. Este problema de conectividad fue el único obstáculo que enfrentamos.


* **Pruebas en PostgreSQL**
No se lograron realizar las pruebas en PostgreSQL debido a problemas de conectividad. A pesar de que el código de PostgreSQL funcionaba de manera adecuada, al igual que la implementación con Flask, y la configuración de la plantilla y la conexión con los valores estaban en orden, nos encontramos con dificultades al intentar ejecutar pruebas externas con Gatling. A pesar de que el puerto de la base de datos estaba activado, no pudimos establecer la conexión. Este inconveniente de conectividad fue el único obstáculo que enfrentamos.



* **Pruebas en PostgreSQL HA**
No fué posible llevar a cabo las pruebas en PostgreSQL HA debido a problemas de conectividad que surgieron durante el proceso. El código de PostgreSQL HA se encuentra en excelentes condiciones y se comporta de manera consistente con la implementación en Flask. La plantilla está configurada de forma adecuada, al igual que la conexión con los valores necesarios. A pesar de que las pruebas internas con Postman se completaron satisfactoriamente, nos encontramos con dificultades al intentar realizar pruebas externas con Gatling. A pesar de tener el puerto de la base de datos activado, lamentablemente, no pudimos establecer la conexión. Este problema de conectividad fue el único desafío que enfrentamos durante el proceso de prueba en PostgreSQL HA

## **Conclusiones y recomendaciones**


### * Conclusiones

El proyecto de implementación de monitoreo y pruebas de carga de bases de datos utilizando Helm Charts, Gatling y herramientas como Prometheus, Grafana y Elasticsearch proporciona una valiosa experiencia en la configuración, monitoreo y evaluación del rendimiento de sistemas y bases de datos en entornos de Kubernetes. A partir de las pruebas realizadas en bases de datos MongoDB y Elasticsearch, se pueden extraer varias conclusiones:

### MongoDB:

1. **Escalabilidad y Rendimiento**: MongoDB demostró ser altamente escalable y tolerante a cargas de trabajo crecientes. Pudo manejar con éxito un aumento significativo en el número de usuarios concurrentes, lo que indica su capacidad para admitir aplicaciones con alta demanda de lectura y escritura.

2. **Recursos del Sistema**: El monitoreo de recursos como el uso de CPU, memoria y conexiones fue esencial. A medida que aumentaba la carga de trabajo, el consumo de recursos también aumentaba. Esto sugiere que se deben asignar recursos adecuados para garantizar un rendimiento óptimo.

3. **Velocidad de Respuesta**: A medida que se incrementaba la carga, se observó un aumento en el tiempo de respuesta, lo que indica que es fundamental dimensionar y optimizar la base de datos para mantener tiempos de respuesta aceptables bajo cargas elevadas.

### Elasticsearch:

1. **Escalabilidad y Rendimiento**: Elasticsearch mostró una buena escalabilidad y capacidad para manejar consultas y búsquedas en un índice de datos. Sin embargo, se notó que el aumento de la carga de trabajo podía afectar negativamente el rendimiento de las consultas.

2. **Recursos del Sistema**: Similar a MongoDB, el monitoreo de recursos fue fundamental para detectar problemas potenciales. El uso de CPU y memoria se incrementó con cargas más pesadas, lo que sugiere que se deben asignar recursos suficientes.

3. **Tiempo de Respuesta**: Al igual que MongoDB, Elasticsearch experimentó un aumento en el tiempo de respuesta bajo cargas pesadas. Esto destaca la importancia de optimizar las consultas y ajustar la configuración para lograr un rendimiento estable.

### MariaDB, MariaDB Galera, PostgreSQL Y PostgreSQL HA:
Base de datos interesantes pero un rendimientos rapido con su alta disponivilida como PostgreSQL y como funciona el SQL con tablas y el sistema CRUD pero por problemas de conexion no pudimos ver su poder total. La recomedacion es trabajar e investigar mas como trabajar flask con base de datos SQL para hacer la conexion.



### * Recomendaciones

Para proyectos similares de implementación de monitoreo y pruebas de carga en bases de datos y sistemas Kubernetes, se pueden considerar las siguientes recomendaciones:

1. **Planificación de Recursos**: Realizar un análisis detallado de los requisitos de recursos de sus aplicaciones y bases de datos. Asigne suficiente CPU, memoria y almacenamiento para evitar problemas de rendimiento.

2. **Optimización de Consultas**: Optimizar las consultas y búsquedas en las bases de datos para reducir el tiempo de respuesta. Utilice índices eficientes y ajuste la estructura de datos según sea necesario.

3. **Escalabilidad Horizontal**: Considerar la posibilidad de utilizar la escalabilidad horizontal para distribuir la carga de trabajo entre múltiples instancias de bases de datos o nodos. Esto puede mejorar la capacidad de respuesta y la tolerancia a fallos.

4. **Monitoreo Continuo**: Implementar un sistema de monitoreo continuo utilizando herramientas como Prometheus y Grafana para supervisar el rendimiento de sus sistemas en tiempo real. Configure alertas para detectar problemas rápidamente.

5. **Pruebas de Carga Graduales**: Realizar pruebas de carga gradualmente incrementando el número de usuarios concurrentes. Esto le permitirá identificar el punto de quiebre donde se alcanza la capacidad máxima de sus sistemas.

6. **Gestión de Errores**: Implementar una estrategia sólida de gestión de errores y recuperación. Las bases de datos y las aplicaciones deben manejar de manera adecuada los errores para evitar la degradación del servicio.

7. **Documentación Detallada**: Manter una documentación completa de la configuración, los resultados de las pruebas de carga y las lecciones aprendidas. Esto facilitará la resolución de problemas futuros y la toma de decisiones informadas.

8. **Exploración de Alternativas**: Considerar explorar otras bases de datos NoSQL y herramientas de monitoreo según las necesidades específicas de su proyecto. Cada tecnología tiene sus propias fortalezas y debilidades.



## **Bibliografía**

- Video para la plantilla  y explicación de Gatling: https://www.youtube.com/watch?v=NzqO6AOKjeg&t=574s
