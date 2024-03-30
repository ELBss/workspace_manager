package com.example.plugins

import com.example.utils.sendTelegramNotification
import com.example.utils.superUserId
import io.ktor.http.*
import io.ktor.server.application.*
import io.ktor.server.request.*
import io.ktor.server.response.*
import io.ktor.server.routing.*
import io.ktor.server.plugins.openapi.*

fun Application.configureReservationsRouting(reservationService: ReservationService) {
    routing {
        post("/reservations") {
            val reservation = call.receive<ExposedReservation>()

            val id = reservationService.create(reservation)
            call.respond(HttpStatusCode.Created, id)
        }

        get("/reservations") {
            sendTelegramNotification(superUserId, "Somebody has read reservations")
            val reservations = reservationService.getAll()
            call.respond(HttpStatusCode.OK, reservations)
        }

        get("/reservations/id={id}") {
            val id = call.parameters["id"]?.toInt() ?: throw IllegalArgumentException("Invalid ID")
            val reservation =  reservationService.read(id)
            if (reservation != null) {
                call.respond(HttpStatusCode.OK, reservation)
            } else {
                call.respond(HttpStatusCode.NotFound)
            }
        }

        put("/reservations/id={id}") {
            val id = call.parameters["id"]?.toInt() ?: throw IllegalArgumentException("Invalid ID")
            val reservation = call.receive<ExposedReservation>()
            reservationService.update(id, reservation)
            call.respond(HttpStatusCode.OK)
        }

        delete("/blockings/id={id}") {
            val id = call.parameters["id"]?.toInt() ?: throw IllegalArgumentException("Invalid ID")
            reservationService.delete(id)
            call.respond(HttpStatusCode.OK)
        }
    }
}