import mwxml
dump = mwxml.Dump.from_file(open("/mnt/d/Tareas David/TEC/Semestre 8/Bases de Datos II/Bases_2/Proyectos/Proyecto 1/P1/Otros/enwiki-latest-pages-articles-multistream1.xml-p1p41242"))
#dump = mwxml.Dump.from_file(open("enwiki-latest-pages-articles-multistream1.xml-p1p41242"))
print(dump.site_info.name, dump.site_info.dbname)
for page in dump:
    print("###################################################################")
    print("TITLE: ", page.title)
    print("REDIRECT: ", page.redirect)
    print("ID: ", page.id)
    print("NAMESPACE: ", page.namespace)
    print("RESTRICTIONS: ", page.restrictions)
    print("___________")
    for revision in page:
        print("REV_ID: ", revision.id)
        print("REV_TIMESTAMP: ", revision.timestamp)
        print("REV_USER: ", revision.user)
        print("REV_PAGE: ", revision.page)
        print("REV_MINOR: ", revision.minor)
        print("REV_COMMENT: ", revision.comment)
        print("REV_TEXT:\n", revision.text)
        print("REV_BYTES: ", revision.bytes)
        print("REV_SHA1: ", revision.sha1)
        print("REV_PARENTID: ", revision.parent_id)
        print("REV_MODEL: ", revision.model)
        print("REV_FORMAT: ", revision.format)
        print("DELETED: ", revision.deleted)
    print("###################################################################")
    #break