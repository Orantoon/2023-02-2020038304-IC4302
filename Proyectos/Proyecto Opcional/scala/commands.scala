// - ABRIR SPARK -

cd "/mnt/d/Tareas David/TEC/Semestre 8/Bases de Datos II/Bases_2/Proyectos/Proyecto Opcional/Descargas/spark-2.4.8-bin-hadoop2.7/"
bin/spark-shell

// - IMPORTS -

import org.apache.spark.SparkContext
import org.apache.spark.SparkContext._
import org.apache.spark.SparkConf
import org.apache.spark.sql.SparkSession
import org.apache.spark.sql.SparkSession._
import org.elasticsearch.spark.sql
import org.elasticsearch.spark.sql._
import org.elasticsearch.spark._ 

// - MAPEAR IP EN ELASTICSEARCH -

// kubectl port-forward service/ic4302-es-http 9200:9200    // Activar en otra terminal

// - DESCARGAS -

//https://www.elastic.co/guide/en/elasticsearch/hadoop/current/spark.html
//https://archive.apache.org/dist/spark/spark-2.4.8/spark-2.4.8-bin-hadoop2.7.tgz
//https://artifacts.elastic.co/downloads/elasticsearch-hadoop/elasticsearch-hadoop-8.6.2.zip
// copy elasticsearch-hadoop-8.6.2.jar into spark-2.4.8-bin-hadoop2.7/jars/

// - BORRAR SESSION ANTERIOR -

sc.stop()
spark.stop()

// - CONFIGS -

val conf = new SparkConf()

conf.set("es.index.auto.create", "true")
conf.set("es.nodes", "http://localhost:9200/")
conf.set("es.net.http.auth.user", "elastic")
conf.set("es.net.http.auth.pass", "I3n5IE2pfkH08A5v97R4DH9J")   // Cambiar contraseña
conf.set("es.port", "9200")
conf.set("es.nodes.wan.only", "true")

// - NUEVA SESSION -

val sc = new SparkContext(conf)
val spark = SparkSession.builder.config(sc.getConf).getOrCreate()

// - SE CONFIGURA LA LECTURA QUE SE VA A HACER -

val sqlcontext = new org.apache.spark.sql.SQLContext(sc)    // Se crea un nuevo SQLContext
//val options = Map("es.read.field.as.array.include" -> "data")   // "data" se va a leer como array
//val df = sqlcontext.read.options(options).format("org.elasticsearch.spark.sql").load("messages")    // Se va a leer el indice "messages"
val df = sqlcontext.read.options(options).format("org.elasticsearch.spark.sql").load("augmented")    // Se va a leer el indice "augmented"
df.createOrReplaceTempView("es")    // Nombre temporal para la vista de "df"

// - QUERIES DE PRUEBA -

//spark.sql("SELECT col.hostname as hostname, col.msg as msg FROM (SELECT EXPLODE(data) FROM es)").show   // Consulta por las columnas "hostname" y "msg"; "show" muestra el resultado
//spark.sql("SELECT col.hostname as hostname, col.msg as msg FROM (SELECT EXPLODE(data) FROM es)").saveToEs("datos")  // Consulta por las columnas "hostname" y "msg"; se guarda en el indice "datos"



//val prueba1 = spark.sql("SELECT CONCAT_WS(', ', TRIM(SPLIT(col.hostname, ' ')[1]), TRIM(SPLIT(col.hostname, ' ')[0])) as hostname FROM (SELECT EXPLODE(data) FROM es)") // Esta prueba no funciona porque no hay nada separado por un ' '

//spark.sql("SELECT CONCAT_WS(', ', TRIM(SPLIT('David Suarez', ' ')[1]), TRIM(SPLIT('David Suarez', ' ')[0])) as author_name").show()
spark.sql("SELECT CONCAT_WS(', ', TRIM(SPLIT(col.author_name, ' ')[1]), TRIM(SPLIT(col.author_name, ' ')[0])) as author_name FROM es").show


//val prueba2 = spark.sql(s"SELECT id, ${newColumns} FROM (SELECT EXPLODE(data) FROM es) LATERAL VIEW OUTER EXPLODE(SPLIT(col.hostname, ' ')) AS exploded_element")
//prueba2.show()

spark.sql("SELECT map_from_arrays(keys, txt) AS txt, name, id FROM (SELECT sequence(1, size(split(txt, ','))) as keys, split(txt, ',') as txt, name, id FROM (SELECT \"hola, soy, Nereo\" as txt, \"Nereo\" as name, 56 as id))").withColumn("Fld1", $"txt".getItem("1")).show
spark.sql("SELECT map_from_arrays(keys, txt) AS txt, name, id FROM 
(SELECT sequence(1, size(split(txt, ','))) as keys, split(txt, ',') as txt, name, id FROM 
(SELECT \"hola, soy, Nereo\" as txt, \"Nereo\" as name, 56 as id))").withColumn("Fld1", $"txt".getItem("1")).show

spark.sql("SELECT SIZE(SPLIT(col.hostname, ', ')) as hostname FROM (SELECT EXPLODE(data) FROM es)").show

val prueba2 = spark.sql("SELECT col.hostname AS hostname FROM (SELECT EXPLODE(data) FROM es) PIVOT (NULL FOR hostname IN )")


//val prueba3 = spark.sql("SELECT INITCAP(TRIM(col.hostname)) as hostname FROM (SELECT EXPLODE(data) FROM es)")

//spark.sql("SELECT INITCAP(TRIM(' esto es una prueba ')) as category FROM es").show
spark.sql("SELECT INITCAP(TRIM(col.category)) as category FROM es").show


//val prueba4 = spark.sql("SELECT REPLACE(col.hostname, '-', '/') as hostname FROM (SELECT EXPLODE(data) FROM es)")

// spark.sql("SELECT REPLACE('20-12-2023', '-', '/') as rel_date FROM es").show
spark.sql("SELECT REPLACE(col.rel_date, '-', '/') as rel_date FROM es").show



// - QUERY FINAL -

spark.sql("SELECT
    CONCAT_WS(', ', TRIM(SPLIT(col.author_name, ' ')[1]), TRIM(SPLIT(col.author_name, ' ')[0])) as author_name,
    --- as author_inst,
    INITCAP(TRIM(col.category)) as category,
    REPLACE(col.rel_date, '-', '/') as rel_date
FROM es").saveToEs("documents") // Consulta; se guarda en el indice "documents"

val dfRes = sqlcontext.read.options(options).format("org.elasticsearch.spark.sql").load("documents")
dfRes.show

// - COMANDOS DE SPARK -

df.show // Muestra el resultado del indice
df.printSchema    // Muestra los diferentes fields/columnas en el indice