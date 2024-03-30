package com.example

import com.example.plugins.*
import com.example.utils.sendTelegramNotification
import io.ktor.server.application.*
import io.ktor.server.engine.*
import io.ktor.server.netty.*
import kotlinx.coroutines.*
import org.jetbrains.exposed.sql.and
import org.jetbrains.exposed.sql.select
import org.jetbrains.exposed.sql.transactions.transaction
import java.time.LocalDateTime

fun main() {
    embeddedServer(Netty, port = 8080, host = "0.0.0.0", module = Application::module)
        .start(wait = true)

    GlobalScope.launch {
        while (isActive) {
            checkReservationsAndNotify()
            delay(60000)
        }
    }
}

fun Application.module() {
    configureRouting()
}

@OptIn(DelicateCoroutinesApi::class)
suspend fun checkReservationsAndNotify() {
    transaction {
        val now = LocalDateTime.now()
        ReservationService.Reservations.select {
            (ReservationService.Reservations.begin greaterEq now.plusMinutes(14)) and
                    (ReservationService.Reservations.end lessEq now.plusMinutes(15))
        }.forEach {
            val userId = it[ReservationService.Reservations.userId]
            val roomId = it[ReservationService.Reservations.roomId]
            GlobalScope.launch {
                sendTelegramNotification(userId.toString(), "Your event begins in 15 minutes in Room $roomId")
            }
        }

        ReservationService.Reservations.select {
            (ReservationService.Reservations.end lessEq now.plusMinutes(5)) and
                    (ReservationService.Reservations.end greaterEq now.plusMinutes(4))
        }.forEach {
            val userId = it[ReservationService.Reservations.userId]
            val roomId = it[ReservationService.Reservations.roomId]
            GlobalScope.launch {
                sendTelegramNotification(userId.toString(), "Your reservation in Room $roomId ends in 5 minutes")
            }
        }
    }
}

