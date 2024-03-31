package com.example.plugins

import io.ktor.http.*
import io.ktor.server.application.*
import io.ktor.server.request.*
import io.ktor.server.response.*
import io.ktor.server.routing.*

fun Application.configureBlockingsRouting(blockingService: BlockingService) {
    routing {
        post("/blockings") {
            val blocking = call.receive<ExposedBlocking>()
            val id = blockingService.create(blocking)
            call.respond(HttpStatusCode.Created, id)
        }

        get("/blockings") {
            val blockings = blockingService.getAll()
            call.respond(HttpStatusCode.OK, blockings)
        }

        get("/blockings/id={id}") {
            val id = call.parameters["id"]?.toInt() ?: throw IllegalArgumentException("Invalid ID")
            val blocking = blockingService.read(id)
            if (blocking != null) {
                call.respond(HttpStatusCode.OK, blocking)
            } else {
                call.respond(HttpStatusCode.NotFound)
            }
        }

        put("/blockings/id={id}") {
            val id = call.parameters["id"]?.toInt() ?: throw IllegalArgumentException("Invalid ID")
            val blocking = call.receive<ExposedBlocking>()
            blockingService.update(id, blocking)
            call.respond(HttpStatusCode.OK)
        }

        delete("/blockings/id={id}") {
            val id = call.parameters["id"]?.toInt() ?: throw IllegalArgumentException("Invalid ID")
            blockingService.delete(id)
            call.respond(HttpStatusCode.OK)
        }
    }
}