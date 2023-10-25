# **Base de Datos II (IC4302)** – Semestre 2, 2023
### **Tarea Corta #1** 
### Jesús Andrés Cortés Álvarez  – 2021579439
### Aaron Ortiz Jimenez  – 2022437529
### Joctan Antonio Porras Esquivel - 2021069671
### Justin Acuña Barrantes  - 2018093451
### David Suárez Acosta – 2020038304

---

## Instrucciones de funcionamiento

* **Base de datos Neo4j**
* 
  Para realizar el script de Neo4j es necesario subir la base de datos, en este caso para visualizar su funcionamiento se deberá de ingresar a la carpeta llamada databases, seleccionar el archivo "values.yaml", seguidamente al entrar el archivo el apartado de enabled debe ser cambiado a "true" en el caso de que se encuentre en "false", si alguna de las otra bases de datos se encuentra en "true", se recomienda cambiar a al valor "false", esto para evitar que las de demás bases de datos se ejecuten en simultaneo.

  ![Alt text](neo1.png)

  Luego deberá de dirigirse a la carpeta llamada "backups", ingresar al archivo "values.yaml", al ingresar al archivo se presentan dos opciones en el apartado de Neo4j, si desea realizar un "backup" en el espacio de enabled lo coloca en true, o en el caso de querer realizar  un "restore", de la misma forma se coloca "true", en el espacio de enabled.


  A continuación, se presenta una imagen de ejemplo de lo anteriormente dicho.

   ![Alt text](neo2.png)

* **Base de datos ElasticSearch**




## Pruebas realizadas

* **Base de datos Neo4j**

    A continuación, se presenta como se realizan las pruebas correspondientes para la base de datos de Neo4j.

    ![Alt text](image1.png)

    Se logra observar el resultado del primer script, que obtiene los datos desde el bucket s3 hacia la maquina en la que se está trabajando.

    ![Alt text](image2.png)

    En la imagen anterior se muestra el proceso para realizar el restore, donde se muestra el archivo que se obtuvo de aws y se crea la base de datos.


  

* **Base de datos ElasticSearch**

    En las siguientes imágenes se presenta como dirigirse a la sección de snapshot, primero se debe de dirigir al cuadro de "menú" y luego se dirige al espacio de "Stack Managment".
    
    ![Alt text](elas1.png)

    Al dar clic se le presentará el siguiente menú, donde deberá de dirigirse al apartado de "Snapshot and Restore".

    ![Alt text](elas2.png)

    Seguidamente se presentan imágenes correspondientes a la creación del repositorio, en este caso para la creación se pone de nombre el carnet estudiantil, el servicio seria "aws s3". Para la siguiente imagen, se define el cliente como default, el bucket que fue el asignado y se logra apreciar en la imagen, al finalizar se preciosa el botón de registrar.

    ![Alt text](elas5.png)

    ![Alt text](elas3.png)

    ![Alt text](elas4.png)

    Para la creación del snapshot, se debe ir al apartado de "Create Policy", se le coloca un nombre, el nombre del snapshot, se asignan las configuraciones que va a tener el snapshot, politicas de retención y la duración, para finalizar se presiona el botón de "Create Policy"

    ![Alt text](image.png)

    En la siguiente imagen se observa que ya fue creado el policy, seguidamente se presiona el botón ubicado al lado derecho para correrlo, y ya realizaria el backup, Al finalizar ya aparecerían los snapshots.

    ![Alt text](image-1.png)

    En el apartado del restore, se coloca el indice ...
    

## Recomendaciones

## Conclusiones
