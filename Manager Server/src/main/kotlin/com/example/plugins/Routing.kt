package com.example.plugins

import io.ktor.server.application.*
import io.ktor.server.response.*
import io.ktor.server.routing.*

fun Application.configureRouting() {
    configureSerialization()
    configureDatabases()
    configureHTTP()
    routing {
        OpenAPIGen@
        get("/") {
            call.respondText("Welcome to Workspace Manager Server!")
        }
    }
}
