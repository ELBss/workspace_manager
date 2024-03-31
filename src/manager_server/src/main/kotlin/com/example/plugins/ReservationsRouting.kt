package com.example.plugins

import com.example.models.RegisteredUser
import com.example.models.UserRole
import com.example.utils.HttpClientProvider
import com.example.utils.authServiceUrl
import com.example.utils.sendTelegramNotification
import com.example.utils.superUserId
import io.ktor.client.call.*
import io.ktor.client.request.*
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
            val userId = reservation.userId
            val authResponse = HttpClientProvider.authServiceClient.get(authServiceUrl + "user/id=$userId")
            if (authResponse.status == HttpStatusCode.OK) {
                val user = authResponse.body<RegisteredUser>()
                if (user.role == UserRole.ADM || user.role == UserRole.COMMON) {
                    val id = reservationService.create(reservation)
                    call.respond(HttpStatusCode.Created, id)
                    sendTelegramNotification(userId.toString(), "Reservation successfully")
                } else {
                    sendTelegramNotification(superUserId, "Somebody has attempted unauthorized reservation")
                    call.respond(HttpStatusCode.Forbidden)
                }
            } else {
                call.respond(HttpStatusCode.Unauthorized)
            }
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

        delete("/reservations/id={id}") {
            val id = call.parameters["id"]?.toInt() ?: throw IllegalArgumentException("Invalid ID")
            reservationService.delete(id)
            call.respond(HttpStatusCode.OK)
        }
    }
}