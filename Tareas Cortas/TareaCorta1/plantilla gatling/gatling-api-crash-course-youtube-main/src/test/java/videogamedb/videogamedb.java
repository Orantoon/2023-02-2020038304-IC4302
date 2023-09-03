package videogamedb;
//Dependencias necesarias de java con la version de Gatling
import io.gatling.javaapi.core.*;
import io.gatling.javaapi.http.*;

//Facilitan la escritura de los scripts
import java.security.PublicKey;

import static io.gatling.javaapi.core.CoreDsl.*;
import static io.gatling.javaapi.http.HttpDsl.*;


public class videogamedb extends Simulation{

    //Http Configuración
    private HttpProtocolBuilder httpProtocol = http
            .baseUrl( "http://localhost:30127")
            .acceptHeader("application/json") //Encabezado
            .contentTypeHeader("application/json"); // Configurando del  tipo de encabezado


    //Runtime parameters

    private static final int USER_COUNT = Integer.parseInt(System.getProperty("USERS", "5"));

    private static final int RAMP_DURATION = Integer.parseInt(System.getProperty("USERS", "10"));

    //-----------------------------------------
    // Feed de datos de prueba

    private static FeederBuilder.FileBased<Object> jsonFeeder = jsonFile("data/gameJsonFile.json").random();

    public void before(){
        System.out.printf("Running test %d users%n", USER_COUNT);
        System.out.printf("Ramping users over %d seconds%n", RAMP_DURATION);
    }

    //Llamadas del HTTP
    private  static  ChainBuilder getAllGames =
            exec(http("Get all games") // Nombre de la transaccion
                    .get("/videogames"));

    private static ChainBuilder authenticate =
            exec(http("Authenticate") // Nombre de la transaccion
                    .post("/authenticate") // Endpoint llamado // Nombre de la transaccion
                    .body(StringBody("{\n" +
                            " \"password\": \"admin\",\n" +
                            " \"username\": \"admin\" \n" +
                            "}"))
                    .check(jmesPath("token").saveAs("jwtToken"))); //Extrae el token
                    // Con el parametro token  se usa para obtener scriptsp

    private static ChainBuilder createNewGame =
            feed(jsonFeeder) // Llama al alimentador del json y luego todos los datos de prueba
                            .exec(http("Create New Game - #{name}")
                            .post("/videogames")
                            .header("Authorzation", "Bearer #{jwtToken}")
                            .body(ElFileBody("bodies/newGameTemplate.json")).asJson()); //Plantilla para crear un nuevo juego

    private static ChainBuilder getLastPostedGame =
            exec(http("get Last Posted Game - #{name}") // Nombre de la transaccion
                    .get("/videogames/#{id}") //El  id del video juego
                    .check(jmesPath("name").isEL("#{name}"))); //Verifica que coincida el nombre

    private  static ChainBuilder deleteLastPostedGame =
            exec(http("Delete Game - #{name}")
                    .delete("/videogames/#{id}")
                    .header("Authorzation", "Bearer #{jwtToken}")
                    .check(bodyString().is("Video game delete")));


    // Defincion del Scenario
    // 1.Get all video games
    // 2.Autenticacion
    // 3.Create a new game
    // 4.Detalles del nuevo juego
    // 5.Eliminiar el juego recien creado


    private ScenarioBuilder scn = scenario( "Video game DB Stress Test") // Llama todos los metodos
            //Primer llamada conseguir todos los juegos
            .exec(getAllGames)
            .pause(2) //pausa por 2 segundos
            .exec(authenticate)
            .pause(2) //pausa por 2 segundos
            .exec(createNewGame)
            .pause(2) //pausa por 2 segundos
            .exec(getLastPostedGame)
            .pause(2) //pausa por 2 segundos
            .exec(deleteLastPostedGame);
            //Scenario listo




    // Carga d ela simulacion
    //Bloque de configuración
    {
        setUp(
                //scn : Escenario que se definio anteriormente
                scn.injectOpen(nothingFor(5),
                        rampUsers(USER_COUNT).during(RAMP_DURATION)) // No hace nada despues de los 5 segundos
                // Aplicacion de protocolos
        ).protocols((httpProtocol));

    }
}
