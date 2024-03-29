package com.example.plugins

import org.jetbrains.exposed.sql.transactions.transaction
import org.jetbrains.exposed.sql.transactions.experimental.newSuspendedTransaction
import org.jetbrains.exposed.sql.SqlExpressionBuilder.eq
import kotlinx.serialization.Serializable
import kotlinx.coroutines.Dispatchers
import kotlinx.datetime.*
import kotlinx.serialization.SerialName
import org.jetbrains.exposed.dao.id.IntIdTable
import org.jetbrains.exposed.sql.*
import org.jetbrains.exposed.sql.javatime.datetime

enum class ReservationPurpose {
    MEETUP,
    STUDY,
    WORK
}

@Serializable
data class ExposedReservation(
    val id: Int?,
    @SerialName("user_id") val userId: Int,
    @SerialName("room_id") val roomId: Int,
    val begin: LocalDateTime,
    val end: LocalDateTime,
    val purpose: ReservationPurpose,
    val participants: Int,
    val comment: String
    )

class ReservationService(private val database: Database) {
    object Reservations : IntIdTable() {
        val userId = integer("user_id")
        val roomId = integer("room_id")
        val begin = datetime("begin")
        val end = datetime("end")
        val purpose = enumeration<ReservationPurpose>("purpose")
        val participants = integer("participants")
        val comment = varchar("comment", length = 64)
    }

    init {
        transaction(database) {
            SchemaUtils.create(Reservations)
        }
    }

    suspend fun <T> dbQuery(block: suspend () -> T): T =
        newSuspendedTransaction(Dispatchers.IO) { block() }

    suspend fun create(reservation: ExposedReservation): Int = dbQuery {
        Reservations.insert {
            it[userId] = reservation.userId
            it[roomId] = reservation.roomId
            it[begin] = reservation.begin.toJavaLocalDateTime()
            it[end] = reservation.end.toJavaLocalDateTime()
            it[purpose] = reservation.purpose
            it[participants] = reservation.participants
            it[comment] = reservation.comment
        }[Reservations.id].value
    }

    suspend fun read(id: Int): ExposedReservation? {
        return dbQuery {
            Reservations.select { Reservations.id eq id }
                .map { ExposedReservation(it[Reservations.id].value, it[Reservations.userId], it[Reservations.roomId],
                    it[Reservations.begin].toKotlinLocalDateTime(), it[Reservations.end].toKotlinLocalDateTime(),
                    it[Reservations.purpose], it[Reservations.participants], it[Reservations.comment]) }
                .singleOrNull()
        }
    }

    suspend fun update(id: Int, reservation: ExposedReservation) {
        dbQuery {
            Reservations.update({ Reservations.id eq id }) {
                it[userId] = reservation.userId
                it[roomId] = reservation.roomId
                it[begin] = reservation.begin.toJavaLocalDateTime()
                it[end] = reservation.end.toJavaLocalDateTime()
                it[purpose] = reservation.purpose
                it[participants] = reservation.participants
                it[comment] = reservation.comment
            }
        }
    }

    suspend fun delete(id: Int) {
        dbQuery {
            Reservations.deleteWhere { Reservations.id.eq(id) }
        }
    }

    suspend fun getReservationsByDate(date: LocalDate) : List<ExposedReservation> {
        val intervalStart = date.toJavaLocalDate().atStartOfDay()
        val intervalEnd = intervalStart.plusDays(1).minusMinutes(1)
        return dbQuery {
            Reservations.select { (Reservations.begin greaterEq intervalStart) and
                    (Reservations.end lessEq intervalEnd)
            }
                .map { ExposedReservation(it[Reservations.id].value, it[Reservations.userId], it[Reservations.roomId],
                it[Reservations.begin].toKotlinLocalDateTime(), it[Reservations.end].toKotlinLocalDateTime(),
                it[Reservations.purpose], it[Reservations.participants], it[Reservations.comment]) }
        }
    }
}

