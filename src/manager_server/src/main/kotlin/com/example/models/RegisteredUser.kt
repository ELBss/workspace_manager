package com.example.models

import kotlinx.serialization.SerialName
import kotlinx.serialization.Serializable

@Serializable
data class RegisteredUser(
    @SerialName("user_id") val userId: Int,
    val role: UserRole
)