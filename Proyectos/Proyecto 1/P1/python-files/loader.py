import oci
import io

import mwxml

import pymongo
import xml.etree.ElementTree as ET

import cx_Oracle

# --- CONFIG ---

# Una vez hecho el "oci setup config", revisar: cat ~/.oci/

config = {
   "key_content": """-----BEGIN PRIVATE KEY-----
MIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQC4CqZSru+uTdSg
vvRaVwvx0u+gAQ/F8vlloxXwpTLJDccpobEr/ZUEIU0mYxdWxSvlP7/763KuhEje
sJ/zxdsxce/wyegHUbKHYquYHBGKkKx5SfaSqeuDJAUKuwkyWz84liC0S5Y9B+8h
+vSZftsTTXeUN4nXvYUeNLW4RMvTUK6cIG32cAkTjUsZpgFcMwU0r62xk5jNfRAu
KFTF35toaUPwvgJK4y0mvPW3GmGr3WDvplKAKZOzBfEVFqNEtkXy4RIfGP4YLza4
NDOxcZCN5H2+fKrPoQs84jgHzStuNaPL3nFUnmNNPjvjJoyobzROKRNBN7xrxIeJ
xz3SWBIJAgMBAAECggEAB6CJXAvb6wFWuoKvZb8Nw6vWOm9Q1AdJxqiHlD2EaUik
5FjLGuObdVxb8idRJEtvkkSeFDahvhHFY1U2i8e7WcU7CGOVthfwqiOwsNEY+QEd
5Ljn+xQHqpunidZOf0PAzvuJx28KfuUBSAs6b9IOCjK/rejPUZ2NEr9keIqBV/SB
9VK/qNyyZsoy1NTjyN2426nbsBF3uLQnX0dJqBGmMnHCQnYkWzP1zKF6up/QqFXx
3yv9s+u/ehFso4TkKTABQrHz/4nsYA55WmwCXC66Ml7K9KjComqkgZm/cbfYRhkf
DFkv5tyUEb6HCb63W9L4l0dRdcrHeVP/Vks2DLPdcQKBgQDuxaT1ZQ/347KhNGba
jIGUrheUmggQtTNMe5QvLvY/dih2hbMAPskomUhK+oz/YGgZi17fz9BFLBGtDMld
WMrPnxikeSkkGARDCQnBCKsI5Gs8/dNvdR/NGivBzCIaIMfY7XO1DDORMbHt5FLT
lVFumbp5Dwk+DJCBlxHtzxNp6wKBgQDFUhRzU4JyIXh7/WcO5KodEpdntWjdeZKF
60I+iKZpgqhq/mwDzj1dGQXhxbz08Xsaa6TeJjiP9VZqBeU+j+j4JXujbBIrQF7Z
NUIgcyKtQtReNlHUIFKX2Dnx8pemzFrVSXhI6JuOxzoKGvBF17QqiRUtghafKbcq
TbVHufHi2wKBgCEXnWwxTIxDr48uDw89J/xuQHBlBLckFe8EtZ3weUqEWslKcGuZ
SBHrZJyXqxD90I+xxD1qtOfRWsXMHuBkHP+3ghfRfwU0muqbhxGM3P+HgOFcIICz
D+xCM0xRuWw7nNcQ2dd+0GrQI2PgICaY7EdS4QhEMDi8Tw7W3DJEX+FvAoGBALhv
8mGh60pW8tGimNQY9NFb8V2k+bIa0tSOhEsDW9k/ocDws3ITMtR0cUUJmYeyuAiI
GYD0ZOZawj0z6YXC6lYYYyrr90eqUX3iBD9kn0MoNm0hhPcsh0cbe34l7Y6hcT3w
AJjVo6GfoyaS64e9CdDAdaUl9ZMsYOMP46R5sBkFAoGBAN1CJj9uGWDZF8K82X3q
yYYOkDWyFRwEvp9tOJ780GmNWu6c3uHBX5Sc780K96GCvQ/wmpVFqZ/h8n7r+lu1
0KMNj8GRb3H0r886sdJybaSiu/V8MGpxgpF/2N9QLetfORip2N/10WfkVmSB9ymP
tPEyYmr51u5OMFcUEy+O0ev2
-----END PRIVATE KEY-----""",
  "user": "ocid1.user.oc1..aaaaaaaahjsrlczdcqcazwhkb3jyotdwq4opnyxr5cx7ctxo3xd5uf7eu25q",
  "fingerprint": "ba:07:35:0c:75:66:58:e5:63:13:11:98:33:97:70:94",
  "tenancy": "ocid1.tenancy.oc1..aaaaaaaa22p5zz37ti2o4fo4wgid5iqaekkaxnykgycssznueu4kfz5272uq",
  "region": "us-chicago-1"
}

# --------------

formato1 = "enwiki-latest-pages-articles-multistream-index" # TXT largo
formato2 = "enwiki-latest-abstract" # XML
formato3 = "enwiki-latest-pages-articles-multistream" # XML largo, parser normal

oci.config.validate_config(config) # Validacion del config
object_storage = oci.object_storage.ObjectStorageClient(config) # Se conecta al Object Storage

bucket = 'david'
compartment_id = config['tenancy']
namespace = object_storage.get_namespace().data

list_objects_response = object_storage.list_objects(namespace_name=namespace, bucket_name=bucket)


mongo_uri = "mongodb+srv://admin:Tgw4ykcov122w5aa@basedatosadj.uzcvkif.mongodb.net/?retryWrites=true&w=majority"
client = pymongo.MongoClient(mongo_uri)

db = client.wikidatos
collection = db['wikidata']


  # Loop de los files del Object Storage
for object_summary in list_objects_response.data.objects:

  # ===== Object Storage =====

  object_name = object_summary.name
  response = object_storage.get_object(namespace_name=namespace, bucket_name=bucket, object_name=object_name)
  object_content = response.data.content

  print("Archivo: ", object_name)

  if object_name.startswith(formato1):
    print("TXT")

    lines = object_content.decode('utf-8').splitlines()
    
    for line in lines:
      fields = line.split(':')

      if len(fields) == 3:
        unknown_id, page_id, page_title = fields

      page_data = {
          "PageId": page_id,
          "PageTitle": page_title
      }
      
      collection.insert_one(page_data)
      print("Subida a MONGO exitosa")

  elif object_name.startswith(formato2):
    print("XML")

    xml_string = object_content.decode('utf-8')
    tree = ET.ElementTree(ET.fromstring(xml_string))
    root = tree.getroot() 

    for doc_element in root.findall('doc'):
      
      title = doc_element.find('title').text
      url = doc_element.find('url').text
      abstract = doc_element.find('abstract').text

      links = doc_element.find('links')
      sublinks = links.findall('.//sublink')

      sublinks_data = []

      for sublink in sublinks:
        link = sublink.find('link').text
        sublinks_data.append(link)

      page_data = {
          "PageTitle": title,
          "PageText": abstract,
          "PageWikipediaLink": url,
          "PageLinks": sublinks_data
      }

      collection.insert_one(page_data)
      print("Subida a MONGO exitosa")

  elif object_name.startswith(formato3):
    print("XML LARGO")

    xml_file = io.BytesIO(object_content)

    # ===== Parser =====

    #dump = mwxml.Dump.from_file(open("/mnt/d/Tareas David/TEC/Semestre 8/Bases de Datos II/Bases_2/Proyectos/Proyecto 1/P1/Otros/enwiki-latest-pages-articles-multistream1.xml-p1p41242"))
    #dump = mwxml.Dump.from_file(open("/mnt/d/Tareas David/TEC/Semestre 8/Bases de Datos II/Bases_2/Proyectos/Proyecto 1/P1/Otros/enwiki-latest-abstract2.xml"))
    dump = mwxml.Dump.from_file(xml_file)

    #print(dump.site_info.name, dump.site_info.dbname)

    # ===== Mongo =====

    for page in dump:
      for revision in page:

        page_data = {
            "PageId": page.id,
            "PageTitle": page.title,
            "PageNamespaces": page.namespace,
            "PageRestriction": page.restrictions,
            "PageLastModifiedUser": revision.user.text,
            "PageBytes": revision.bytes,
            "PageText": revision.text
        }

        collection.insert_one(page_data)
        print("Subida a MONGO exitosa")

  else:
    print("ERROR, archivo desconocido")

  

#page_data = {
#    "_id": "ObjectId('6508ce5b92eabe2919130c23')",
#    "PageId": "12",
#    "PageTitle": "Anarchism",
#    "PageNamespaces": [],
#    "PageRedirect": "",
#    "PageHasRedirect": False,
#    "PageRestriction": [],
#    "SiteInfoName": "",
#    "SiteInfoDBName": "",
#    "SiteLanguage": "English",
#    "PageLastModified": "2023-08-31T15:06:22.000+00:00",
#    "PageLastModifiedUser": "Citation bot",
#    "PageBytes": 110933,
#    "PageText": "'''Anarchism''' is a [[political philosophy]] and [[Political movement...",
#    "PageWikipediaLink": "https://en.wikipedia.org/wiki/Anarchism",
#    "pageWikipediaGenerated": "http://en.wikipedia.org/?curid=12",
#    "PageLinks": [
#        "https://en.wikipedia.org/wiki/Anarchism#History",
#        "https://en.wikipedia.org/wiki/Anarchism#Pre-modern-era"
#    ],
#    "PageNumberLinks": 21
#}

client.close()

  # ===== Autonomous =====

  #username = 'your_username'
  #password = 'your_password'
  #dsn = cx_Oracle.makedsn('adb_host', 'port', service_name='service_name')

  #connection = cx_Oracle.connect(username, password, dsn)
  #cursor = connection.cursor()

  #table_name = 'your_table'
  #file_column = 'your_file_column'
  #file_path = '/path/to/your/file.pdf'
  #sql = f"INSERT INTO {table_name} ({file_column}) VALUES (BFILENAME('DIRECTORY', '{file_path}'))"

  #cursor.execute(sql)
  #connection.commit()

  #cursor.close()
  #connection.close()