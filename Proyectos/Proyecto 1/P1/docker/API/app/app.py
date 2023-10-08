from datetime import datetime, timedelta
from borneo.iam import SignatureProvider
from borneo import NoSQLHandle, NoSQLHandleConfig, Regions, PutRequest, QueryRequest
from flask import Flask, request, Response, jsonify
from flask_pymongo import PyMongo
from prometheus_client import start_http_server, Summary, Gauge, make_wsgi_app
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from bson import json_util
from bson.json_util import dumps
import oracledb
import time 
from json import loads

app = Flask(__name__)
 
#Conexion de mongo 
uri = 'mongodb+srv://admin:Tgw4ykcov122w5aa@basedatosadj.uzcvkif.mongodb.net/?retryWrites=true&w=majority'
client= MongoClient(uri)

#Oracle database
cs='''(description= (retry_count=20)(retry_delay=3)(address=(protocol=tcps)(port=1522)(host=adb.us-chicago-1.oraclecloud.com))(connect_data=(service_name=gd72ea22cc39bd2_ic4302_high.adb.oraclecloud.com))(security=(ssl_server_dn_match=yes)))'''
connection=oracledb.connect(  
     user="ADMIN",
     password="thisiswrongNereo08",
     dsn=cs)
print("Successfully connected to Oracle Database")


#Conexion No-sql

at_provider =SignatureProvider(tenant_id="""ocid1.tenancy.oc1..aaaaaaaa3epwpfrm2lqzabu6lvt2dggy7mixxirw3o4x34s2y23rhh34n6oq',
                               user_id= 'ocid1.user.oc1..aaaaaaaawyygyja6timgy2wvdb5v7kok7d5jmjsoktyxh2ciulip5hnvmomq',
                               private_key='/app/.oci/oci_api_key.pem""",
                                fingerprint= '32:5e:ab:23:3e:2e:b5:91:41:fc:8f:c5:ea:7d:30:6e')

region = Regions.US_CHICAGO_1
config = NoSQLHandleConfig(region, at_provider)
handle = NoSQLHandle(config)

Request_time = Summary('request_processing_seconds_MongoAtlas_BuscaGeneral', 'Tiempo tomado en el request General Mongo')
Request_time1 = Summary('request_processing_seconds_MongoAtlas_BuscarFiltros', 'Tiempo tomado en el request Filtro Mongo')
Request_time2 = Summary('request_processing_seconds_AutomousDatabase_Busqueda', 'Tiempo tomado en el request General AD')
pruebas = Gauge('prueba', 'prueba')



db = client.wikidatos
coleccion= db['wikidata']



@app.route('/', methods=['GET'])
def prueba():
    pruebas.inc()
    query={'hola': 'prueba'}
    return Response(query, mimetype='application/json')

#Busqueda General
@Request_time.time() 
@app.route('/buscaGene/<valor>', methods=['GET'])
def busqueda(valor):
    with Request_time.time():
        if valor:
           result= coleccion.aggregate([
                {
                    '$search':{
                        'index': 'generalindice',
                        'facet':{
                            'operator':{
                                'compound':{
                                    'should':[{
                                        'text':{
                                            'query': f'{valor}',
                                            'path': 'PageTitle'
                                        }
                                    },{
                                        'text':{
                                            'query': f'{valor}',
                                            'path': 'PageText'
                                        }
                                    }]
                                }
                            },
                                'facets':{
                                    'SiteLanguage':{
                                        'type': 'string',
                                        'path': 'SiteLanguage'
                                    },
                                    'PageLastModified':{
                                        'type': 'string',
                                        'path': 'PageLastModifiedUser',
                                    },
                                    'SiteInfoName':{
                                        'type': 'string',
                                        'path': 'SiteInfoName'
                                    }, 
                                    'PageLastModifiedUser':{
                                        'type': 'string',
                                        'path': 'PageLastModifiedUser'
                                    },
                                    'PageNamespaces':{
                                        'type': 'string',
                                        'path': 'PageNamespaces'
                                    },
                                    'PageRedirect':
                                    {
                                        'type': 'string',
                                        'path': 'PageRedirect'
                                    },
                                    'PageRestriction':{
                                        'type': 'string',
                                        'path': 'PageRestriction'
                                    },
                                    'SiteInfoDBName': {
                                        'type': 'string',
                                        'path': 'SiteInfoDBName'
                                    },
                                    'SiteInfoName':{
                                        'type': 'string',
                                        'path': 'SiteInfoName'
                                    },
                                    'PageNumberLinks':{
                                        'type': 'number',
                                        'path': 'PageNumberLinks',
                                        'boundaries':[0, 5, 10, 15, 20, 25, 30],
                                        'default': 'mas'
                                    },
                                    'PageLastModified':{
                                        'type': 'date',
                                        'path': 'PageLastModified',
                                        'boundaries': [datetime(2010, 1, 1), datetime(2015, 1, 1), datetime(2020, 1, 1), 
                                                       datetime(2025, 1, 1)],
                                        'default': 'mas'
                                    },
                                    'PageBytes': {
                                        'type': 'number',
                                        'path': 'PageBytes',
                                        'boundaries': [50000, 100000, 150000, 200000],
                                        'default': 'mas'
                                    }
                            }
                        },
                        'highlight':{
                            'path': 'PageText'
                        }
                    }  
                },{
                    '$facet': {
                        'doc':[
                            {'$limit': 3},
                            {
                                '$project':{
                                    'PageId': 1,
                                    'PageTitle':2,
                                    'highlights': {'$meta': 'searchHighlights'}
                                }
                            }
                        ],
                        'meta':[
                            {'$replaceWith': '$$SEARCH_META'},
                            {'$limit': 1}
                        ]
                    }
                },{
                    '$set':{
                        'meta':{
                            '$arrayElemAt': ['$meta', 0]
                        }   
                    }
                }
            ])
        jsonResult= dumps(result)
        #Seccion de los logs.
        url = request.url
        dates = datetime.now()
        query = 'SELECT max(logId) FROM ic4302_logs'
        consulta= QueryRequest().set_statement(query)
        result = handle.query_iterable(consulta)
        for i in result:
            if i['Column_1'] != None:
                logId= int(i['Column_1'])+1
            else:
                logId = 0
        queue = PutRequest().set_table_name(table_name='ic4302_logs')
        queue.set_value({'logId': logId,'title': 'request/mongo', 'bagInfo':{'time':dates, 'url': url}})
        result = handle.put(queue)
        pruebas.inc()
        #Final de los logs
        return Response(jsonResult, mimetype='application/json')
#Busqueda con Filtros    
@Request_time1.time()   
@app.route('/buscarFiltros/<valor>', methods=['GET'])
def searchFiltering(valor):
    with Request_time1.time():
        text = {
            'text': {
                'query': 'value',
                'path' : 'value'
            }
        }
        leng = request.args.get('leng')
        fecha= request.args.get('fecha')
        bytes = request.args.get('bytes')
        numLink = request.args.get('nLink')
        namespace = request.args.get('nameSpace')
        restriction = request.args.get('rest')
        infoName = request.args.get('infoName')
        infodbName = request.args.get('indbName')
        pageredirect = request.args.get('redirect')
        if valor:
            fil = [] 
            if leng != None:
                leng = leng.split("-")
                reLeng={
                    'text': {
                        'query': leng,
                        'path' : 'SiteLanguage'
                    }
                }     
                fil.append(reLeng)
            if fecha != None:
                suma = timedelta(days=365*5)
                fecha = datetime.strptime(fecha, '%d/%m/%Y')
                print(fecha)
                print(fecha +suma)
                date = {
                    'range': {
                        'path': 'PageLastModified',
                        'gt' : fecha,
                        'lt': fecha +suma
                    }
                } 
                fil.append(date)
            if bytes != None:
                bytes = int(bytes)
                byteRe = {
                    'range': {
                        'path': 'PageBytes',
                        'gt' : bytes,
                        'lt': bytes + 50000
                    }
                } 
                fil.append(byteRe)
            if numLink != None:
                numLink = int(numLink)
                reNuLink ={
                    'range': {
                        'path': 'PageLastModified',
                        'gt' : numLink,
                        'lt': numLink+5
                    }
                } 
                fil.append(reNuLink)
            if namespace != None:
                namespace = namespace.split("-")
                reNamesp={
                    'text': {
                        'query': namespace,
                        'path' : 'PageNamespace'
                    }
                }  
                fil.append(reNamesp)
            if restriction != None:
                restriction= restriction.split("-")
                reRestric ={
                    'text': {
                        'query': restriction,
                        'path' : 'PageRestriction'
                    }
                }  
                fil.append(reRestric)
            if infoName != None:
                infoName = infoName.split("-")
                reInfo={
                    'text': {
                        'query': infoName,
                        'path' : 'SiteInfoName'
                    }
                }  
                fil.append(reInfo)
            if infodbName != None:
                infodbName = infodbName.split("-")
                reDb = {
                    'text': {
                        'query': infodbName,
                        'path' : 'SiteInfoDBName'
                    }
                }  
                fil.append(reDb)
            if pageredirect != None:
                pageredirect = pageredirect.split("-")
                rePageRe ={
                    'text': {
                        'query': pageredirect,
                        'path' : 'PageRedirect'
                    }
                } 
                fil.append(rePageRe)
            #Seccion del filtrado
            query=[
                {
                    '$search':{
                        'index': 'generalindice',
                        'facet':{
                            'operator':{
                                'compound':{
                                    'should':[{
                                        'text':{
                                            'query': f'{valor}',
                                            'path': 'PageTitle'
                                        }
                                    },{
                                        'text':{
                                            'query': f'{valor}',
                                            'path': 'PageText'
                                        }
                                    }],
                                    'filter': fil 
                                },
                            },
                                'facets':{
                                        'SiteLanguage':{
                                            'type': 'string',
                                            'path': 'SiteLanguage'
                                        },
                                        'PageLastModified':{
                                            'type': 'string',
                                            'path': 'PageLastModifiedUser',
                                        },
                                        'SiteInfoName':{
                                            'type': 'string',
                                            'path': 'SiteInfoName'
                                        }, 
                                        'PageLastModifiedUser':{
                                            'type': 'string',
                                            'path': 'PageLastModifiedUser'
                                        },
                                        'PageNamespaces':{
                                            'type': 'string',
                                            'path': 'PageNamespaces'
                                        },
                                        'PageRedirect':
                                        {
                                            'type': 'string',
                                            'path': 'PageRedirect'
                                        },
                                        'PageRestriction':{
                                            'type': 'string',
                                            'path': 'PageRestriction'
                                        },
                                        'SiteInfoDBName': {
                                            'type': 'string',
                                            'path': 'SiteInfoDBName'
                                        },
                                        'SiteInfoName':{
                                            'type': 'string',
                                            'path': 'SiteInfoName'
                                        },
                                        'PageNumberLinks':{
                                            'type': 'number',
                                            'path': 'PageNumberLinks',
                                            'boundaries':[0, 5, 10, 15, 20, 25, 30],
                                            'default': 'mas'
                                        },
                                        'PageLastModified':{
                                            'type': 'date',
                                            'path': 'PageLastModified',
                                            'boundaries': [datetime(2010, 1, 1), datetime(2015, 1, 1), datetime(2020, 1, 1), 
                                                           datetime(2025, 1, 1)],
                                            'default': 'mas'
                                        },
                                        'PageBytes': {
                                            'type': 'number',
                                            'path': 'PageBytes',
                                            'boundaries': [50000, 100000, 150000, 200000],
                                            'default': 'mas'
                                        }
                                }
                            },
                            'highlight':{
                                'path': 'PageText'
                            }
                        }
                    },{
                    '$facet': {
                        'doc':[
                            {'$limit': 3},
                            {
                                '$project':{
                                    'PageId': 1,
                                    'PageTitle':2,
                                    'highlights': {'$meta': 'searchHighlights'}
                                }
                            }
                        ],
                        'meta':[
                            {'$replaceWith': '$$SEARCH_META'},
                            {'$limit': 1}
                        ]
                    }
                },{
                    '$set':{
                        'meta':{
                            '$arrayElemAt': ['$meta', 0]
                        }   
                    }
                }
            ]
            #Seccion de logs
            url = request.url
            dates = datetime.now()
            statement = 'SELECT max(logId) FROM ic4302_logs'
            consulta= QueryRequest().set_statement(statement)
            result = handle.query_iterable(consulta)
            for i in result:
                if i['Column_1'] != None:
                    logId= int(i['Column_1'])+1
                else:
                    logId = 0
            queue = PutRequest().set_table_name(table_name='ic4302_logs')
            queue.set_value({'logId': logId,'title': 'request/mongo', 'bagInfo':{'time':dates, 'url': url}})
            result = handle.put(queue)
            #Final de seccion
            result = coleccion.aggregate(query)
            jsonResult = dumps(result)
            return Response(jsonResult, mimetype='application/json')
        
######################################################
@Request_time2.time()
@app.route("/getData/<texto_dado>")
def getData(texto_dado):
    with Request_time2.time():
        cursor1 = connection.cursor()#cursor para realizar las consultas
        queryData=  """

            SELECT JSON_OBJECT(
                'PageTitle' VALUE p.title,
                'PageText' VALUE p.text,
                'PageWikipediaLinks' VALUE p.wikiLinks
            )
            FROM Page p 
            WHERE p.text LIKE '%' || :texto_dado || '%'

            """

        cursor2 = connection.cursor()#cursor para realizar las consultas
        queryFacet =  """

                WITH facet_data AS (

                SELECT
                    'PageNamespace' AS field,
                    p.NAMESPACE AS value,
                    COUNT(*) AS COUNT

                FROM
                    Page p
                WHERE
                    p.text LIKE '%' || :texto_dado || '%'
                GROUP BY
                    p.NAMESPACE

                UNION ALL

                SELECT
                    'Redirect' AS field,
                    p.REDIRECT AS value,
                    COUNT(*) AS count
                FROM
                    Page p
                WHERE
                    p.text LIKE '%' || :texto_dado || '%'
                GROUP BY
                    p.REDIRECT

                UNION ALL

                SELECT
                    'Restriction' AS field,
                    p.RESTRICTION AS value,
                    COUNT(*) AS count
                FROM
                    Page p
                WHERE
                    p.text LIKE '%' || :texto_dado || '%'
                GROUP BY
                    p.RESTRICTION

                UNION ALL

                SELECT
                    'SiteInfoName' AS field,
                    s.INFODBNAME AS value,
                    COUNT(*) AS count
                FROM
                    Page p
                JOIN 
                    Site s ON p.id_Site = s.id_Site
                WHERE
                    p.text LIKE '%' || :texto_dado || '%' 
                GROUP BY
                    s.INFODBNAME

            UNION ALL

            SELECT
                    'SiteInfoDBName' AS field,
                    s.INFODBNAME AS value,
                    COUNT(*) AS count
                FROM
                    Page p
                JOIN 
                    Site s ON p.id_Site = s.id_Site
                WHERE
                    p.text LIKE '%' || :texto_dado || '%' 
                GROUP BY
                    s.INFODBNAME

                UNION ALL

                SELECT
                    'SiteLanguaje' AS field,
                    l.NAME AS value,
                    COUNT(*) AS count
                FROM
                    Page p
                JOIN 
                    Site s ON p.id_Site = s.id_Site
                    JOIN Languaje l ON s.id_Languaje = l.id_Languaje
                WHERE
                    p.text LIKE '%' || :texto_dado || '%' 
                GROUP BY
                    l.NAME

                UNION ALL

                SELECT
                    'PageLastModified' AS field,
                    p.LASTMODIFY AS value,
                    COUNT(*) AS count
                FROM
                    Page p

                WHERE
                    p.text LIKE '%' || :texto_dado || '%' 
                GROUP BY
                    p.LASTMODIFY

                UNION ALL

                SELECT
                    'PageLastModifiedUser' AS field,
                    u.NAME AS value,
                    COUNT(*) AS count
                FROM
                    Page p
                JOIN 
                    Usertable u ON u.id_User  = p.id_User 
                WHERE
                    p.text LIKE '%' || :texto_dado || '%' 
                GROUP BY
                    u.NAME


                UNION ALL

                SELECT
                    'PageLinks' AS field,
                    p.PAGELINKS AS value,
                    COUNT(*) AS count

                FROM
                    Page p
                WHERE
                    p.text LIKE '%' || :texto_dado || '%' 
                GROUP BY
                    p.PAGELINKS



            )
            SELECT JSON_OBJECT(
                field,
                value,
                count
            )
            FROM
                facet_data

            """

        resultadosData = []
        resultadosFacet = []

        for row in cursor1.execute(queryData, {'texto_dado': texto_dado}):
            resultadosData.append(loads(row[0]))

        for row in cursor2.execute(queryFacet, {'texto_dado': texto_dado}):
            resultadosFacet.append(loads(row[0]))

        cursor3 = connection.cursor()#cursor para realizar las consultas
        queryBytes= """ 
            SELECT JSON_OBJECT(
            'field' VALUE 'PageBytes',
        	'value' VALUE p.BYTES,
        	'count' VALUE COUNT(*)
            )
            FROM
                Page p
            WHERE
                p.text LIKE '%' || :texto_dado || '%' 
            GROUP BY
                p.BYTES

        """

        for row in cursor3.execute(queryBytes, {'texto_dado': texto_dado}):
            resultadosFacet.append(loads(row[0]))

        resultados = []
        resultados.append(resultadosData)
        resultados.append(resultadosFacet)   
        #Seccion de logs
        url = request.url
        dates = datetime.now()
        statement = 'SELECT max(logId) FROM ic4302_logs'
        consulta= QueryRequest().set_statement(statement)
        result = handle.query_iterable(consulta)
        for i in result:
            if i['Column_1'] != None:
                logId= int(i['Column_1'])+1
            else:
                logId = 0
        queue = PutRequest().set_table_name(table_name='ic4302_logs')
        queue.set_value({'logId': logId,'title': 'request/mongo', 'bagInfo':{'time':dates, 'url': url}})
        result = handle.put(queue)
        #Final de seccion

        return resultados

if __name__ == "__main__":
    start_http_server(8000) 
    app.run(host="0.0.0.0", port=5000, debug=True)
     
    