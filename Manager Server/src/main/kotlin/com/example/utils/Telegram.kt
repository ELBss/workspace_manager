package com.example.utils

import io.ktor.client.request.*

suspend fun sendTelegramNotification(userId: String, message: String) {
    val url = "https://api.telegram.org/bot$botToken/sendMessage"
    val response = HttpClientProvider.authServiceClient.post(url) {
        parameter("chat_id", userId)
        parameter("text", message)
    }
}