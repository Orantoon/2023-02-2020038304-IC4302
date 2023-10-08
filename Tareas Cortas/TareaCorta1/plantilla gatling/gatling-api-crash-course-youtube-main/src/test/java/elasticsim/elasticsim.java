package elasticsim;

//Dependencias necesarias de java con la version de Gatling
import io.gatling.javaapi.core.*;
import io.gatling.javaapi.http.*;

//Facilitan la escritura de los scripts
import java.security.PublicKey;

import static io.gatling.javaapi.core.CoreDsl.*;
import static io.gatling.javaapi.http.HttpDsl.*;

public class elasticsim extends Simulation{

    //Http Configuración
    private HttpProtocolBuilder httpProtocol = http
            .baseUrl( "http://localhost:30127")
            .acceptHeader("application/json") // Encabezado / acepta JSONs
            .contentTypeHeader("application/json"); // Configurando del  tipo de encabezado

    //-----------------------------------------

    //Runtime parameters
    private static final int USER_COUNT = Integer.parseInt(System.getProperty("USERS", "4000"));   // Cantidad de suarios para las pruebas
    private static final int RAMP_DURATION = Integer.parseInt(System.getProperty("USERS", "60"));   // Tiempo de pruebas

    //-----------------------------------------

    // Feed de datos de prueba
    private static FeederBuilder.FileBased<Object> jsonFeeder = jsonFile("data/content.json").random();

    public void before(){
        System.out.printf("Running test %d users%n", USER_COUNT);
        System.out.printf("Ramping users over %d seconds%n", RAMP_DURATION);
    }

    //-----------------------------------------

    //Llamadas del HTTP
    private static ChainBuilder crearRegistro =
            feed(jsonFeeder) // Llama al alimentador del json y luego todos los datos de prueba
                    .exec(http("Crear Registro - #{name}")
                            .post("/crear")
                            .body(ElFileBody("bodies/newGameTemplate.json")).asJson()); //Plantilla para crear un nuevo juego

    private  static ChainBuilder borrarRegistro =
            exec(http("Borrar Registro - #{name}")
                    .delete("/borrar/#{name}"));

    private  static ChainBuilder actualizarRegistro =
            feed(jsonFeeder)
                    .exec(http("Actualizar Registro - #{name}")
                            .put("/actualizar/#{name}")
                            .body(ElFileBody("bodies/newGameTemplate.json")).asJson());

    private  static ChainBuilder busquedaRegistro =
            exec(http("Buscar Registro - #{name}")
                    .get("/buscar/#{id}")
                    .check(jmesPath("name").isEL("#{name}")));    // Revisa que sea el registro correcto

    //-----------------------------------------

    // Defincion del Scenario

    // 1. Crear registro
    // 2. Borrar registro
    // 3. Actualizar registro
    // 4. Busqueda registro

    private ScenarioBuilder scn = scenario( "Elasticsearch Stress Test") // Llama todos los metodos
            .exec(crearRegistro)
            .pause(2)  //pausa por 2 segundos
            .exec(actualizarRegistro)
            .pause(2)
            .exec(busquedaRegistro)
            .pause(2)
            .exec(borrarRegistro);

            //Scenario listo

    //-----------------------------------------

    // Carga de la simulacion

    //Bloque de configuración
    {
        setUp(
                //scn : Escenario que se definio anteriormente
                scn.injectOpen(nothingFor(5),   // No hace nada despues de los 5 segundos
                        rampUsers(USER_COUNT).during(RAMP_DURATION))    // Se corren las pruebas
                // Aplicacion de protocolos
        ).protocols((httpProtocol));

    }
}
