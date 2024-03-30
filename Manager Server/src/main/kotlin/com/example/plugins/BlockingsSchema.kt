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
import org.jetbrains.exposed.sql.javatime.date

@Serializable
data class ExposedBlocking(
    @SerialName("room_id") val roomId: String,
    val begin: LocalDate,
    val end: LocalDate,
    val tag: String
    )
class BlockingService(private val database: Database) {
    object Blockings : IntIdTable() {
        val roomId = varchar("room_id", length = 8)
        val begin = date("begin")
        val end = date("end")
        val tag = varchar("tag", length = 16)
    }

    init {
        transaction(database) {
            SchemaUtils.create(Blockings)
        }
    }

    suspend fun <T> dbQuery(block: suspend () -> T): T =
        newSuspendedTransaction(Dispatchers.IO) { block() }

    suspend fun create(blocking: ExposedBlocking): Int = dbQuery {
        Blockings.insert {
            it[roomId] = blocking.roomId
            it[begin] = blocking.begin.toJavaLocalDate()
            it[end] = blocking.end.toJavaLocalDate()
            it[tag] = blocking.tag
        }[Blockings.id].value
    }

    suspend fun read(id: Int): ExposedBlocking? {
        return dbQuery {
            Blockings.select { Blockings.id eq id }
                .map { ExposedBlocking(it[Blockings.roomId], it[Blockings.begin].toKotlinLocalDate(),
                    it[Blockings.end].toKotlinLocalDate(), it[Blockings.tag]) }
                .singleOrNull()
        }
    }

    suspend fun update(id: Int, blocking: ExposedBlocking) {
        dbQuery {
            Blockings.update({ Blockings.id eq id }) {
                it[roomId] = blocking.roomId
                it[begin] = blocking.begin.toJavaLocalDate()
                it[end] = blocking.end.toJavaLocalDate()
                it[tag] = blocking.tag
            }
        }
    }

    suspend fun delete(id: Int) {
        dbQuery {
            Blockings.deleteWhere { Blockings.id.eq(id) }
        }
    }

    suspend fun getAll(): List<ExposedBlocking> {
        return dbQuery {
            Blockings.selectAll()
                .map { ExposedBlocking(it[Blockings.roomId], it[Blockings.begin].toKotlinLocalDate(),
                    it[Blockings.end].toKotlinLocalDate(), it[Blockings.tag]) }
        }
    }
}

