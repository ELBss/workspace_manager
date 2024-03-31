package com.example.utils

import io.ktor.client.*
import io.ktor.client.engine.cio.*
import io.ktor.client.plugins.contentnegotiation.*
import io.ktor.serialization.kotlinx.json.*
import org.h2.util.JdbcUtils.serializer

object HttpClientProvider {
    val authServiceClient = HttpClient(CIO) {
        install(ContentNegotiation) {
            json()
        }
    }
}