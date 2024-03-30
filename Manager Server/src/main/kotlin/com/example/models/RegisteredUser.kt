package com.example.models

import kotlinx.serialization.SerialName

data class RegisteredUser(
    @SerialName("user_id") val userId: Int,
    val role: UserRole
)